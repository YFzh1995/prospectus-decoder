#!/bin/bash
# Prospectus Decoder — 一键安装脚本
# 支持平台：opencode / codex / claude-code / cursor / 通用
# 作者：观星哥 | 微信：guanxingge2025
# 仓库：https://github.com/YFzh1995/prospectus-decoder

set -e

SKILL_NAME="prospectus-decoder"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# === 检测平台 ===
detect_platform() {
    if [ -d "$HOME/.config/opencode/skills" ]; then
        echo "opencode"
    elif [ -d "$HOME/.codex/skills" ]; then
        echo "codex"
    elif [ -d "$HOME/.claude/skills" ]; then
        echo "claude-code"
    elif [ -d "$HOME/.cursor/skills" ]; then
        echo "cursor"
    else
        echo "generic"
    fi
}

PLATFORM=$(detect_platform)

case "$PLATFORM" in
    opencode)
        TARGET_DIR="$HOME/.config/opencode/skills/${SKILL_NAME}"
        ;;
    codex)
        TARGET_DIR="$HOME/.codex/skills/${SKILL_NAME}"
        ;;
    claude-code)
        TARGET_DIR="$HOME/.claude/skills/${SKILL_NAME}"
        ;;
    cursor)
        TARGET_DIR="$HOME/.cursor/skills/${SKILL_NAME}"
        ;;
    *)
        TARGET_DIR="$HOME/.prospectus-decoder"
        echo "⚠️  未检测到已知平台，安装到通用目录：${TARGET_DIR}"
        echo "   如需手动注册，请将目录路径加入平台 skills 配置。"
        ;;
esac

echo "📦 Prospectus Decoder v$(cat "${SCRIPT_DIR}/VERSION")"
echo "📍 安装目标：${TARGET_DIR}"
echo "🖥️  检测平台：${PLATFORM}"

# === 安装文件 ===
mkdir -p "${TARGET_DIR}"

# 复制核心文件
cp -r "${SCRIPT_DIR}/SKILL.md" "${TARGET_DIR}/"
cp -r "${SCRIPT_DIR}/VERSION" "${TARGET_DIR}/"
cp -r "${SCRIPT_DIR}/prompts" "${TARGET_DIR}/" 2>/dev/null || true
cp -r "${SCRIPT_DIR}/templates" "${TARGET_DIR}/" 2>/dev/null || true
cp -r "${SCRIPT_DIR}/outputs" "${TARGET_DIR}/" 2>/dev/null || true
cp -r "${SCRIPT_DIR}/install.sh" "${TARGET_DIR}/" 2>/dev/null || true

echo ""
echo "✅ 安装完成！"
echo ""
echo "使用方法："
echo "  @prospectus-decoder /path/to/prospectus.pdf"
echo "  @prospectus-decoder /path/to/prospectus.pdf --level 2"
echo "  @prospectus-decoder --version  # 查看版本"
echo ""
echo "📖 更多帮助：输入 @prospectus-decoder --help"

# === 降级安装提示 ===
if [ "$PLATFORM" = "generic" ]; then
    echo ""
    echo "⚠️  降级安装（通用目录）注意事项："
    echo "  - Skill 未自动注册到任何 AI 平台"
    echo "  - 请手动将 ${TARGET_DIR} 添加到平台的 skills 路径配置"
    echo "  - 或使用绝对路径引用：@${TARGET_DIR}/SKILL.md /path/to/prospectus.pdf"
fi
