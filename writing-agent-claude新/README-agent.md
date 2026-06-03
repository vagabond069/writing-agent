# Writing Agent Project

把零散灵感、片段笔记、问题意识，转化为结构清楚、风格鲜明、事实审慎的中文长文。

项目分**两条独立链路**：

1. **写作链路**：`inputs/fragments/` → 方向 → 大纲 → 初稿 → 改稿 → `runs/{experimental|formal}/{主题}/fact-check.md`
2. **蒸馏链路**：`inputs/distillation-sources/{name}/` → 女娲调研 → `.claude/personas/{name}-perspective/` → `.claude/styles/{name}/` → 写作链路按需调用

---

## 文档分工（MECE）

| 文件 | 只负责 |
|---|---|
| `CLAUDE.md` | 不变的边界：硬规则、触发判定、目录与命名约定 |
| `agent/writing-agent.md` | 角色与决策：默认推进点、停顿点、版本规则、回退规则 |
| `agent/workflow-writing.md` | 流程唯一权威：8 阶段，每阶段目标/输入/产出/注意事项 |
| `agent/writing-start-prompt.md` | 启动模板：用户复制即用 |
| `agent/fact-check-template.md` | 事实回顾文件模板 |
| `.claude/skills/style-application/SKILL.md` | 风格调用的统一逻辑 |
| `.claude/skills/huashu-nuwa/SKILL.md` | 风格蒸馏（女娲原件） |

更新规则在哪改：

- 改硬规则 / 目录命名 → `CLAUDE.md`
- 改"什么时候停下、什么时候默认推进" → `agent/writing-agent.md`
- 改流程步骤 → `agent/workflow-writing.md`
- 改启动方式 → `agent/writing-start-prompt.md`

---

## 启动方式

启动一次写作 / 改稿 / 蒸馏任务，直接复制 `agent/writing-start-prompt.md` 中对应模板即可。

第一次使用建议：

1. 读 `CLAUDE.md`（边界与目录）
2. 读 `agent/writing-agent.md`（决策点）
3. 读 `agent/workflow-writing.md`（流程）
4. 从 `agent/writing-start-prompt.md` 复制模板开始

---

## 顶层目录速查

```
CLAUDE.md                            # 边界与触发
README-agent.md                      # 本文件
agent/                               # 角色、流程、模板
inputs/fragments/                    # 写作碎片
inputs/distillation-sources/{name}/  # 女娲一手语料
runs/experimental/{主题}/            # 写作试验版
runs/formal/{主题}/                  # 写作正式版
experiments/{实验名}/                # 蒸馏实验目录
.claude/skills/                      # 项目 skill
.claude/personas/{name}-perspective/ # 完整 persona
.claude/styles/{name}/               # 轻量风格卡
```

详细目录约定见 `CLAUDE.md` 「目录约定」。
