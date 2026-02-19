# rive-script-builder

[English README](README.md)

`rive-script-builder` 是一个跨 Agent 的 Rive Luau 脚本技能，采用“先澄清、后实现、需明确批准”的工作流。

## 特性

- 覆盖 Node、Layout、Converter、Path Effect、Transition Condition、Listener Action、Util、Test 协议。
- 内置“明确批准”闸门，避免在需求不清时直接产出脚本。
- 离线参考资料优先，可选实时同步官方文档。
- 提供编辑器挂载指引、调试与测试清单。

## 安装

从 npm skill 包安装：

```bash
npx skills add rive-script-builder-skill
```

或者使用你的 Agent 运行时支持的 GitHub skill 目录安装方式。

## 3 行快速开始

```text
1) 执行：npx skills add rive-script-builder-skill
2) 对话里输入："Use rive-script-builder"
3) 提需求："帮我写一个蜡笔粗糙边缘的 Path Effect 脚本"
```

## 使用

在提示词中触发 `rive-script-builder`，然后按澄清与批准流程执行。

示例请求：

- “帮我写一个蜡笔粗糙边缘的 Path Effect 脚本。”
- “重构这个 Rive Converter，并补上 reverseConvert。”
- “排查我的 Transition Condition 闪烁问题。”

可选：同步最新 Rive 文档

```bash
python3 scripts/sync_rive_docs.py sync
python3 scripts/sync_rive_docs.py search --query "PathEffect"
```

## 维护者

- 作者：`三秋十李 Sergio`
- 发布方：`RiveCN.com`
- 网站：`https://RiveCN.com`

## 许可证

MIT，见 [LICENSE](LICENSE)。
