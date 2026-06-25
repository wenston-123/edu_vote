#!/usr/bin/env bash
#===========================================================================
# 高考录取数据 PDF 报告生成器
#
# 用法:
#   ./run.sh                                    # 默认参数
#   ./run.sh --rank-min 3000 --rank-max 5000    # 自定义位次
#   ./run.sh --province 广东 --category 历史类  # 自定义省份科类
#===========================================================================
set -euo pipefail

cd "$(dirname "$0")"

# 检查依赖
python3 -c "import reportlab" 2>/dev/null || {
    echo "📦 正在安装依赖 reportlab ..."
    pip3 install reportlab -q
}

# 确保输出目录存在
mkdir -p output

# 执行生成（透传所有参数）
echo "🚀 启动报告生成..."
python3 generate_pdf.py "$@"

echo "📂 报告保存在 output/ 目录下"
