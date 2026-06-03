#!/usr/bin/env python3
"""
OCR 抽取脚本：处理扫描版 PDF 和图像型 EPUB，输出干净中文文本。

依赖：
  - tesseract（含 chi_sim 语言包）
  - python: pdf2image, Pillow
  - poppler-utils（pdf2image 后端）

环境变量：
  - TESSDATA_PREFIX：tesseract data 目录，含 chi_sim.traineddata

用法：
  python3 ocr_extract.py <input_file> <output_txt> [--dpi 200] [--start N] [--end N]

支持输入：
  - 扫描版 PDF（FreePic2Pdf 类型，无文本层）
  - 图像型 EPUB（OEBPS/Image*.jpg 为主要内容）

输出：干净 txt 文件 + 同目录下的 progress 日志
"""
import argparse, os, sys, subprocess, tempfile, re, zipfile, time, json
from pathlib import Path


def clean_chinese_ocr(text: str) -> str:
    """清洗 tesseract chi_sim 输出的常见瑕疵。"""
    # 1. 移除中文字符之间的空格（OCR 把每个汉字之间都加了空格）
    #    匹配两个 CJK 字符之间的空白
    text = re.sub(r'([一-鿿])\s+([一-鿿])', r'\1\2', text)
    text = re.sub(r'([一-鿿])\s+([一-鿿])', r'\1\2', text)  # 跑两遍
    # 2. CJK 与中文标点之间的空格
    text = re.sub(r'([一-鿿])\s+([，。！？、；：""''（）《》【】])', r'\1\2', text)
    text = re.sub(r'([，。！？、；：""''（）《》【】])\s+([一-鿿])', r'\1\2', text)
    # 3. 折行：把段落内部的硬换行合并（只保留段落分隔）
    text = re.sub(r'([一-鿿，、])\n([一-鿿])', r'\1\2', text)
    # 4. 多余空行压缩
    text = re.sub(r'\n{3,}', '\n\n', text)
    # 5. 行内多余空格
    text = re.sub(r' {2,}', ' ', text)
    return text.strip()


def ocr_image(image_path: str, tessdata_prefix: str, timeout: int = 60) -> str:
    """对单张图片跑 tesseract chi_sim。"""
    env = os.environ.copy()
    env['TESSDATA_PREFIX'] = tessdata_prefix
    try:
        r = subprocess.run(
            ['tesseract', image_path, '-', '-l', 'chi_sim',
             '--psm', '3', '--oem', '1'],
            capture_output=True, text=True, env=env, timeout=timeout
        )
        return r.stdout
    except subprocess.TimeoutExpired:
        return f"[OCR TIMEOUT for {image_path}]"
    except Exception as e:
        return f"[OCR ERROR: {e}]"


def ocr_pdf(pdf_path: str, output_path: str, dpi: int, start: int, end: int,
            tessdata_prefix: str, log_path: str):
    """扫描 PDF → 逐页转图 → OCR → 合并文本。"""
    from pdf2image import convert_from_path, pdfinfo_from_path

    info = pdfinfo_from_path(pdf_path)
    total_pages = info['Pages']
    end = end if end > 0 else total_pages
    end = min(end, total_pages)

    log = {'source': pdf_path, 'total_pages': total_pages,
           'processing': f'{start}-{end}', 'dpi': dpi, 'started': time.time(),
           'pages_done': 0, 'pages_failed': []}

    print(f"[ocr_pdf] {os.path.basename(pdf_path)}: pages {start}-{end} / {total_pages}, dpi={dpi}")
    sys.stdout.flush()

    all_text = []
    BATCH = 10  # 每批 10 页处理，避免一次性内存爆炸
    for batch_start in range(start, end + 1, BATCH):
        batch_end = min(batch_start + BATCH - 1, end)
        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                images = convert_from_path(
                    pdf_path, dpi=dpi,
                    first_page=batch_start, last_page=batch_end,
                    output_folder=tmpdir, paths_only=True, fmt='png'
                )
            except Exception as e:
                print(f"  [page {batch_start}-{batch_end}] convert FAIL: {e}")
                log['pages_failed'].extend(range(batch_start, batch_end + 1))
                continue
            for i, img in enumerate(images):
                page_no = batch_start + i
                txt = ocr_image(img, tessdata_prefix, timeout=120)
                cleaned = clean_chinese_ocr(txt)
                if cleaned.strip():
                    all_text.append(f"\n\n=== Page {page_no} ===\n\n{cleaned}")
                    log['pages_done'] += 1
                else:
                    log['pages_failed'].append(page_no)
        # 每批写一次磁盘+日志，断点可恢复
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(''.join(all_text))
        log['elapsed_s'] = round(time.time() - log['started'], 1)
        with open(log_path, 'w', encoding='utf-8') as f:
            json.dump(log, f, indent=2, ensure_ascii=False)
        print(f"  [batch {batch_start}-{batch_end}] done. total pages OK: {log['pages_done']}, failed: {len(log['pages_failed'])}, {log['elapsed_s']}s")
        sys.stdout.flush()

    log['finished'] = time.time()
    log['elapsed_s'] = round(log['finished'] - log['started'], 1)
    log['output_chars'] = sum(len(t) for t in all_text)
    with open(log_path, 'w', encoding='utf-8') as f:
        json.dump(log, f, indent=2, ensure_ascii=False)
    print(f"[ocr_pdf] DONE {os.path.basename(pdf_path)}: {log['output_chars']:,} chars in {log['elapsed_s']}s")
    return log


def ocr_epub_images(epub_path: str, output_path: str, tessdata_prefix: str, log_path: str):
    """图像型 EPUB → 抽图 → OCR → 合并。"""
    log = {'source': epub_path, 'started': time.time(), 'images_done': 0, 'images_failed': []}
    print(f"[ocr_epub] {os.path.basename(epub_path)}")
    sys.stdout.flush()
    all_text = []
    with zipfile.ZipFile(epub_path) as z:
        images = sorted([n for n in z.namelist()
                        if n.lower().endswith(('.jpg', '.jpeg', '.png'))
                        and z.getinfo(n).file_size > 50000])  # 跳过封面小图
        log['total_images'] = len(images)
        print(f"  images: {len(images)} (skipping <50KB covers)")
        with tempfile.TemporaryDirectory() as tmpdir:
            for i, name in enumerate(images):
                img_path = os.path.join(tmpdir, f'p{i:04d}.jpg')
                with open(img_path, 'wb') as f:
                    f.write(z.read(name))
                txt = ocr_image(img_path, tessdata_prefix, timeout=120)
                cleaned = clean_chinese_ocr(txt)
                if cleaned.strip():
                    all_text.append(f"\n\n=== Page {i+1} ({os.path.basename(name)}) ===\n\n{cleaned}")
                    log['images_done'] += 1
                else:
                    log['images_failed'].append(name)
                if (i + 1) % 20 == 0:
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(''.join(all_text))
                    log['elapsed_s'] = round(time.time() - log['started'], 1)
                    with open(log_path, 'w', encoding='utf-8') as f:
                        json.dump(log, f, indent=2, ensure_ascii=False)
                    print(f"  page {i+1}/{len(images)}, {log['elapsed_s']}s")
                    sys.stdout.flush()
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(''.join(all_text))
    log['finished'] = time.time()
    log['elapsed_s'] = round(log['finished'] - log['started'], 1)
    log['output_chars'] = sum(len(t) for t in all_text)
    with open(log_path, 'w', encoding='utf-8') as f:
        json.dump(log, f, indent=2, ensure_ascii=False)
    print(f"[ocr_epub] DONE: {log['output_chars']:,} chars in {log['elapsed_s']}s")
    return log


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('input', help='输入 PDF 或 EPUB 文件')
    ap.add_argument('output', help='输出 txt 路径')
    ap.add_argument('--dpi', type=int, default=200)
    ap.add_argument('--start', type=int, default=1)
    ap.add_argument('--end', type=int, default=0, help='0 = 到最后一页')
    ap.add_argument('--tessdata', default=os.environ.get('TESSDATA_PREFIX', os.path.expanduser('~/tessdata')))
    args = ap.parse_args()

    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
    log_path = args.output + '.log.json'

    if args.input.lower().endswith('.pdf'):
        ocr_pdf(args.input, args.output, args.dpi, args.start, args.end, args.tessdata, log_path)
    elif args.input.lower().endswith('.epub'):
        ocr_epub_images(args.input, args.output, args.tessdata, log_path)
    else:
        sys.exit(f"Unsupported file type: {args.input}")


if __name__ == '__main__':
    main()
 == '__main__':
    main()
