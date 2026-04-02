#!/usr/bin/env python3
"""
OpenClaw 文档搜索工具
根据关键词搜索相关文档
"""

import json
import sys
import os
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent
INDEX_FILE = SKILL_DIR / "docs-index.json"

# 尝试读取配置
def get_docs_base():
    config_file = SKILL_DIR / "config.json"
    if config_file.exists():
        with open(config_file, 'r') as f:
            config = json.load(f)
            return config.get('docs_path', '/Users/su/my-github/openclaw-zh/docs')
    return '/Users/su/my-github/openclaw-zh/docs'

DOCS_BASE = get_docs_base()


def load_index():
    """加载文档索引"""
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def search_docs(keyword, index):
    """搜索文档"""
    keyword = keyword.lower()
    results = []
    
    for doc in index["files"]:
        # 在标题、摘要、路径中搜索
        text = f"{doc['title']} {doc.get('summary', '')} {doc['path']}".lower()
        if keyword in text:
            results.append(doc)
    
    # 按相关性排序（标题匹配优先）
    def relevance(doc):
        title = doc['title'].lower()
        if keyword in title:
            return 0
        elif keyword in doc.get('summary', '').lower():
            return 1
        else:
            return 2
    
    results.sort(key=relevance)
    return results


def format_result(doc, show_summary=True):
    """格式化输出"""
    result = f"📄 {doc['title']}\n"
    result += f"   路径: {doc['path']}\n"
    if show_summary and doc.get('summary'):
        result += f"   摘要: {doc['summary'][:100]}...\n"
    return result


def main():
    if len(sys.argv) < 2:
        print("🔍 OpenClaw 文档搜索工具")
        print("\n用法:")
        print("  python search-docs.py <关键词> [数量]")
        print("\n示例:")
        print("  python search-docs.py 'multi-agent'")
        print("  python search-docs.py '配置' 10")
        sys.exit(1)
    
    keyword = sys.argv[1]
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    
    print(f"🔍 搜索: '{keyword}'\n")
    
    index = load_index()
    results = search_docs(keyword, index)
    
    if not results:
        print("❌ 未找到相关文档")
        print(f"\n💡 提示: 试试更通用的词，如 'gateway', 'config', 'skill'")
        return
    
    print(f"✅ 找到 {len(results)} 个相关文档 (显示前 {min(limit, len(results))} 个):\n")
    
    for doc in results[:limit]:
        print(format_result(doc))
    
    if len(results) > limit:
        print(f"... 还有 {len(results) - limit} 个结果")
    
    print(f"\n📚 文档库总计: {index['total_files']} 个文件")


if __name__ == "__main__":
    main()
