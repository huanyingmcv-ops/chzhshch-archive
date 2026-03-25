#!/usr/bin/env python3
"""
为每个分类目录生成索引页面
"""
import os
import re

def extract_title(filename):
    """从文件名提取标题"""
    # 去掉.md后缀和编号前缀
    title = re.sub(r'^\d+_', '', filename.replace('.md', ''))
    return title

def generate_category_index(category_dir, category_info):
    """为指定分类生成索引页面"""
    
    # 读取该目录下的所有md文件
    md_files = [f for f in os.listdir(category_dir) if f.endswith('.md')]
    md_files.sort()  # 按文件名排序（通常是编号顺序）
    
    # 提取文章列表
    articles = []
    for f in md_files:
        articles.append({
            'filename': f,
            'title': extract_title(f)
        })
    
    # 生成分类索引HTML
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{category_info['name']} | 缠中说禅</title>
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
            --bg: #f8fafc;
            --card-bg: #ffffff;
            --border: #e2e8f0;
        }}
        
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: 'Noto Sans SC', -apple-system, BlinkMacSystemFont, sans-serif;
            line-height: 1.8;
            color: var(--text);
            background: var(--bg);
            min-height: 100vh;
        }}
        
        header {{
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            color: white;
            padding: 60px 20px 50px;
            text-align: center;
        }}
        
        .back-link {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            color: rgba(255,255,255,0.8);
            text-decoration: none;
            margin-bottom: 20px;
            font-size: 0.95em;
            transition: color 0.3s;
        }}
        
        .back-link:hover {{
            color: var(--gold-light);
        }}
        
        h1 {{
            font-family: 'Noto Serif SC', serif;
            font-size: 2.5em;
            font-weight: 700;
            margin-bottom: 15px;
            letter-spacing: 6px;
        }}
        
        .subtitle {{
            font-size: 1.1em;
            color: var(--gold-light);
            letter-spacing: 3px;
            margin-bottom: 20px;
        }}
        
        .desc {{
            font-size: 1em;
            color: rgba(255,255,255,0.8);
            max-width: 600px;
            margin: 0 auto;
            line-height: 1.8;
        }}
        
        .stats {{
            margin-top: 25px;
            padding-top: 25px;
            border-top: 1px solid rgba(255,255,255,0.1);
        }}
        
        .stats span {{
            display: inline-block;
            background: rgba(255,255,255,0.1);
            padding: 8px 20px;
            border-radius: 20px;
            font-size: 0.9em;
            margin: 0 5px;
        }}
        
        main {{
            max-width: 900px;
            margin: 0 auto;
            padding: 50px 20px;
        }}
        
        .article-list {{
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            overflow: hidden;
        }}
        
        .article-item {{
            display: flex;
            align-items: center;
            padding: 18px 25px;
            border-bottom: 1px solid var(--border);
            text-decoration: none;
            color: inherit;
            transition: all 0.2s;
        }}
        
        .article-item:last-child {{
            border-bottom: none;
        }}
        
        .article-item:hover {{
            background: #f8fafc;
            padding-left: 30px;
        }}
        
        .article-number {{
            font-size: 0.85em;
            color: var(--gold);
            font-weight: 600;
            min-width: 50px;
            font-family: monospace;
        }}
        
        .article-title {{
            flex: 1;
            font-size: 1.05em;
            color: var(--text);
        }}
        
        .article-item:hover .article-title {{
            color: var(--primary);
        }}
        
        .article-arrow {{
            color: var(--text-light);
            opacity: 0;
            transition: opacity 0.2s;
        }}
        
        .article-item:hover .article-arrow {{
            opacity: 1;
        }}
        
        footer {{
            background: var(--primary);
            color: rgba(255,255,255,0.7);
            padding: 40px 20px;
            text-align: center;
            margin-top: 50px;
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
        
        @media (max-width: 600px) {{
            h1 {{ font-size: 1.8em; letter-spacing: 4px; }}
            .article-item {{ padding: 15px 18px; }}
            .article-number {{ min-width: 40px; font-size: 0.8em; }}
            .article-title {{ font-size: 0.95em; }}
        }}
    </style>
</head>
<body>
    <header>
        <a href="../" class="back-link">← 返回首页</a>
        <h1>{category_info['name']}</h1>
        <p class="subtitle">{category_info['subtitle']}</p>
        <p class="desc">{category_info['desc']}</p>
        <div class="stats">
            <span>共 {len(articles)} 篇文章</span>
        </div>
    </header>
    
    <main>
        <div class="article-list">
'''
    
    # 添加文章列表
    for i, article in enumerate(articles, 1):
        html += f'''            <a href="{article['filename']}" class="article-item">
                <span class="article-number">{i:03d}</span>
                <span class="article-title">{article['title']}</span>
                <span class="article-arrow">→</span>
            </a>
'''
    
    html += '''        </div>
    </main>
    
    <footer>
        <p>本站所有内容版权归原作者（缠中说禅）所有</p>
        <p>仅供学习交流使用，如有侵权请联系删除</p>
        <p class="footer-curator">全库整理 · 元白</p>
    </footer>
</body>
</html>'''
    
    # 写入文件
    index_path = os.path.join(category_dir, 'index.html')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✓ 生成: {index_path} ({len(articles)} 篇文章)")
    return len(articles)

# 分类信息
categories = {
    '01_时政历史': {
        'name': '时政历史',
        'subtitle': '政治 · 历史 · 经济',
        'desc': '民国、台湾、抗战、政治制度、主权相关。货币战争、人民币战略、经济危机。'
    },
    '02_社会文化': {
        'name': '社会文化',
        'subtitle': '文化 · 社会 · 评论',
        'desc': '文化现象、社会评论、人物事件、网络舆论。犀利点评，纵论古今。'
    },
    '03_解盘市场': {
        'name': '解盘市场',
        'subtitle': '大盘 · 个股 · 实时分析',
        'desc': '大盘分析、个股解盘、走势研判。2006-2008年实时市场评论，最珍贵的教学案例。'
    },
    '04_论语详解': {
        'name': '论语详解',
        'subtitle': '儒家 · 经典 · 正本清源',
        'desc': '给所有曲解孔子的人。逐字逐句解读，还原真正的儒家思想，理解"君子不器"。'
    },
    '05_108课教程': {
        'name': '108课教程',
        'subtitle': '缠论 · 技术 · 操作系统',
        'desc': '教你炒股票108课完整技术体系。分型、中枢、背驰、买卖点，从零构建操作系统。'
    },
    '06_诗词文学': {
        'name': '诗词文学',
        'subtitle': '诗词 · 创作 · 文学',
        'desc': '古体诗、现代诗、歌词创作、文学评论。才华横溢，意境深远，不让古人。'
    },
    '07_音乐艺术': {
        'name': '音乐艺术',
        'subtitle': '音乐 · 艺术 · 鉴赏',
        'desc': '周末音乐会、古典音乐赏析、艺术评论。舒伯特、贝多芬、萧邦，用音乐说禅。'
    },
    '08_禅宗哲学': {
        'name': '禅宗哲学',
        'subtitle': '禅宗 · 哲学 · 心性',
        'desc': '缠中说禅系列、枯木龙吟照大千。禅宗智慧，打坐指导，直指人心，见性成佛。'
    },
    '09_数学科学': {
        'name': '数学科学',
        'subtitle': '数学 · 科学 · 技术',
        'desc': '数学、科学、技术相关。数学世界之王，闲谈现代数学的基础问题。'
    },
    '10_个人随笔': {
        'name': '个人随笔',
        'subtitle': '随笔 · 杂文 · 真情',
        'desc': '那一夜系列、白话杂文、个人感想。真实、性情、不做作，缠师的另一面。'
    }
}

# 执行生成
total = 0
for dir_name, info in categories.items():
    if os.path.exists(dir_name):
        count = generate_category_index(dir_name, info)
        total += count
    else:
        print(f"✗ 跳过: {dir_name} (目录不存在)")

print(f"\n总计: {total} 篇文章")
