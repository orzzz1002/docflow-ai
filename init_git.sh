#!/bin/bash
# DocFlow AI - Git 初始化脚本
# 使用方法：./init_git.sh

set -e

echo "🚀 初始化 DocFlow AI Git 仓库..."

# 检查是否在正确的目录
if [ ! -f "README.md" ]; then
    echo "❌ 错误：请在 docflow-ai 项目根目录运行此脚本"
    exit 1
fi

# 初始化 Git 仓库
echo "📦 初始化 Git 仓库..."
git init

# 创建 .gitignore
cat > .gitignore << EOF
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
.venv/
venv/
ENV/
env/
*.egg-info/
dist/
build/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# 环境变量
.env

# 日志
logs/
*.log

# 操作系统
.DS_Store
Thumbs.db

# 测试
.pytest_cache/
.coverage
htmlcov/

# 模型文件
models/*.bin
models/*.pt
models/*.h5
EOF

# 添加所有文件
echo "📝 添加文件到 Git..."
git add .

# 首次提交
echo "💾 创建首次提交..."
git commit -m "Initial commit: DocFlow AI v1.0.0

- 多 Agent 协作架构（5 个专用 Agent）
- 长链推理引擎（10+ 步推理链）
- FastAPI REST API
- Web UI 演示界面
- 完整的文档和配置

Author: 吴金永 <your-email@example.com>
Team: 我的 AI 团队"

echo ""
echo "✅ Git 仓库初始化完成！"
echo ""
echo "下一步操作："
echo "1. 在 GitHub 创建新仓库：docflow-ai"
echo "2. 运行以下命令推送代码："
echo ""
echo "   git remote add origin https://github.com/YOUR_USERNAME/docflow-ai.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "或者使用 SSH："
echo "   git remote add origin git@github.com:YOUR_USERNAME/docflow-ai.git"
echo "   git push -u origin main"
echo ""
