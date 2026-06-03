# Nuwa Full Dai Jinhua Experiment

## 实验目标

完整实验女娲 skill 在本项目下的适配与运行能力。

目标链路：

`原始语料 → 分类入库 → 六路并行调研 → 调研 review → 框架提炼 → persona → style card → 写作测试 → fact-check → closure report`

## 输入语料

原始语料统一存放在仓库根目录的：

`inputs/distillation-sources/dai-jinhua/`

按 `books/ articles/ interviews/ lectures/ media/ notes/` 分类。

本实验不在自己目录下保存原始 PDF/EPUB，避免多实验之间重复存储和版本漂移。

## 隔离原则

本实验完全独立，不直接写入正式资产目录：

- 不写入 `.claude/personas/`
- 不写入 `.claude/styles/`
- 不写入 `runs/`

若实验结果被认可，人工迁移到正式目录。

## 目录结构

- `extracted-text/`：从 PDF、EPUB、MOBI、TXT 中抽取出的纯文本。
- `persona/references/research/`：六路调研结果。
- `persona/SKILL.md`：实验版完整 persona。
- `style-card/style-card.experimental.md`：实验版轻量风格卡。
- `writing-test/`：写作测试和事实回顾。
- `logs/`：抽取日志、阶段报告、质量检查。

## 当前模式

- 模式：本地语料优先。
- 补充：必要时使用公开网页来源核验基本事实与近期动态。
- 状态：实验版，不作为正式戴锦华风格资产。
