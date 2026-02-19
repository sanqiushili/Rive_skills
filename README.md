# Rive Skills

这个仓库用于发布 Rive 相关技能（Skills）。  
当前只有一个技能：`rive-script-builder`。

## 仓库结构

```text
.
├─ skills/
│  └─ rive-script-builder/
│     ├─ SKILL.md
│     ├─ README.md
│     ├─ package.json
│     ├─ agents/openai.yaml
│     ├─ references/
│     └─ scripts/
└─ .github/workflows/   # CI / 发布工作流（可选）
```

## rive-script-builder

`rive-script-builder` 是一个跨 Agent 的 Rive Luau 脚本技能，采用“先澄清、后实现、需明确批准”的工作流。

## 支持范围

- Node
- Layout
- Converter
- Path Effect
- Transition Condition
- Listener Action
- Util
- Test

## 特性

- 明确批准前不输出最终脚本代码。
- 优先使用离线参考资料，可选同步官方实时文档。
- 提供编辑器挂载指引、调试清单和测试建议。

## 安装

```bash
npx skills add rive-script-builder-skill
```

或者使用你的 Agent 运行时支持的 GitHub 目录安装方式。

## 使用流程

1. 在对话中触发：`Use rive-script-builder`
2. 描述目标效果和协议上下文
3. 查看技能给出的澄清问题和待实现计划
4. 明确批准后，输出最终 Luau 代码与接线步骤

## 示例请求

- “帮我写一个蜡笔粗糙边缘的 Path Effect 脚本。”
- “重构这个 Rive Converter，并补上 reverseConvert。”
- “排查我的 Transition Condition 闪烁问题。”


## 维护者

- 作者：`三秋十李 Sergio`
- 发布方：`RiveCN.com`
- 网站：`https://RiveCN.com`

## 许可证

`skills/rive-script-builder` 使用 MIT 许可证，见 `LICENSE`。
