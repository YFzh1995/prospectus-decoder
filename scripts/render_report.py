#!/usr/bin/env python3
"""Offline report renderer: readable argument, quiet citations, prominent author.

Requires markdown-it-py only. Raw HTML is disabled except validated ID anchors.
"""
import argparse
from html import escape
from pathlib import Path
import re
import sys

CSS = """

:root{color-scheme:light;--bg:#f5f4ef;--paper:#fffefb;--ink:#243343;--muted:#677482;--accent:#12776f;--line:#dce3e2}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--bg);color:var(--ink);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;font-size:16px;line-height:1.85}
a{color:var(--accent);text-underline-offset:3px;overflow-wrap:anywhere}a:hover{text-decoration-thickness:2px}
.shell{max-width:1250px;margin:auto;display:grid;grid-template-columns:245px minmax(0,1fr);gap:32px;padding:40px 24px}
nav{position:sticky;top:24px;max-height:calc(100vh - 48px);overflow:auto;align-self:start;font-size:14px;padding:20px 12px}
nav strong{display:block;letter-spacing:.12em;font-size:12px;color:var(--muted);margin-bottom:16px}nav ul{list-style:none;padding:0;margin:0}nav li{margin:7px 0}nav .sub{padding-left:14px;font-size:12px}nav a{text-decoration:none;color:var(--muted)}nav a:hover{color:var(--accent)}
main{min-width:0;background:var(--paper);padding:44px 48px;border:1px solid var(--line);border-radius:16px;box-shadow:0 8px 32px #24334306}
h1{font-size:clamp(26px,3vw,36px);line-height:1.4;letter-spacing:-.02em;margin:0 0 24px}h2{font-size:23px;margin:44px 0 18px;padding-top:12px;border-top:1px solid var(--line);scroll-margin-top:24px}h3{font-size:18px;margin:28px 0 12px;scroll-margin-top:24px}p{margin:14px 0}li{margin:5px 0}blockquote{margin:20px 0;padding:12px 20px;background:#edf5f2;border-left:3px solid var(--accent);border-radius:0 8px 8px 0}blockquote p{margin:5px 0}
.table-wrap{max-width:100%;overflow-x:auto;margin:22px 0}table{width:100%;border-collapse:collapse;font-size:14px;line-height:1.65}th,td{padding:12px 14px;text-align:left;vertical-align:top;border-bottom:1px solid var(--line);min-width:100px}th{background:#eaf0ef;color:#244841}tbody tr:nth-child(even){background:#f8faf8}
pre{overflow:auto;background:#eef1f2;border-radius:8px;padding:16px;font-size:13px}code{font-family:ui-monospace,SFMono-Regular,monospace;background:#eef1f2;padding:2px 4px;border-radius:3px}pre code{padding:0}hr{border:0;border-top:1px solid var(--line);margin:30px 0}img{max-width:100%;height:auto}main>p:last-child{color:var(--muted);font-size:13px}.top{display:block;margin-top:30px;font-size:13px}
@media(max-width:850px){.shell{display:block;padding:16px 12px}nav{position:static;max-height:none;padding:12px 8px 24px}nav ul{columns:2;column-gap:16px}nav li{break-inside:avoid}main{padding:28px 20px;border-radius:10px}h2{font-size:21px}body{font-size:16px}}
@media(max-width:460px){nav ul{columns:1}main{padding:24px 16px}}
@media print{body{background:white;font-size:11pt}.shell{display:block;padding:0;max-width:none}nav,.top{display:none}main{border:0;box-shadow:none;padding:0}h2,h3{break-after:avoid}tr,blockquote{break-inside:avoid}.table-wrap{overflow:visible}th,td{min-width:0;padding:6px}a{color:inherit}h1{font-size:24pt}}


:root{--bg:#f8f7f3;--paper:#fffefa;--ink:#26343b;--muted:#7c8588;--accent:#246e69;--line:#e8e9e2}
body{font-size:18px;line-height:1.95;background:var(--bg);color:var(--ink);-webkit-font-smoothing:antialiased}
.shell{max-width:1180px;grid-template-columns:210px minmax(0,1fr);gap:46px;padding:64px 30px 80px}
main{padding:0 0 30px;border:0;border-radius:0;box-shadow:none;background:transparent;max-width:780px}
nav{top:32px;padding:0 0 20px;line-height:1.6;font-size:12px;max-height:calc(100vh - 64px)}
nav strong{font-size:11px;letter-spacing:.18em;margin-bottom:22px;color:#98a09f}
nav li{margin:0 0 13px}nav a{display:block;color:#7d8788;transition:color .15s}nav a:hover{color:var(--accent)}
nav .nav-source{margin-top:24px;padding-top:18px;border-top:1px solid var(--line)}
h1{font-size:clamp(30px,3.1vw,42px);font-weight:720;line-height:1.45;letter-spacing:-.035em;margin:0 0 22px;color:#20363b}
p.meta{font-size:12px;letter-spacing:.04em;line-height:1.7;color:#8a9391;margin:0 0 36px}p.meta strong{font-weight:450;color:inherit}
p.lead{font-size:22px;line-height:1.9;color:#354f52;margin:0 0 22px}p.intro{font-size:18px;color:#61706f;margin-bottom:46px}
h2{border-top:1px solid #dee4dd;margin:65px 0 26px;padding-top:26px;font-size:25px;line-height:1.6;letter-spacing:-.015em;color:#203e41;scroll-margin-top:30px}
.section-number{display:block;font-family:ui-sans-serif,-apple-system,sans-serif;font-size:11px;font-weight:500;letter-spacing:.14em;color:#9aa9a1;margin-bottom:8px}
h3{font-size:19px;line-height:1.65;margin:35px 0 15px;color:#315653;font-weight:650}
p{margin:0 0 21px}strong{font-weight:650;color:#294d4e}
ul{padding-left:1.25em;margin:22px 0 28px}main li{padding-left:7px;margin:0 0 15px}main li::marker{color:#8ba297;font-size:.7em}
a{text-decoration-color:#b7cbc2;text-underline-offset:4px}
.reference-mark{font-size:10px;vertical-align:super;line-height:0;margin-left:3px}.reference{font-weight:450;color:#a0aaa5;text-decoration:none;white-space:nowrap;padding:1px 2px}.reference:hover{color:var(--accent);background:#e8eee8;border-radius:3px}
.table-wrap{margin:29px 0 30px;border:1px solid #e0e5de;border-radius:8px;overflow-x:auto;background:#fffefa}
table{font-size:14px;line-height:1.75;min-width:560px}th,td{padding:14px 16px;min-width:90px;border-bottom:1px solid #e6e9e1}th{font-weight:600;background:#edf2eb;color:#37564c}tbody tr:nth-child(even){background:#f6f8f2}tbody tr:last-child td{border-bottom:0}
details.source-notes{margin-top:65px;border-top:1px solid #dfe4dc;border-bottom:1px solid #dfe4dc;padding:22px 0;color:#7a8380;font-size:13px;line-height:1.85;scroll-margin-top:28px}
details.source-notes summary{cursor:pointer;font-size:15px;color:#697b72;font-weight:550;list-style:none;display:flex;align-items:center;justify-content:space-between}
details.source-notes summary::after{content:'＋';font-size:20px;font-weight:300;color:#8b9e92}
details[open].source-notes summary::after{content:'−'}
.source-intro{margin:8px 0 0;font-size:12px;color:#a0aaa1}.source-content{margin-top:30px}.source-content .source-heading{display:none}.source-content h3{font-size:15px;margin-top:28px;color:#738579}.source-content strong{font-weight:550;color:#7b8880}.source-content a{color:#748f83}.source-content .table-wrap{margin:18px 0}.source-content table{font-size:12px}
p.signature{font-size:11px;line-height:1.8;color:#a6ada7;margin:18px 0 0}p.signature+p.signature{margin-top:4px}.top{font-size:12px;color:#8d9d92;margin-top:25px}
@media(max-width:900px){.shell{display:block;padding:32px 28px 60px;max-width:810px}nav{position:static;max-height:none;padding:0 0 30px;margin-bottom:30px;border-bottom:1px solid var(--line)}nav strong{margin-bottom:14px}nav ul{columns:2;column-gap:24px}nav li{margin-bottom:8px}nav .nav-source{margin-top:0;padding-top:0;border-top:0}main{max-width:none}h1{font-size:34px}}
@media(max-width:520px){body{font-size:17px;line-height:1.95}.shell{padding:24px 22px 45px}nav{font-size:11px;margin-bottom:26px;padding-bottom:20px}nav ul{columns:2;column-gap:15px}nav li{margin-bottom:9px}h1{font-size:29px}p.meta{font-size:11px;margin-bottom:28px}p.lead{font-size:20px}h2{font-size:23px;margin-top:48px;padding-top:22px}.section-number{font-size:10px}h3{font-size:18px}.table-wrap{margin-left:-4px;margin-right:-4px}main li{padding-left:3px;margin-bottom:16px}}
@media print{body{background:white;font-size:11pt;line-height:1.8}.shell{display:block;max-width:none;padding:0}nav,.top{display:none}main{max-width:none;padding:0}h1{font-size:26pt}h2{margin-top:30pt;font-size:17pt;padding-top:15pt}p.lead{font-size:13pt}p.intro{font-size:11pt}.table-wrap{overflow:visible}table{min-width:0;font-size:9pt}th,td{min-width:0;padding:6px}details.source-notes{font-size:8pt}.source-content{display:block!important}details.source-notes summary::after{content:''}.source-intro{display:none}}

.product-brand{font-size:12px;letter-spacing:.12em;color:#557e70;margin:0 0 18px;font-weight:600}
.author-signature{margin-top:32px;padding:24px 28px;background:#e9f1e9;border:1px solid #bed0c1;border-left:4px solid #38736b;border-radius:10px;line-height:1.85;color:#294e48}
.author-signature p{margin:0 0 9px;font-size:14px;color:#3d6056}.author-signature p:last-child{margin-bottom:0;font-size:14px}.author-signature p:nth-child(2){font-size:17px;font-weight:650;color:#1f5149}.author-signature em{font-style:normal}.author-signature a{color:inherit}
.source-heading{display:none}.anchor-target{scroll-margin-top:30px}
@media(max-width:520px){.author-signature{padding:20px}.author-signature p:nth-child(2){font-size:16px}}
@media print{.author-signature{break-inside:avoid;print-color-adjust:exact;-webkit-print-color-adjust:exact}.author-signature p,.author-signature p:last-child{font-size:9pt}.author-signature p:nth-child(2){font-size:11pt}}

h2[data-section]::before{content:attr(data-section);display:block;font-size:11px;font-weight:500;letter-spacing:.14em;color:#9aa9a1;margin-bottom:8px}

"""

SCRIPT = """
(function(){
const notes=document.getElementById('source-details');
function reveal(hash){if(!notes||!hash)return;const target=document.getElementById(hash.slice(1));if(target&&(target===notes||notes.contains(target)))notes.open=true;}
document.addEventListener('click',function(e){const a=e.target.closest('a[href^="#"]');if(a)reveal(a.getAttribute('href'));});
window.addEventListener('hashchange',function(){reveal(location.hash);});reveal(location.hash);
let openBeforePrint=false;
window.addEventListener('beforeprint',function(){if(notes){openBeforePrint=notes.open;notes.open=true;}});
window.addEventListener('afterprint',function(){if(notes)notes.open=openBeforePrint;});
})();
"""
SOURCE_TITLES = {'来源与可另存文件','来源与附件','资料、数据口径与附件','来源与注释','sources','references','sources and attachments','sources and notes'}


def render(source, output):
    try:
        from markdown_it import MarkdownIt
    except ImportError:
        raise RuntimeError('需要 markdown-it-py；请在已有运行时或独立虚拟环境中安装。')
    text = source.read_text(encoding='utf-8')
    # Stop BEFORE the next explicit anchor; preserve the first content anchor.
    text = re.sub(r'^## (?:目录|Contents|Table of Contents)[ \t]*\n.*?(?=^<a id="|^## |\Z)', '', text, flags=re.M | re.S)
    anchors = []
    def keep_anchor(match):
        anchors.append(match.group(1))
        return f'\n\nPDANCHOR{len(anchors)-1}END\n\n'
    text = re.sub(r'^<a id="([a-zA-Z][\w-]*)"></a>[ \t]*$', keep_anchor, text, flags=re.M)
    if len(set(anchors)) != len(anchors):
        raise ValueError('Markdown中存在重复显式锚点')
    if set(anchors) & {'top','source-details'}:
        raise ValueError('显式锚点不可使用渲染器保留ID：top/source-details')
    md = MarkdownIt('commonmark', {'html': False, 'typographer': False}).enable('table')
    tokens = md.parse(text)
    title = source.stem
    toc, used = [], set(anchors) | {'top','source-details'}
    number, section_number, source_heading = 0, 0, None
    in_sources = False
    for i, token in enumerate(tokens):
        if token.type != 'heading_open':
            continue
        label = tokens[i+1].content
        if token.tag == 'h1':
            title = label
        elif token.tag in ('h2','h3'):
            number += 1
            anchor = f'pd-heading-{number}'
            while anchor in used:
                anchor += '-nav'
            used.add(anchor)
            token.attrSet('id', anchor)
            if token.tag == 'h2' and label.strip().lower() in SOURCE_TITLES:
                in_sources = True
                source_heading = (anchor, label)
            if token.tag == 'h2':
                if not in_sources:
                    section_number += 1
                    token.attrSet('data-section', f'{section_number:02}')
                    inline = tokens[i+1]
                    if inline.children and inline.children[0].type == 'text':
                        inline.children[0].content = re.sub(r'^\d+[.、]\s*', '', inline.children[0].content)
                toc.append((anchor, re.sub(r'^\d+[.、]\s*', '', label), in_sources))
    body = md.renderer.render(tokens, md.options, {})
    for i, anchor in enumerate(anchors):
        body = body.replace(f'<p>PDANCHOR{i}END</p>', f'<a class="anchor-target" id="{escape(anchor, quote=True)}"></a>')
    if re.search(r'PDANCHOR\d+END', body):
        raise ValueError('显式锚点转换未完成')
    body = body.replace('<table>', '<div class="table-wrap"><table>').replace('</table>', '</table></div>')
    # A citation is an explicit numeric link to a note; never general raw HTML.
    body = re.sub(r'<a href="#((?:note|fn)-[\w-]+)">\[?(\d+)\]?</a>',
                  lambda m: f'<sup class="reference-mark"><a class="reference" href="#{m[1]}" aria-label="Source {m[2]}">{m[2]}</a></sup>', body)
    # Keep signed author paragraphs OUTSIDE the source disclosure.
    signature = re.search(r'<p>(?:<em>|<strong>)?(?:报告由「观星哥·拆公司」|报告由 Prospectus Decoder|Report generated by Prospectus Decoder|Report generated by GXG Company Decoder)', body)
    signature_html = ''
    if signature:
        signature_html = body[signature.start():]
        body = body[:signature.start()]
    if source_heading:
        anchor, label = source_heading
        marker = f'<h2 id="{anchor}">'
        start = body.find(marker)
        if start < 0:
            raise ValueError('无法定位来源标题')
        before, notes = body[:start], body[start:]
        notes = notes.replace(marker, f'<h2 class="source-heading" id="{anchor}">', 1)
        body = before + f'<details class="source-notes" id="source-details"><summary>{escape(label)}</summary><div class="source-content">' + notes + '</div></details>'
    if signature_html:
        body += '<footer class="author-signature" aria-label="Author and feedback">' + signature_html + '</footer>'
    # Short metadata and intro, without any company-specific text matching.
    first_h1_end = body.find('</h1>') + len('</h1>')
    prefix, after_title = body[:first_h1_end], body[first_h1_end:]
    after_title = re.sub(r'<p><strong>([^<\n]+)</strong></p>', r'<p class="meta">\1</p>', after_title, count=1)
    body = prefix + after_title
    # The main navigation remains concise; all headings retain anchors.
    nav = ''.join(f'<li class="{"nav-source" if is_source else "item"}"><a href="#{"source-details" if is_source else anchor}">{escape(label)}</a></li>' for anchor, label, is_source in toc)
    lang = 'zh-CN' if re.search(r'[\u4e00-\u9fff]', text) else 'en'
    nav_title, top_title = ('目录','返回顶部') if lang == 'zh-CN' else ('Contents','Back to top')
    document = f'<!doctype html>\n<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)}</title><style>{CSS}</style></head><body id="top"><div class="shell"><nav aria-label="{nav_title}"><strong>{nav_title}</strong><ul>{nav}</ul></nav><main><div class="product-brand">观星哥·拆公司</div>{body}<a class="top" href="#top">↑ {top_title}</a></main></div><script>{SCRIPT}</script></body></html>'
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(document, encoding='utf-8')
    return len(toc)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('markdown', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    source = args.markdown.resolve()
    output = args.output.resolve() if args.output else source.with_suffix('.html')
    if output == source:
        parser.error('输出不能覆盖Markdown原稿')
    if output.parent != source.parent:
        parser.error('HTML请保存在Markdown同目录，以保持相对附件链接有效')
    try:
        count = render(source, output)
    except (RuntimeError, ValueError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(f'{output} ({count} navigation entries)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
