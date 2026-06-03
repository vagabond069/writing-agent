# Phase 0 / 0.5 Setup

## 任务定义

- 蒸馏对象：戴锦华。
- 实验类型：完整女娲六 Agent 并行调研实验。
- 运行环境：Codex 项目内，通过 `.agents/skills/nuwa-distillation/SKILL.md` 适配原版女娲。
- 输出位置：`experiments/nuwa-full-dai-jinhua/`。

## 路径映射

原版女娲中的 `.claude/skills/[person-name]-perspective/` 在本实验中映射为：

`experiments/nuwa-full-dai-jinhua/persona/`

正式项目中的潜在迁移目标为：

`.agents/personas/dai-jinhua-redistill-perspective/`

但本次实验不会自动写入正式目录。

## 本地语料模式

用户已提供本地素材，因此采用“本地语料优先”：

1. 先读取 `sources/` 和 `extracted-text/`。
2. 对缺失维度使用公开网页补充基本事实与近期动态。
3. 所有推断必须标注依据与边界。

## 六路调研分配

- Agent 1：`01-writings.md`
- Agent 2：`02-conversations.md`
- Agent 3：`03-expression-dna.md`
- Agent 4：`04-external-views.md`
- Agent 5：`05-decisions.md`
- Agent 6：`06-timeline.md`
