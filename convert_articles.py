#!/usr/bin/env python3
"""
为所有Markdown文章生成精美的HTML阅读页面
"""
import os
import re
import markdown
from markdown.extensions import fenced_code, tables

def extract_metadata(content):
    """提取文章元数据"""
    metadata = {}
    
    # 提取原文编号
    number_match = re.search(r'\*\*原文编号\*\*:\s*(\d+)', content)
    if number_match:
        metadata['number'] = number_match.group(1)
    
    # 提取发布时间
    date_match = re.search(r'\*\*发布时间\*\*:\s*(.+?)(?:\n|\r)', content)
    if date_match:
        metadata['date'] = date_match.group(1).strip()
    
    # 提取原文链接
    link_match = re.search(r'\*\*原文链接\*\*:\s*(.+?)(?:\n|\r)', content)
    if link_match:
        metadata['link'] = link_match.group(1).strip()
    
    # 提取分类
    cat_match = re.search(r'\*\*分类\*\*:\s*(.+?)(?:\n|\r)', content)
    if cat_match:
        metadata['category'] = cat_match.group(1).strip()
    
    return metadata

def md_to_html(md_content):
    """将Markdown转换为HTML"""
    # 移除元数据块，只保留正文
    lines = md_content.split('\n')
    content_lines = []
    in_metadata = False
    metadata_ended = False
    
    for line in lines:
        if line.startswith('> **原文') or line.startswith('> **发布时间') or line.startswith('> **原文链接') or line.startswith('> **分类'):
            in_metadata = True
            continue
        if in_metadata and line.startswith('>'):
            continue
        if in_metadata and not line.startswith('>'):
            in_metadata = False
            metadata_ended = True
        if line.startswith('---') and not metadata_ended:
            metadata_ended = True
            continue
        if metadata_ended or (not line.startswith('>') and not line.startswith('---')):
            content_lines.append(line)
    
    content = '\n'.join(content_lines)
    
    # 转换Markdown为HTML
    md = markdown.Markdown(extensions=['fenced_code', 'tables'])
    html_content = md.convert(content)
    
    return html_content

def generate_article_html(md_file, category_name, category_path):
    """生成文章HTML页面"""
    
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # 提取元数据
    metadata = extract_metadata(md_content)
    
    # 提取标题
    title_match = re.search(r'^#\s+(.+)$', md_content, re.MULTILINE)
    title = title_match.group(1) if title_match else os.path.basename(md_file).replace('.md', '')
    
    # 转换正文
    content_html = md_to_html(md_content)
    
    # 获取前后文章链接
    dir_path = os.path.dirname(md_file)
    all_files = sorted([f for f in os.listdir(dir_path) if f.endswith('.md')])
    current_file = os.path.basename(md_file)
    current_idx = all_files.index(current_file)
    
    prev_link = ''
    next_link = ''
    
    if current_idx > 0:
        prev_file = all_files[current_idx - 1]
        prev_title = re.sub(r'^\d+_', '', prev_file.replace('.md', ''))
        prev_link = f'<a href="{prev_file}" class="nav-link prev">← {prev_title[:20]}{"..." if len(prev_title) > 20 else ""}</a>'
    
    if current_idx < len(all_files) - 1:
        next_file = all_files[current_idx + 1]
        next_title = re.sub(r'^\d+_', '', next_file.replace('.md', ''))
        next_link = f'<a href="{next_file}" class="nav-link next">{next_title[:20]}{"..." if len(next_title) > 20 else ""} →</a>'
    
    # 生成HTML
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | 缠中说禅</title>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700&family=Noto+Sans+SC:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {{
            --primary: #0f172a;
            --secondary: #1e293b;
            --accent: #334155;
            --gold: #d4af37;
            --gold-light: #f0d878;
            --text: #1f2937;
            --text-light: #6b7280;
            --text-muted: #94a3b8;
            --bg: #f8fafc;
            --card-bg: #ffffff;
            --border: #e2e8f0;
        }}
        
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: 'Noto Serif SC', 'Noto Sans SC', -apple-system, BlinkMacSystemFont, serif;
            line-height: 1.9;
            color: var(--text);
            background: var(--bg);
            min-height: 100vh;
        }}
        
        /* 顶部导航 */
        .top-nav {{
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            padding: 15px 0;
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .nav-container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 0 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .nav-brand {{
            color: var(--gold-light);
            text-decoration: none;
            font-family: 'Noto Serif SC', serif;
            font-size: 1.3em;
            letter-spacing: 4px;
            font-weight: 600;
        }}
        
        .nav-links {{
            display: flex;
            gap: 20px;
        }}
        
        .nav-links a {{
            color: rgba(255,255,255,0.8);
            text-decoration: none;
            font-size: 0.9em;
            transition: color 0.3s;
        }}
        
        .nav-links a:hover {{
            color: var(--gold-light);
        }}
        
        /* 文章头部 */
        .article-header {{
            background: linear-gradient(180deg, var(--secondary) 0%, var(--bg) 100%);
            padding: 60px 20px 40px;
            text-align: center;
        }}
        
        .article-meta-bar {{
            display: inline-flex;
            gap: 20px;
            margin-bottom: 25px;
            flex-wrap: wrap;
            justify-content: center;
        }}
        
        .meta-item {{
            display: flex;
            align-items: center;
            gap: 6px;
            color: rgba(255,255,255,0.7);
            font-size: 0.9em;
        }}
        
        .meta-item .icon {{
            color: var(--gold);
        }}
        
        .article-title {{
            font-family: 'Noto Serif SC', serif;
            font-size: 2.2em;
            font-weight: 700;
            color: white;
            max-width: 800px;
            margin: 0 auto;
            line-height: 1.4;
            letter-spacing: 2px;
        }}
        
        /* 文章正文 */
        .article-container {{
            max-width: 720px;
            margin: 0 auto;
            padding: 50px 25px;
        }}
        
        .article-content {{
            background: white;
            padding: 50px;
            border-radius: 16px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.06);
            font-size: 1.1em;
            line-height: 2;
        }}
        
        .article-content h1 {{
            font-size: 1.8em;
            margin: 1.5em 0 0.8em;
            color: var(--primary);
            border-bottom: 2px solid var(--gold);
            padding-bottom: 0.3em;
        }}
        
        .article-content h2 {{
            font-size: 1.5em;
            margin: 1.5em 0 0.7em;
            color: var(--primary);
        }}
        
        .article-content h3 {{
            font-size: 1.3em;
            margin: 1.3em 0 0.6em;
            color: var(--secondary);
        }}
        
        .article-content p {{
            margin: 1em 0;
            text-align: justify;
        }}
        
        .article-content blockquote {{
            margin: 1.5em 0;
            padding: 15px 25px;
            border-left: 4px solid var(--gold);
            background: var(--bg);
            color: var(--text-light);
            font-style: italic;
        }}
        
        .article-content code {{
            background: #f1f5f9;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 0.9em;
            color: #c7254e;
        }}
        
        .article-content pre {{
            background: var(--primary);
            color: #e2e8f0;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
            margin: 1.5em 0;
        }}
        
        .article-content pre code {{
            background: transparent;
            color: inherit;
            padding: 0;
        }}
        
        .article-content ul, .article-content ol {{
            margin: 1em 0;
            padding-left: 2em;
        }}
        
        .article-content li {{
            margin: 0.5em 0;
        }}
        
        .article-content table {{
            width: 100%;
            border-collapse: collapse;
            margin: 1.5em 0;
        }}
        
        .article-content th, .article-content td {{
            padding: 12px;
            border: 1px solid var(--border);
            text-align: left;
        }}
        
        .article-content th {{
            background: var(--bg);
            font-weight: 600;
        }}
        
        .article-content a {{
            color: var(--gold);
            text-decoration: none;
            border-bottom: 1px dotted var(--gold);
        }}
        
        .article-content a:hover {{
            border-bottom-style: solid;
        }}
        
        /* 原文链接 */
        .source-link {{
            margin-top: 40px;
            padding-top: 30px;
            border-top: 1px solid var(--border);
            text-align: center;
        }}
        
        .source-link a {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            color: var(--text-light);
            text-decoration: none;
            font-size: 0.9em;
            transition: color 0.3s;
        }}
        
        .source-link a:hover {{
            color: var(--gold);
        }}
        
        /* 底部导航 */
        .article-nav {{
            max-width: 720px;
            margin: 40px auto 0;
            padding: 0 25px;
            display: flex;
            justify-content: space-between;
            gap: 20px;
        }}
        
        .nav-link {{
            flex: 1;
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 20px 25px;
            background: white;
            border-radius: 12px;
            text-decoration: none;
            color: var(--text);
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            transition: all 0.3s;
        }}
        
        .nav-link:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            border-color: var(--gold);
        }}
        
        .nav-link.prev {{
            justify-content: flex-start;
        }}
        
        .nav-link.next {{
            justify-content: flex-end;
            text-align: right;
        }}
        
        .nav-link .label {{
            font-size: 0.8em;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .nav-link .title {{
            font-weight: 500;
            color: var(--primary);
        }}
        
        .nav-link:hover .title {{
            color: var(--gold);
        }}
        
        /* 页脚 */
        footer {{
            background: var(--primary);
            color: rgba(255,255,255,0.7);
            padding: 40px 20px;
            text-align: center;
            margin-top: 60px;
        }}
        
        footer p {{
            font-size: 0.9em;
            margin-bottom: 8px;
        }}
        
        .footer-curator {{
            color: var(--gold-light);
            font-family: 'Noto Serif SC', serif;
            margin-top: 15px;
            letter-spacing: 3px;
        }}
        
        /* 返回顶部按钮 */
        .back-to-top {{
            position: fixed;
            bottom: 30px;
            right: 30px;
            width: 45px;
            height: 45px;
            background: var(--gold);
            color: white;
            border: none;
            border-radius: 50%;
            cursor: pointer;
            font-size: 1.2em;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            transition: all 0.3s;
            opacity: 0;
            visibility: hidden;
        }}
        
        .back-to-top.visible {{
            opacity: 1;
            visibility: visible;
        }}
        
        .back-to-top:hover {{
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.2);
        }}
        
        @media (max-width: 768px) {{
            .article-title {{ font-size: 1.6em; }}
            .article-content {{ padding: 30px 20px; font-size: 1em; }}
            .article-nav {{ flex-direction: column; }}
            .nav-links {{ display: none; }}
        }}
    </style>
</head>
<body>
    <nav class="top-nav">
        <div class="nav-container">
            <a href="../" class="nav-brand">缠中说禅</a>
            <div class="nav-links">
                <a href="./">← 返回分类</a>
                <a href="../index.html">首页</a>
            </div>
        </div>
    </nav>
    
    <header class="article-header">
        <div class="article-meta-bar">
            {f'<div class="meta-item"><span class="icon">◈</span><span>编号 {metadata["number"]}</span></div>' if 'number' in metadata else ''}
            {f'<div class="meta-item"><span class="icon">◷</span><span>{metadata["date"]}</span></div>' if 'date' in metadata else ''}
            {f'<div class="meta-item"><span class="icon">◉</span><span>{category_name}</span></div>' if category_name else ''}
        </div>
        <h1 class="article-title">{title}</h1>
    </header>
    
    <main class="article-container">
        <article class="article-content">
            {content_html}
            
            {'<div class="source-link"><a href="' + metadata['link'] + '" target="_blank">查看原文链接 →</a></div>' if 'link' in metadata else ''}
        </article>
        
        <nav class="article-nav">
            {prev_link if prev_link else '<div></div>'}
            {next_link if next_link else '<div></div>'}
        </nav>
    </main>
    
    <footer>
        <p>本站所有内容版权归原作者（缠中说禅）所有</p>
        <p>仅供学习交流使用，如有侵权请联系删除</p>
        <p class="footer-curator">全库整理 · 元白</p>
    </footer>
    
    <button class="back-to-top" onclick="window.scrollTo({{top: 0, behavior: 'smooth'}})">↑</button>
    
    <script>
        // 返回顶部按钮显示/隐藏
        const backToTop = document.querySelector('.back-to-top');
        window.addEventListener('scroll', () => {{
            if (window.scrollY > 300) {{
                backToTop.classList.add('visible');
            }} else {{
                backToTop.classList.remove('visible');
            }}
        }});
    </script>
</body>
</html>'''
    
    return html

def process_category(category_dir, category_name):
    """处理整个分类目录"""
    md_files = [f for f in os.listdir(category_dir) if f.endswith('.md')]
    md_files.sort()
    
    count = 0
    for md_file in md_files:
        md_path = os.path.join(category_dir, md_file)
        html_content = generate_article_html(md_path, category_name, category_dir)
        
        # 生成HTML文件名（同名）
        html_file = md_file.replace('.md', '.html')
        html_path = os.path.join(category_dir, html_file)
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        count += 1
        if count % 50 == 0:
            print(f"  已处理 {count}/{len(md_files)} 篇...")
    
    return count

# 分类信息
categories = {
    '01_时政历史': '时政历史',
    '02_社会文化': '社会文化',
    '03_解盘市场': '解盘市场',
    '04_论语详解': '论语详解',
    '05_108课教程': '108课教程',
    '06_诗词文学': '诗词文学',
    '07_音乐艺术': '音乐艺术',
    '08_禅宗哲学': '禅宗哲学',
    '09_数学科学': '数学科学',
    '10_个人随笔': '个人随笔'
}

# 执行转换
total = 0
for dir_name, name in categories.items():
    if os.path.exists(dir_name):
        print(f"\n处理 {name}...")
        count = process_category(dir_name, name)
        total += count
        print(f"✓ {name}: {count} 篇")
    else:
        print(f"✗ 跳过: {dir_name}")

print(f"\n总计生成: {total} 个HTML页面")
