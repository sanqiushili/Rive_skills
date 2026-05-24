# Rive Skills

[![Install with Skills](https://skills.sh/b/sanqiushili/Rive_skills)](https://skills.sh/sanqiushili/Rive_skills)

[English](README.md)

> 本 Skills 来自 [RiveCN](https://rivecn.com)。

**当前版本：** `rive-script-builder v2.0.0`

这个仓库用于发布可复用的 Rive 相关技能。  
当前只有一个技能：`rive-script-builder`。

## 仓库结构

```text
.
├─ skills/
│  └─ rive-script-builder/
│     ├─ SKILL.md
│     ├─ agents/openai.yaml
│     ├─ docs/
│     ├─ references/
│     └─ scripts/
└─ .github/workflows/   # 可选的 CI/发布工作流
```

## rive-script-builder

`rive-script-builder` 是一个跨 Agent 的 Rive Luau 脚本技能。只有在需求不明确或风险较高时，才采用先澄清再实现的流程。

## 协议覆盖

- Node
- Layout
- Converter
- Path Effect
- Transition Condition
- Listener Action
- Util
- Test

## 主要特性

- 需求清楚时可直接输出代码。
- 仅在需要澄清或做高风险决策时才给出待实现计划。
- 默认优先通过 Context7 MCP 查询官方文档（`/rive-app/rive-docs`）。
- MCP 不可用时，自动回退到本地 docs/references 与同步脚本链路。
- 附带挂载指引、调试清单和测试建议。

## 推荐前置（可选）

建议在使用本 skill 前先安装并配置 Context7 MCP（非必须）。

- 本地 MCP 服务命令：
  ```bash
  npx -y @upstash/context7-mcp --api-key YOUR_API_KEY
  ```
- 远程 MCP 地址：
  ```text
  https://mcp.context7.com/mcp
  ```
- 官方安装文档：[Context7 Installation](https://context7.com/docs/installation)

## 安装

按 skills.sh 常见方式，从 GitHub 仓库安装：

```bash
npx skills add https://github.com/sanqiushili/Rive_skills --skill rive-script-builder
```

如果该 skill 已被 Skills 索引，也可以使用：

```bash
npx skills add https://github.com/sanqiushili/Rive_skills@rive-script-builder
```

参考：[Skills CLI](https://skills.sh/docs/cli)

## 使用

1. 在对话中触发：`Use rive-script-builder`
2. 描述目标效果和协议上下文
3. 如有需要，查看澄清问题和待实现计划
4. 需求清楚时可直接获得最终 Luau 代码与挂载步骤

## MCP 查询（默认）

技能默认会通过 Context7 MCP 查询 Rive 文档：

```text
resolve-library-id -> /rive-app/rive-docs
query-docs(libraryId="/rive-app/rive-docs", query="<你的 API/协议问题>")
```

如果 MCP 不可用，会回退到本地/同步脚本，例如：

```bash
python3 skills/rive-script-builder/scripts/sync_rive_docs.py search --source auto --query "PathEffect"
```

## 示例请求

- “帮我写一个蜡笔粗糙边缘的 Path Effect 脚本。”
- “重构这个 Rive Converter，并补上 reverseConvert。”
- “排查我的 Transition Condition 闪烁问题。”

## 维护者

- 作者：`三秋十李 Sergio`
- 发布方：`RiveCN.com`
- 网站：`https://RiveCN.com`

## 许可证

`skills/rive-script-builder` 使用 CC BY 4.0 许可证，使用和改编时必须署名。见 `LICENSE`。
