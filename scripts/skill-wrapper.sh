#!/bin/bash
# OpenClaw Docs Skill - Wrapper Script
# 一键执行常用操作

set -e

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SCRIPTS_DIR="$SKILL_DIR/scripts"
CACHE_DIR="${HOME}/.openclaw/docs-cache"

cd "$SKILL_DIR"

show_help() {
    cat << EOF
OpenClaw Docs Skill - 命令行工具

用法: ./scripts/skill-wrapper.sh <命令>

命令:
  setup         首次安装/配置
  sync          同步最新文档
  search <词>   搜索文档
  index         重新生成索引
  stats         显示统计信息
  clean         清理缓存

示例:
  ./scripts/skill-wrapper.sh setup
  ./scripts/skill-wrapper.sh search "multi-agent"
  ./scripts/skill-wrapper.sh sync && ./scripts/skill-wrapper.sh index

EOF
}

cmd_setup() {
    echo "🔧 开始安装配置..."
    python3 "$SCRIPTS_DIR/setup.py"
}

cmd_sync() {
    echo "🔄 同步最新文档..."
    python3 "$SCRIPTS_DIR/fetch-docs.py"
}

cmd_search() {
    local query="${1:-}"
    if [ -z "$query" ]; then
        echo "❌ 请提供搜索词"
        echo "用法: skill-wrapper.sh search <关键词>"
        exit 1
    fi
    echo "🔍 搜索: $query"
    python3 "$SCRIPTS_DIR/search-docs.py" "$query"
}

cmd_index() {
    echo "📊 重新生成索引..."
    python3 "$SCRIPTS_DIR/build-index.py"
}

cmd_stats() {
    echo "📈 文档统计"
    echo "============"
    
    if [ -d "$CACHE_DIR" ]; then
        local file_count=$(find "$CACHE_DIR" -name "*.md" | wc -l)
        local total_size=$(du -sh "$CACHE_DIR" | cut -f1)
        local line_count=$(find "$CACHE_DIR" -name "*.md" -exec cat {} \; | wc -l)
        
        echo "📁 缓存位置: $CACHE_DIR"
        echo "📄 文档数量: $file_count"
        echo "📏 总行数: $line_count"
        echo "💾 总大小: $total_size"
        
        echo ""
        echo "📂 分类统计:"
        find "$CACHE_DIR" -mindepth 1 -maxdepth 1 -type d | while read dir; do
            local name=$(basename "$dir")
            local count=$(find "$dir" -name "*.md" | wc -l)
            printf "  %-20s %3d 个文件\n" "$name:" $count
        done
    else
        echo "❌ 文档缓存不存在，请先运行: ./scripts/skill-wrapper.sh setup"
    fi
}

cmd_clean() {
    echo "🧹 清理缓存..."
    if [ -d "$CACHE_DIR" ]; then
        rm -rf "$CACHE_DIR"
        echo "✅ 已清理: $CACHE_DIR"
    else
        echo "⚠️ 缓存目录不存在"
    fi
}

# 主入口
main() {
    local cmd="${1:-}"
    
    case "$cmd" in
        setup)
            cmd_setup
            ;;
        sync)
            cmd_sync
            ;;
        search)
            shift
            cmd_search "$@"
            ;;
        index)
            cmd_index
            ;;
        stats)
            cmd_stats
            ;;
        clean)
            cmd_clean
            ;;
        help|--help|-h|"")
            show_help
            ;;
        *)
            echo "❌ 未知命令: $cmd"
            show_help
            exit 1
            ;;
    esac
}

main "$@"
