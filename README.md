# Prospectus Decoder（招股书商业模式解码器）

> 不是"招股书摘要器"。是"商业模式翻译官"。

招股书会写"提供智能化整体解决方案"——本 Skill 会告诉你：这是一家卖铲子的设备公司，客户是电池厂，最大的风险是下游客户扩产放缓。

---

## 快速开始

```bash
# 一键安装
curl -fsSL https://raw.githubusercontent.com/YFzh1995/prospectus-decoder/main/install.sh | bash
```

安装后在 AI 对话中输入：

```
@prospectus-decoder /path/to/prospectus.pdf
```

---

## 功能特性

- **三层架构**：事实抽取 → 合并去重 → 推理写作，Token 成本节省 60-80%
- **三种输出深度**：Level 1（30秒·500字）/ Level 2（3分钟·2500字）/ Level 3（30分钟·8000字）
- **8步商业推理**：分类 → 痛点 → 价值 → 赚钱 → 产业链 → 竞争 → 风险机会 → 行业视角
- **匿名实体识别**：自动推断招股书中脱敏的竞争对手/客户/供应商真实身份
- **定语剥离**：剥离招股书中为美化排名而添加的限定词，还原真实行业位置
- **推理观点标注**：明确区分招股书原文陈述与 AI 推理判断

---

## 安装部署

### 一键安装

```bash
curl -fsSL https://raw.githubusercontent.com/YFzh1995/prospectus-decoder/main/install.sh | bash
```

自动检测平台（opencode / codex / claude-code / cursor）并安装到对应目录。

### 降级安装（手动）

| 平台 | Skills 目录 |
|------|------------|
| opencode | `~/.config/opencode/skills/prospectus-decoder/` |
| codex | `~/.codex/skills/prospectus-decoder/` |
| claude-code | `~/.claude/skills/prospectus-decoder/` |
| cursor | `~/.cursor/skills/prospectus-decoder/` |
| 通用 | 任意目录，使用时指定完整路径 |

---

## 使用示例

```bash
# 交互式选择报告深度
@prospectus-decoder /path/to/prospectus.pdf

# 直接指定深度
@prospectus-decoder /path/to/prospectus.pdf --level 1  # 30秒读懂
@prospectus-decoder /path/to/prospectus.pdf --level 2  # 3分钟读懂
@prospectus-decoder /path/to/prospectus.pdf --level 3  # 30分钟深度研究

# 查看版本
@prospectus-decoder --version
```

---

## 报告结构（Level 2 示例）

1. 一句话讲清公司
2. 产品和服务
3. 客户是谁
4. 为什么客户付钱
5. 产业链位置
6. 赚钱逻辑
7. 竞争格局
8. 核心风险
9. 核心机会
10. 大白话解释
11. 行业视角（定语剥离）
12. 信息来源

---

## 跨平台兼容

- 所有 Prompt 文件为纯文本 Markdown，无框架依赖
- PDF 提取三层回退：pdftotext → PyMuPDF → pdfplumber
- 不依赖任何付费 API 或闭源工具链

---

## 版本与更新

版本号格式：`v<MAJOR>.<MINOR>.<PATCH>`（语义化版本）。

Skill 启动时会自动检查远程版本，有新版本将提示更新：

```bash
cd ~/.config/opencode/skills/prospectus-decoder/
git pull origin main
# 或重新运行安装脚本
curl -fsSL https://raw.githubusercontent.com/YFzh1995/prospectus-decoder/main/install.sh | bash
```

---

## 作者

**观星哥**

- 小红书：观星哥
- 微信：guanxingge2025
- GitHub：[YFzh1995](https://github.com/YFzh1995)

---

## License

MIT License
