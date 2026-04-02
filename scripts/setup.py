#!/usr/bin/env python3
"""
OpenClaw Docs Skill - 安装向导
智能检测、拉取、过滤、清洗文档
"""

import os
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(SKILL_DIR / "scripts"))


def check_existing_docs():
    """检查是否已有文档"""
    # 检查配置
    config_file = SKILL_DIR / "config.json"
    if config_file.exists():
        import json
        with open(config_file, 'r') as f:
            config = json.load(f)
            docs_path = config.get('docs_path')
            if docs_path and Path(docs_path).exists():
                return docs_path
    
    # 检查默认位置
    possible_paths = [
        Path.home() / ".openclaw" / "docs-cache",
        Path.home() / "openclaw-docs",
        Path.home() / "my-github" / "openclaw" / "docs",
        "/Users/su/my-github/openclaw-zh/docs",
    ]
    
    for path in possible_paths:
        if path.exists() and (path / "index.md").exists():
            return str(path)
    
    return None


def main():
    print("🦞 OpenClaw Docs Skill - 安装向导")
    print("=" * 50)
    
    # 1. 检查现有文档
    existing = check_existing_docs()
    if existing:
        print(f"\n✅ 找到现有文档: {existing}")
        use_existing = input("是否使用现有文档? [Y/n]: ").strip().lower()
        if use_existing in ('', 'y', 'yes'):
            # 更新配置
            import json
            config = {
                "docs_path": existing,
                "source": "local"
            }
            with open(SKILL_DIR / "config.json", 'w') as f:
                json.dump(config, f, indent=2)
            print(f"✅ 配置已更新")
            
            # 生成索引
            print("\n🔍 生成文档索引...")
            import build_index
            build_index.build_index()
            
            print("\n🎉 安装完成！")
            return
    
    # 2. 拉取新文档
    print("\n📥 从 GitHub 拉取文档...")
    print("   将自动执行:")
    print("   1. Sparse checkout (只拉取 docs/)")
    print("   2. 过滤非英文文档")
    print("   3. 清洗文档内容")
    print("   4. 生成索引")
    print()
    
    confirm = input("继续? [Y/n]: ").strip().lower()
    if confirm in ('', 'y', 'yes'):
        # 运行 fetch-docs.py
        import subprocess
        subprocess.run([sys.executable, str(SKILL_DIR / "scripts" / "fetch-docs.py")])
    else:
        print("\n已取消")
        print("\n手动安装方式:")
        print("   1. git clone https://github.com/openclaw/openclaw.git")
        print("   2. 创建 config.json 指定 docs_path")
        print("   3. 运行 build-index.py")


if __name__ == "__main__":
    main()
