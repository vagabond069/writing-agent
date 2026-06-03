# Writing Start Prompt

本文件**只放启动模板**。所有规则、流程、决策都在其它文件，本文件不重复。

复制下面任一模板给 agent，替换花括号中的内容即可启动一次任务。

---

## 通用模板

```md
请按当前项目中的 writing-agent 流程处理这次写作任务。

任务类型：{experimental / formal / revision}
输入文件：{例如：灵感碎片001.md，或对话中提供的新碎片}
主题目标：{你想写什么，或你想逼近什么问题}
输出目标：{大纲 / 初稿 / 改稿 / 完整流程}
风格要求：{无 / 指定风格卡名称}
版本要求：{试验版 / 正式版}

执行依据：
- 边界规则：CLAUDE.md
- 角色与决策：agent/writing-agent.md
- 流程步骤：agent/workflow-writing.md
- 事实回顾模板：agent/fact-check-template.md
- 风格调用（如需要）：.claude/skills/style-application/SKILL.md
- 风格蒸馏（如需要）：.claude/skills/huashu-nuwa/SKILL.md
```

---

## 试验版

适用于流程试跑、风格测试、灵感快速扩写。

```md
请按当前项目中的 writing-agent 流程处理这次写作任务。

任务类型：experimental
输入文件：灵感碎片001.md
主题目标：从碎片中提炼最值得展开的问题，并完成一轮试验版成文
输出目标：完整流程（方向 → 大纲 → 初稿 → 改稿 → 事实回顾）
风格要求：调用 style-application，优先使用实验版风格卡
版本要求：试验版

执行依据见 agent/writing-start-prompt.md 通用模板。
风格卡优先读取：.claude/styles/dai-jinhua/style-card.experimental.md
所有产物写入：runs/experimental/{主题}/
```

---

## 正式版

适用于进入正式生产、已认可方向的任务。

```md
请按当前项目中的 writing-agent 流程处理这次正式写作任务。

任务类型：formal
输入文件：{文件名}
主题目标：{主题}
输出目标：完整流程
风格要求：{无 / 指定风格卡}
版本要求：正式版

执行依据见 agent/writing-start-prompt.md 通用模板。
所有产物写入：runs/formal/{主题}/

前置确认：方向已定 / 大纲已定 / 已有至少一轮改稿计划 / fact-check 将真实完成。
```

---

## 改稿

适用于已有草稿做定向修改。

```md
请按当前项目中的 writing-agent 流程处理这次改稿任务。

任务类型：revision
输入文件：{草稿文件路径}
主题目标：在保留原意的基础上完成定向改稿
输出目标：改稿 + 事实回顾更新
风格要求：{无 / 指定风格卡}
版本要求：{试验版 / 正式版}

改稿优先级：结构 → 逻辑 → 重复 → 字词。
若改动会明显偏离原稿方向，先停下说明。
若原稿中有未核验的高风险事实，同步更新 fact-check.md。
```

---

## 风格蒸馏

适用于新增某位作者的风格资产。

```md
请按当前项目中的女娲蒸馏流程处理这次风格资产任务。

任务类型：style-distillation
蒸馏对象：{作者 / 学者 / 评论家}
本地语料位置：inputs/distillation-sources/{名称}/
输出目标：完整 persona + 写作可调用的轻量风格卡
版本要求：{实验版 / 正式版}

执行依据：
- .claude/skills/huashu-nuwa/SKILL.md
- 完整 persona → .claude/personas/{名称}-perspective/
- 轻量风格卡 → .claude/styles/{名称}/style-card.md
- 试验版风格卡 → .claude/styles/{名称}/style-card.experimental.md
- 调研中间产物 → experiments/{实验名}/
- 不修改 .claude/skills/huashu-nuwa/ 中的原件
```

---

## 当前推荐用法

只想稳定启动项目时用这条：

```md
请按当前项目中的 writing-agent 流程处理这次写作任务。

任务类型：experimental
输入文件：灵感碎片001.md
输出目标：完整流程
风格要求：调用 style-application，优先使用 .claude/styles/dai-jinhua/style-card.experimental.md
版本要求：试验版

请先读取：
- CLAUDE.md
- agent/writing-agent.md
- agent/workflow-writing.md
- .claude/skills/style-application/SKILL.md
- .claude/styles/dai-jinhua/style-card.experimental.md

然后完成方向提炼 → 大纲 → 初稿 → 改稿 → 事实回顾，
正文与事实回顾写入 runs/experimental/{主题}/。
```

---

## 使用提醒

- 不指定风格 → 不要主动调用风格卡。
- 用试验版风格卡 → 输出落到 `runs/experimental/`。
- 涉及真实案件 / 人物 / 争议事件 → 同步生成 `fact-check.md`。
- 只是测试 → 不要写入正式版目录。
