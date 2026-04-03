#!/bin/bash
# OpenClaw Docs Skill - Validation Script
# 验证 Skill 结构是否符合规范

set -e

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
ERRORS=0

echo "🔍 验证 OpenClaw Docs Skill 结构"
echo "================================"

# 检查必需文件
check_file() {
    local file="$1"
    local required="$2"
    
    if [ -f "$SKILL_DIR/$file" ]; then
        echo "✅ $file"
        return 0
    else
        if [ "$required" = "required" ]; then
            echo "❌ $file (必需)"
            ERRORS=$((ERRORS + 1))
        else
            echo "⚠️  $file (可选)"
        fi
        return 1
    fi
}

# 检查必需目录
check_dir() {
    local dir="$1"
    if [ -d "$SKILL_DIR/$dir" ]; then
        echo "✅ $dir/"
    else
        echo "⚠️  $dir/ (可选)"
    fi
}

echo ""
echo "📄 必需文件:"
check_file "SKILL.md" "required"
check_file "README.md" "optional"

echo ""
echo "📁 目录结构:"
check_dir "scripts"
check_dir "references"
check_dir "assets"

echo ""
echo "🔧 脚本文件:"
if [ -d "$SKILL_DIR/scripts" ]; then
    for script in fetch-docs.py search-docs.py build-index.py setup.py; do
        check_file "scripts/$script" "optional"
    done
fi

echo ""
echo "📝 SKILL.md 检查:"
if [ -f "$SKILL_DIR/SKILL.md" ]; then
    # 检查 frontmatter
    if head -10 "$SKILL_DIR/SKILL.md" | grep -q "^---"; then
        echo "✅ Frontmatter 存在"
    else
        echo "⚠️  Frontmatter 可能缺失"
    fi
    
    # 检查 name
    if grep -q "^name:" "$SKILL_DIR/SKILL.md"; then
        echo "✅ 'name' 字段存在"
    else
        echo "❌ 'name' 字段缺失"
        ERRORS=$((ERRORS + 1))
    fi
    
    # 检查 description
    if grep -q "^description:" "$SKILL_DIR/SKILL.md"; then
        echo "✅ 'description' 字段存在"
    else
        echo "❌ 'description' 字段缺失"
        ERRORS=$((ERRORS + 1))
    fi
    
    # 统计行数
    lines=$(wc -l < "$SKILL_DIR/SKILL.md")
    echo "📊 SKILL.md 行数: $lines"
    if [ "$lines" -gt 500 ]; then
        echo "⚠️  SKILL.md 过长，建议精简 (<300 行)"
    fi
fi

echo ""
echo "📚 References 检查:"
if [ -d "$SKILL_DIR/references" ]; then
    ref_count=$(find "$SKILL_DIR/references" -type f | wc -l)
    echo "✅ references/ 目录存在，包含 $ref_count 个文件"
else
    echo "⚠️  references/ 目录不存在"
fi

echo ""
echo "================================"
if [ $ERRORS -eq 0 ]; then
    echo "✅ 验证通过！"
    exit 0
else
    echo "❌ 发现 $ERRORS 个问题"
    exit 1
fi
