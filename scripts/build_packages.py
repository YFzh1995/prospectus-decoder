#!/usr/bin/env python3
"""Build WorkBuddy/Codex/generic ZIPs from a single core. Standard library only."""
import argparse
import json
from pathlib import Path
import re
import zipfile
ROOT=Path(__file__).resolve().parents[1]
NAME='gxg-company-decoder'

def workbuddy_document(original,version):
    parts=original.split('---',2)
    if len(parts)!=3:raise ValueError('SKILL.md缺少frontmatter')
    header={
        'name':NAME,'display_name':'观星哥·拆公司','display_name_en':'GXG Company Decoder',
        'description':'拆公司、招股书解读与商业模式分析：输入公司名，拆解产品、客户、收入、成本、现金与竞争，保留可查来源。',
        'description_zh':'输入公司名或招股书，拆解公司靠什么赚钱、收入为何增长、钱花到哪里，并生成有数据和来源的商业分析报告。',
        'description_en':'Understand how a company makes money through official filings, financial analysis, claim checks and peer comparisons.',
        'examples_zh':['帮我分析泡泡玛特，它靠什么赚钱？先让我选择报告深度。','用招股书拆解小米的收入、成本和现金流。','分析 Iambic，做 L3 数据与同行对照。'],
        'examples_en':['Analyze Iambic and let me choose the depth.','Explain revenue growth, spending and cash flow.','Check qualified leadership claims and compare peers.'],
        'version':version,'author':'观星哥'}
    lines=[]
    for k,v in header.items():
        if isinstance(v,list):lines.append(k+':\n'+'\n'.join('- '+json.dumps(x,ensure_ascii=False) for x in v))
        else:lines.append(k+': '+json.dumps(v,ensure_ascii=False))
    return '---\n'+'\n'.join(lines)+'\n---'+parts[2]

def build(out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    version=(ROOT/'VERSION').read_text().strip();original=(ROOT/'SKILL.md').read_text()
    if not re.search(r'^name: '+NAME+r'\s*$',original,re.M):raise ValueError('Canonical name mismatch')
    results=[]
    for platform in ['workbuddy','codex','generic','skillhub']:
        dest=out/f'{NAME}-{version}-{platform}.zip'
        with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED) as z:
            for f in sorted(ROOT.rglob('*')):
                rel=f.relative_to(ROOT)
                if out.resolve() in f.resolve().parents:continue
                if not f.is_file() or any(x in {'.git','__pycache__','outputs','.DS_Store'} for x in rel.parts) or f.suffix=='.pyc':continue
                if rel.parts[0]=='platforms':continue
                if rel.parts[0]=='agents' and platform!='codex':continue
                if platform=='skillhub' and str(rel)=='.gitignore':continue
                data=workbuddy_document(original,version).encode() if platform in ('workbuddy','skillhub') and str(rel)=='SKILL.md' else f.read_bytes()
                if platform=='skillhub':
                    if rel.name=='VERSION':rel=rel.with_name('VERSION.md')
                    if rel.suffix in ('.md','.py','.sh'):
                        data=re.sub(rb'\bVERSION\b(?!\.md)', b'VERSION.md', data)
                z.writestr(str(Path(NAME)/rel),data)
        results.append(dest)
    return results

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    for path in build(args.output):print(path)
if __name__=='__main__':main()
