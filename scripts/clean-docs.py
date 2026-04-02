#!/usr/bin/env python3
"""
文档清洗工具 - 用于 GitHub Actions
清洗 Markdown 文档内容
"""

import re
import sys
from pathlib import Path


def clean_markdown_file(filepath):
    """清洗单个 Markdown 文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # 1. 移除 HTML 注释
        content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
        
        # 2. 规范化代码块标记（移除语言标记后的多余空格）
        content = re.sub(r'```\s*\n', '```\n', content)
        
        # 3. 移除多余空行（超过3个换行保留3个）
        content = re.sub(r'\n{4,}', '\n\n\n', content)
        
        # 4. 修复 frontmatter 格式
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                frontmatter = parts[1].strip()
                body = parts[2].strip()
                
                # 清理 frontmatter
                lines = []
                for line in frontmatter.split('\n'):
                    line = line.strip()
                    if line and not line.startswith('#'):
                        lines.append(line)
                
                frontmatter = '\n'.join(lines)
                content = f"---\n{frontmatter}\n---\n\n{body}"
        
        # 5. 确保文件以换行符结尾
        content = content.rstrip() + '\n'
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
        
    except Exception as e:
        print(f"⚠️  无法处理 {filepath}: {e}")
        return False


def main():
    if len(sys.argv) < 2:
        print("Usage: python clean-docs.py <docs-directory>")
        sys.exit(1)
    
    docs_dir = Path(sys.argv[1])
    
    if not docs_dir.exists():
        print(f"❌ 目录不存在: {docs_dir}")
        sys.exit(1)
    
    print(f"🧹 清洗文档: {docs_dir}")
    
    cleaned_count = 0
    for md_file in docs_dir.rglob("*.md"):
        if clean_markdown_file(md_file):
            cleaned_count += 1
    
    print(f"✅ 清洗完成: {cleaned_count} 个文件")


if __name__ == "__main__":
    main()
