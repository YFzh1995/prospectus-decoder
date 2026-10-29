# 跨平台安装与运行

核心标识为gxg-company-decoder，展示名为“观星哥·拆公司”。旧prospectus-decoder名称仅用于识别迁移来源，不承诺自动调用别名。

## WorkBuddy（主要分发场景）

使用build_packages.py生成的workbuddy.zip。在技能板块选择“添加技能→上传技能”，导入完整ZIP。专用包的SKILL.md包含name、display_name/display_name_en、description及中英文简介、示例、version、author，分析正文与通用内核相同。

“试试这样用”：用观星哥·拆公司分析Iambic，先让我选择分析深度。

平台目录因客户端/分发方式不同，不猜测路径。若明确知道本地路径，可用Python安装脚本的--target。ZIP导入、名称触发、联网、脚本、HTML交付须在实际WorkBuddy中验收；本地打包和结构检查不等于实机验证。

官方依据（核对2026-10-29）：https://open.workbuddy.cn/docs/skill 和 https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market 。市场提交还需遵循该市场当前字段和审核规则。

## Codex

使用codex.zip；完整解压后运行python3 scripts/install_skill.py --platform codex。agents/openai.yaml配置中文展示名，显式调用示例：$gxg-company-decoder。安装后刷新/重新加载技能列表，当前对话已注入的旧目录不会被脚本追溯改写。

## 其他平台

通用ZIP保留标准SKILL.md和所有必要配套资源。可显式选择claude-code、cursor、opencode、agents，或用--target指定最终技能目录。Windows可用py -3代替python3，具体目录和调用选择器以实际平台为准。不同平台的自动触发和显示能力需分别验收。

## 更新与迁移

解压新发布包后执行相同安装命令，可加--update表示本地更新。它从当前完整包重新部署，备份既有目标，且不进行git pull。旧prospectus-decoder目录在识别为本技能后移到技能扫描目录之外的备份目录，避免两份生效。使用--backup-root可指定备份位置。安装器不会修改其他Skill。

## 执行能力与依赖

联网检索与文件下载由当前Agent可用工具承担。HTML渲染需要Python 3和markdown-it-py；可先运行python3 scripts/install_skill.py --check。缺依赖时在独立虚拟环境安装，不覆盖系统环境。PDF优先pdftotext，回退可用提取工具；扫描件按实际OCR能力处理。全部路径相对Skill目录或运行目录，Python脚本不依赖macOS固定路径。

核心流程要求保留来源、原件、文本及计算；当前平台权限或网络不足时记录实际取得范围。接受公司名的入口不意味着每家公司都有公开可下载的正式披露。
