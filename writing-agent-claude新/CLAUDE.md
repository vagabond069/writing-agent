# CLAUDE.md

本文件只负责**不变的边界**：硬性规则、触发判定、目录约定、命名约定。

具体怎么做事不在本文件展开：

- 角色定义、决策点、停顿与回退 → `agent/writing-agent.md`
- 标准写作流程（阶段顺序、每阶段产出） → `agent/workflow-writing.md`
- 启动模板 → `agent/writing-start-prompt.md`
- 事实回顾模板 → `agent/fact-check-template.md`
- 风格调用细则 → `.claude/skills/style-application/SKILL.md`
- 风格蒸馏细则 → `.claude/skills/huashu-nuwa/SKILL.md`

---

## 项目目标

把用户提供的思维碎片、瞬时灵感、片段笔记和零散材料，整理为结构清楚、表达有力、风格鲜明灵活、事实审慎的中文文章。

本项目包含两条链路：

1. **写作链路**：碎片 → 方向 → 大纲 → 初稿 → 改稿 → 事实回顾。
2. **蒸馏链路**：原始语料 → 女娲调研 → 完整 persona → 轻量风格卡 → 写作链路调用。

两条链路解耦运行：先把风格资产沉淀好，再让写作链路按需调用。

---

## 硬性规则（不可越线）

所有写作任务必须遵守：

1. 不得编造事实。
2. 不得伪造引文、来源、书名、片名、人名、年份、事件或数据。
3. 不得把推测、联想、印象写成已确认的事实。
4. 信息不足时，应明确说明"不确定""需要核验"或"这是推断"，不能擅自补全。
5. 若某一事实无法确认但影响判断，应降调表达（"可能是""可以看作""某种程度上"），不强行下结论。
6. 正文中无法及时核验但又不宜删除的内容，必须明确标记其风险状态。
7. 初稿或改稿完成后，必须生成 `fact-check.md`；未完成核验不得把相关表述包装成已确定结论。
8. 默认输出为中文。

---

## 触发判定

Agent 根据用户输入判断进入哪条链路：

**进入标准写作流程**（默认）
- 用户提供碎片、草稿、主题说明
- 用户要求生成大纲 / 初稿 / 改稿 / 事实回顾
- 入口：`agent/workflow-writing.md`

**叠加风格调用**
- 用户明确指定某位作者、学者、评论家或某种写作气质
- 用户使用"靠近""参考""借鉴""模仿""沿用某种笔法"等措辞
- 用户描述了足够明确的气质且项目中存在相近风格卡
- 入口：`.claude/skills/style-application/SKILL.md`
- 不触发：用户没有明确提出风格要求；项目中没有对应风格卡且无法合理近似匹配

**进入风格蒸馏流程**
- 用户要求"蒸馏 XX""做 XX 视角""新增 XX 风格卡""女娲 XX"
- 用户提出模糊的认知需求且需要先定位人物
- 入口：`.claude/skills/huashu-nuwa/SKILL.md`
- 蒸馏完成后回到写作链路，不直接由蒸馏替代写作

**禁止伪造风格**
- 用户指定的风格在项目中没有对应风格卡时，必须明确说明缺失，不得自行伪造"像某某"的写法
- 用户若要求新增，转入蒸馏流程；用户若不要求新增，退回默认中文写作风格

---

## 目录约定

```
Writing-Agent-Claude/
├── CLAUDE.md                       # 本文件：硬规则与触发判定
├── README-agent.md                 # 项目导航
├── agent/                          # 写作 agent 的角色、流程、模板
├── inputs/
│   ├── fragments/                  # 写作灵感碎片（写作链路入口）
│   └── distillation-sources/       # 蒸馏一手语料（蒸馏链路入口）
│       └── {name}/                 # 按蒸馏对象分组
│           ├── books/
│           ├── articles/
│           ├── interviews/
│           ├── lectures/
│           ├── media/
│           └── notes/
├── runs/
│   ├── experimental/{主题}/        # 写作试验版产物
│   └── formal/{主题}/              # 写作正式版产物
├── experiments/                    # 蒸馏链路的实验目录
│   └── {实验名}/                   # 调研、抽取、persona 草稿、写作测试
└── .claude/
    ├── skills/
    │   ├── huashu-nuwa/            # 女娲上游 skill 原件（不修改）
    │   └── style-application/      # 通用风格调用 skill
    ├── personas/{name}-perspective/# 蒸馏出的完整人物视角
    └── styles/{name}/              # 写作时调用的轻量风格卡
```

分工原则：

- 碎片不覆盖草稿，草稿不替代 fact-check，风格说明不写进正文文件。
- 原始素材（PDF/EPUB/transcript 等）放 `inputs/distillation-sources/`，不要绑死在某一次实验目录里。
- 实验目录只放本次实验的中间产物（抽取文本、调研日志、persona 草稿、写作测试）。
- 蒸馏完成的成品才进入 `.claude/personas/` 和 `.claude/styles/`，未定稿不混入。
- 女娲原件、persona、style card 三者保持分工，不混放。

---

## 文件命名约定

```
runs/{experimental|formal}/{主题}/outline.md
runs/{experimental|formal}/{主题}/draft-v1.md
runs/{experimental|formal}/{主题}/draft-v2.md
runs/{experimental|formal}/{主题}/fact-check.md

.claude/personas/{名称}-perspective/SKILL.md
.claude/styles/{名称}/style-card.md
.claude/styles/{名称}/style-card.experimental.md

inputs/distillation-sources/{名称}/{books|articles|interviews|lectures|media|notes}/
```

主题名过长可用简短中文或拼音缩写，同一主题下保持命名一致。
