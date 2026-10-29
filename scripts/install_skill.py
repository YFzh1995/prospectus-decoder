#!/usr/bin/env python3
"""Install/update from a complete local release; standard library, no network.

WorkBuddy: prefer GUI ZIP upload. An explicit --target supports known local paths.
"""
import argparse
from datetime import datetime
from pathlib import Path
import importlib.util
import shutil
import sys
from tempfile import mkdtemp

NAME='gxg-company-decoder'
LEGACY='prospectus-decoder'
ROOT=Path(__file__).resolve().parents[1]
RESOURCES=['SKILL.md','VERSION','README.md','prompts','references','templates','scripts']
OPTIONAL=['agents','tests','install.sh']

def install(source, target, backup_root=None):
    source,target=Path(source).resolve(),Path(target).expanduser().resolve()
    for item in RESOURCES:
        if not (source/item).exists():raise ValueError('发布目录缺少 '+item)
    if source==target:return {'status':'already_installed','target':str(target),'backups':[]}
    if source in target.parents or target in source.parents:raise ValueError('安装目标与源目录不可互相包含')
    target.parent.mkdir(parents=True,exist_ok=True)
    stage=Path(mkdtemp(prefix='.gxg-stage-',dir=target.parent))
    backups=[];committed=False
    try:
        for item in RESOURCES+OPTIONAL:
            src=source/item
            if not src.exists():continue
            dst=stage/item
            if src.is_dir():shutil.copytree(src,dst,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
            else:shutil.copy2(src,dst)
        stamp=datetime.now().strftime('%Y%m%d-%H%M%S-%f')
        backup_dir=Path(backup_root).expanduser().resolve() if backup_root else target.parent.parent/'gxg-skill-backups'
        if target.exists():
            backup_dir.mkdir(parents=True,exist_ok=True);saved=backup_dir/(target.name+'-'+stamp)
            target.rename(saved);backups.append((target,saved))
        stage.rename(target);committed=True
        legacy=target.with_name(LEGACY)
        # Only migrate the recognized former product, never a name-only collision.
        if target.name==NAME and legacy.is_dir() and (legacy/'SKILL.md').exists():
            text=(legacy/'SKILL.md').read_text(encoding='utf-8')
            if 'name: prospectus-decoder' in text:
                backup_dir.mkdir(parents=True,exist_ok=True);saved=backup_dir/(LEGACY+'-'+stamp)
                legacy.rename(saved);backups.append((legacy,saved))
        return {'status':'installed','target':str(target),'backups':[str(b) for a,b in backups]}
    except Exception:
        if committed and target.exists():shutil.rmtree(target)
        for original,saved in reversed(backups):
            if saved.exists() and not original.exists():saved.rename(original)
        raise
    finally:
        if stage.exists():shutil.rmtree(stage)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--platform',choices=['workbuddy','codex','claude-code','cursor','opencode','agents','generic'])
    p.add_argument('--target',type=Path,help='Explicit final skill directory, including gxg-company-decoder')
    p.add_argument('--backup-root',type=Path)
    p.add_argument('--update',action='store_true',help='Reinstall from this local release; backups retained, no git pull')
    p.add_argument('--check',action='store_true',help='Read-only runtime and release check')
    args=p.parse_args()
    if args.check:
        missing=[x for x in RESOURCES if not (ROOT/x).exists()]
        print('Skill:',NAME,'version:',(ROOT/'VERSION').read_text().strip())
        print('Python:',sys.version.split()[0]);print('markdown-it-py:', 'available' if importlib.util.find_spec('markdown_it') else 'missing; install in a separate venv for HTML rendering')
        print('pdftotext:',shutil.which('pdftotext') or 'not found; use available PDF text extractor')
        print('Network/download access must be verified in the actual Agent session.')
        if missing:p.error('Missing resources: '+','.join(missing))
        return
    if args.target:target=args.target
    elif args.platform=='workbuddy':
        p.error('WorkBuddy首选“添加技能→上传技能”导入WorkBuddy ZIP。若已确认本地安装路径，请使用--target；不猜测客户端路径。')
    elif args.platform in ['codex','claude-code','cursor','opencode','agents']:
        paths={'codex':'.codex/skills','claude-code':'.claude/skills','cursor':'.cursor/skills','opencode':'.config/opencode/skills','agents':'.agents/skills'}
        target=Path.home()/paths[args.platform]/NAME
    else:p.error('请显式指定--platform或--target；通用包请指定目标目录。')
    result=install(ROOT,target,args.backup_root)
    print('观星哥·拆公司 v'+(ROOT/'VERSION').read_text().strip());print('目标:',result['target'])
    for backup in result['backups']:print('已备份:',backup)
    print('请重新加载平台技能列表；旧名称的自动别名不作承诺。')
    print('试试这样用：用“观星哥·拆公司”分析Iambic，先让我选择分析深度。')

if __name__=='__main__':main()
