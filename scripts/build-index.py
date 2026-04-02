#!/usr/bin/env python3
"""
OpenClaw 文档索引生成器
扫描 docs 目录，生成文档索引 JSON
"""

import os
import json
import re
from pathlib import Path

import sys
SKILL_DIR = Path(__file__).parent.parent

# 尝试读取配置
def get_docs_path():
    config_file = SKILL_DIR / "config.json"
    if config_file.exists():
        with open(config_file, 'r') as f:
            import json
            config = json.load(f)
            return config.get('docs_path', '/Users/su/my-github/openclaw-zh/docs')
    # 检查常见位置
    possible_paths = [
        '/Users/su/my-github/openclaw-zh/docs',
        str(SKILL_DIR / 'docs'),
        str(Path.home() / 'openclaw-docs-cache'),
        str(Path.home() / 'openclaw-docs'),
    ]
    for path in possible_paths:
        if Path(path).exists():
            return path
    return '/Users/su/my-github/openclaw-zh/docs'  # 默认

DOCS_DIR = get_docs_path()
INDEX_FILE = "../docs-index.json"


def extract_title(file_path):
    """从 markdown 文件提取 title"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read(2000)  # 只读前2000字符
            
        # 尝试从 frontmatter 提取 title
        if content.startswith('---'):
            match = re.search(r'title:\s*["\']?([^"\'\n]+)["\']?', content)
            if match:
                return match.group(1).strip()
        
        # 尝试从第一个 # 标题提取
        match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if match:
            return match.group(1).strip()
            
        # 使用文件名
        return Path(file_path).stem.replace('-', ' ').replace('_', ' ').title()
    except:
        return Path(file_path).stem


def extract_summary(file_path):
    """从 markdown 文件提取摘要"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read(3000)
        
        # 尝试从 frontmatter 提取 summary
        if content.startswith('---'):
            match = re.search(r'summary:\s*["\']?([^"\'\n]+)["\']?', content)
            if match:
                return match.group(1).strip()
        
        # 提取第一段非空文本
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#') and not line.startswith('---'):
                return line[:200]
        return ""
    except:
        return ""


def build_index():
    """构建文档索引"""
    index = {
        "total_files": 0,
        "categories": {},
        "files": []
    }
    
    for root, dirs, files in os.walk(DOCS_DIR):
        # 跳过隐藏目录
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            if not file.endswith('.md'):
                continue
                
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, DOCS_DIR)
            
            # 获取分类
            category = rel_path.split('/')[0] if '/' in rel_path else 'root'
            
            doc_info = {
                "path": rel_path,
                "full_path": file_path,
                "title": extract_title(file_path),
                "summary": extract_summary(file_path),
                "category": category
            }
            
            index["files"].append(doc_info)
            index["total_files"] += 1
            
            # 按分类统计
            if category not in index["categories"]:
                index["categories"][category] = 0
            index["categories"][category] += 1
    
    # 排序
    index["files"].sort(key=lambda x: x["path"])
    
    return index


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Build docs index')
    parser.add_argument('--docs-path', default=DOCS_DIR, help='Path to docs directory')
    args = parser.parse_args()
    
    global DOCS_DIR
    DOCS_DIR = args.docs_path
    
    print(f"🔍 正在扫描文档目录: {DOCS_DIR}")
    index = build_index()
    
    # 保存索引
    output_path = SKILL_DIR / "docs-index.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 索引生成完成！")
    print(f"📊 共索引 {index['total_files']} 个文件")
    print(f"📁 分类统计：")
    for cat, count in sorted(index["categories"].items(), key=lambda x: -x[1]):
        print(f"   - {cat}: {count} 个文件")


if __name__ == "__main__":
    main()
