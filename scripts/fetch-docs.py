#!/usr/bin/env python3
"""
OpenClaw Docs Skill - 智能文档拉取工具
从 GitHub 拉取文档，过滤语言，清洗内容
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import re

# 配置
GITHUB_REPO = "https://github.com/openclaw/openclaw.git"
DEFAULT_CACHE_DIR = Path.home() / ".openclaw" / "docs-cache"
SKILL_DIR = Path(__file__).parent.parent

# 要剔除的语言目录
EXCLUDE_LANGS = {'zh-CN', 'ja-JP', 'ko-KR', 'de-DE', 'fr-FR', 'es-ES'}


def run_cmd(cmd, cwd=None, check=True):
    """运行命令"""
    try:
        result = subprocess.run(
            cmd, shell=True, cwd=cwd, check=check,
            capture_output=True, text=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        if check:
            print(f"❌ 命令失败: {cmd}")
            print(f"   错误: {e.stderr}")
            raise
        return None


def check_git():
    """检查 git 是否可用"""
    try:
        subprocess.run(['git', '--version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def sparse_clone_docs(target_dir):
    """使用 sparse checkout 只拉取 docs 目录"""
    print("📥 使用 sparse checkout 拉取文档...")
    print(f"   仓库: {GITHUB_REPO}")
    print(f"   目标: {target_dir}")
    
    # 清理或创建目录
    if target_dir.exists():
        print("   清理旧目录...")
        shutil.rmtree(target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    
    # 初始化仓库
    run_cmd("git init", cwd=target_dir)
    run_cmd("git remote add origin " + GITHUB_REPO, cwd=target_dir)
    
    # 配置 sparse checkout
    run_cmd("git config core.sparseCheckout true", cwd=target_dir)
    
    # 只检出 docs 目录
    sparse_file = target_dir / ".git" / "info" / "sparse-checkout"
    with open(sparse_file, 'w') as f:
        f.write("docs/\n")
    
    # 拉取（浅克隆，只取最新）
    print("   正在下载...")
    run_cmd("git pull --depth 1 origin main", cwd=target_dir)
    
    # 移动 docs 内容到根目录
    docs_dir = target_dir / "docs"
    if docs_dir.exists():
        temp_dir = target_dir.parent / ".docs-temp"
        shutil.move(str(docs_dir), str(temp_dir))
        shutil.rmtree(target_dir)
        shutil.move(str(temp_dir), str(target_dir))
    
    print(f"✅ 拉取完成: {target_dir}")
    return target_dir


def remove_non_english_docs(docs_dir):
    """移除非英文文档"""
    print("\n🧹 清理非英文文档...")
    
    removed_count = 0
    for lang_dir in EXCLUDE_LANGS:
        lang_path = Path(docs_dir) / lang_dir
        if lang_path.exists():
            file_count = len(list(lang_path.rglob("*.md")))
            shutil.rmtree(lang_path)
            print(f"   已移除: {lang_dir}/ ({file_count} 个文件)")
            removed_count += file_count
    
    # 也清理 .i18n 目录
    i18n_path = Path(docs_dir) / ".i18n"
    if i18n_path.exists():
        shutil.rmtree(i18n_path)
        print(f"   已移除: .i18n/")
    
    print(f"✅ 清理完成，共移除 {removed_count} 个非英文文件")
    return removed_count


def clean_documentation(docs_dir):
    """清洗文档内容"""
    print("\n✨ 清洗文档内容...")
    
    cleaned = 0
    for md_file in Path(docs_dir).rglob("*.md"):
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original = content
            
            # 1. 移除 HTML 注释
            content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
            
            # 2. 规范化代码块
            content = re.sub(r'```\s*\n', '```\n', content)
            
            # 3. 移除多余空行
            content = re.sub(r'\n{4,}', '\n\n\n', content)
            
            # 4. 确保 frontmatter 格式正确
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    frontmatter = parts[1].strip()
                    body = parts[2].strip()
                    # 修复 frontmatter
                    frontmatter = fix_frontmatter(frontmatter)
                    content = f"---\n{frontmatter}\n---\n\n{body}"
            
            if content != original:
                with open(md_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                cleaned += 1
                
        except Exception as e:
            print(f"   警告: 无法处理 {md_file}: {e}")
    
    print(f"✅ 清洗完成，处理了 {cleaned} 个文件")
    return cleaned


def fix_frontmatter(frontmatter):
    """修复 frontmatter 格式"""
    lines = []
    for line in frontmatter.split('\n'):
        line = line.strip()
        # 跳过空行
        if not line:
            continue
        # 确保 key: value 格式正确
        if ':' in line and not line.startswith('#'):
            lines.append(line)
    return '\n'.join(lines)


def generate_summary(docs_dir):
    """生成文档摘要统计"""
    print("\n📊 生成统计信息...")
    
    stats = {
        'total_files': 0,
        'categories': {},
        'total_lines': 0,
        'total_size': 0
    }
    
    for md_file in Path(docs_dir).rglob("*.md"):
        rel_path = md_file.relative_to(docs_dir)
        category = rel_path.parts[0] if rel_path.parts else 'root'
        
        stats['total_files'] += 1
        stats['categories'][category] = stats['categories'].get(category, 0) + 1
        
        file_size = md_file.stat().st_size
        stats['total_size'] += file_size
        
        with open(md_file, 'r', encoding='utf-8') as f:
            stats['total_lines'] += len(f.readlines())
    
    print(f"\n📈 文档统计:")
    print(f"   总文件数: {stats['total_files']}")
    print(f"   总行数: {stats['total_lines']:,}")
    print(f"   总大小: {stats['total_size'] / 1024 / 1024:.2f} MB")
    print(f"   分类数: {len(stats['categories'])}")
    print(f"\n📁 分类详情:")
    for cat, count in sorted(stats['categories'].items(), key=lambda x: -x[1]):
        print(f"   - {cat}: {count} 个文件")
    
    return stats


def regenerate_index(docs_path):
    """重新生成索引"""
    print("\n🔍 重新生成文档索引...")
    sys.path.insert(0, str(SKILL_DIR / "scripts"))
    import build_index
    # 临时修改 DOCS_DIR
    original_dir = build_index.DOCS_DIR
    build_index.DOCS_DIR = str(docs_path)
    try:
        build_index.main()
    finally:
        build_index.DOCS_DIR = original_dir


def update_skill_config(docs_path):
    """更新 skill 配置"""
    config_file = SKILL_DIR / "config.json"
    config = {
        "docs_path": str(docs_path),
        "source": "github",
        "repo": GITHUB_REPO,
        "filtered": True,
        "languages": ["en"]
    }
    
    with open(config_file, 'w', encoding='utf-8') as f:
        import json
        json.dump(config, f, indent=2)
    
    print(f"\n✅ 配置已保存: {config_file}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description='OpenClaw Docs Fetcher')
    parser.add_argument('--path', '-p', default=str(DEFAULT_CACHE_DIR), 
                       help='文档保存路径')
    parser.add_argument('--force', '-f', action='store_true',
                       help='强制重新拉取，覆盖现有文档')
    parser.add_argument('--skip-clean', action='store_true',
                       help='跳过内容清洗')
    args = parser.parse_args()
    
    print("🦞 OpenClaw Docs Fetcher")
    print("=" * 50)
    
    # 检查 git
    if not check_git():
        print("❌ 错误: 未找到 git 命令")
        print("   请先安装 Git: https://git-scm.com/")
        sys.exit(1)
    
    # 确定目标目录
    target_dir = Path(args.path)
    
    # 检查是否已存在
    if target_dir.exists() and not args.force:
        index_file = target_dir / "index.md"
        if index_file.exists():
            print(f"\n✅ 文档已存在: {target_dir}")
            print("   使用 --force 重新拉取")
            
            # 更新配置
            update_skill_config(target_dir)
            
            # 询问是否重新生成索引
            if sys.stdin.isatty():
                regen = input("\n是否重新生成索引? [y/N]: ").strip().lower()
                if regen == 'y':
                    regenerate_index(target_dir)
            return
    
    try:
        # 1. 拉取文档
        docs_path = sparse_clone_docs(target_dir)
        
        # 2. 过滤语言
        remove_non_english_docs(docs_path)
        
        # 3. 清洗内容（可选）
        if not args.skip_clean:
            clean_documentation(docs_path)
        else:
            print("\n⏭️  跳过内容清洗")
        
        # 4. 生成统计
        generate_summary(docs_path)
        
        # 5. 更新配置
        update_skill_config(docs_path)
        
        # 6. 生成索引
        regenerate_index(docs_path)
        
        print("\n" + "=" * 50)
        print("🎉 文档获取完成！")
        print(f"📚 文档位置: {docs_path}")
        print("\n现在可以使用了:")
        print("   python scripts/search-docs.py 'multi-agent'")
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
