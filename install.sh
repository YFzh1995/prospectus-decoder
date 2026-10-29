#!/usr/bin/env bash
# 观星哥·拆公司：完整本地发布包的便捷入口。
set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
if [ ! -f "${SCRIPT_DIR}/scripts/install_skill.py" ]; then
  echo '请解压完整发布包后执行；单独下载或管道运行本文件不能安装配套资源。' >&2
  exit 1
fi
if command -v python3 >/dev/null 2>&1; then
  exec python3 "${SCRIPT_DIR}/scripts/install_skill.py" "$@"
fi
echo '需要Python 3。Windows可使用 py -3 scripts/install_skill.py；WorkBuddy首选上传专用ZIP包。' >&2
exit 1
