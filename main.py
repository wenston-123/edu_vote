#!/usr/bin/env python3
"""
山西高考物理类录取数据查询工具

默认查询：2025年山西物理类位次4000-5000名的录取学校和专业
支持自定义省份、科类、年份、位次范围筛选
支持查看学校/专业详细信息、课程信息
支持导出为 CSV/JSON
"""
import argparse
import sys
import os

# 将项目根目录加入 path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.loader import load_all_data
from src.filter_engine import (
    FilterCriteria,
    flatten_admission_records,
    filter_records,
    get_statistics,
)
from src.display import (
    print_summary_table,
    print_detailed_info,
    export_csv,
    export_json,
    Colors,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="山西高考物理类录取数据查询工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例：
  python main.py                              # 默认查询：山西物理类4000-6000名(2025)
  python main.py --detail                     # 显示学校和专业详细信息
  python main.py --courses                    # 显示课程信息（需配合 --detail）
  python main.py --detail --courses           # 显示全部信息（学校+专业+课程）
  python main.py --rank-min 3000 --rank-max 6000   # 自定义位次范围
  python main.py --school 重庆                # 按学校名筛选
  python main.py --major 计算机               # 按专业关键词筛选
  python main.py --export results.csv         # 导出为CSV
  python main.py --export results.json        # 导出为JSON
  python main.py --stats                      # 仅显示统计信息
        """,
    )
    parser.add_argument("--province", default="山西", help="省份（默认：山西）")
    parser.add_argument("--category", default="物理类", help="科类（默认：物理类）")
    parser.add_argument("--year", type=int, default=2025, help="年份（默认：2025）")
    parser.add_argument("--rank-min", type=int, default=4000, help="最低位次（默认：4000）")
    parser.add_argument("--rank-max", type=int, default=6000, help="最高位次（默认：6000）")
    parser.add_argument("--school", help="按学校名筛选（模糊匹配）")
    parser.add_argument("--major", help="按专业关键词筛选（模糊匹配）")
    parser.add_argument("--detail", action="store_true", help="显示学校和专业详细信息")
    parser.add_argument("--courses", action="store_true", help="显示课程信息（需配合 --detail）")
    parser.add_argument("--export", help="导出文件路径（支持 .csv / .json）")
    parser.add_argument("--stats", action="store_true", help="仅显示统计信息")
    return parser.parse_args()


def main():
    args = parse_args()

    # 1. 加载数据
    print(f"{Colors.DIM}正在加载数据...{Colors.RESET}")
    try:
        admission_data, schools_info, courses = load_all_data(year=args.year)
    except FileNotFoundError as e:
        print(f"{Colors.SCHOOL}错误：{e}{Colors.RESET}")
        sys.exit(1)

    print(f"{Colors.DIM}已加载 {len(admission_data)} 个院校专业组数据{Colors.RESET}")

    # 2. 展开记录
    records = flatten_admission_records(admission_data)
    print(f"{Colors.DIM}已展开为 {len(records)} 条专业录取记录{Colors.RESET}")

    # 3. 筛选
    criteria = FilterCriteria(
        province=args.province,
        category=args.category,
        year=args.year,
        rank_min=args.rank_min,
        rank_max=args.rank_max,
        school=args.school,
        major_keyword=args.major,
    )

    filtered = filter_records(records, criteria)

    # 4. 统计
    stats = get_statistics(filtered)

    # 打印筛选条件
    print(f"\n{Colors.BOLD}📋 筛选条件：{Colors.RESET}")
    print(f"  省份: {args.province}  |  科类: {args.category}  |  "
          f"年份: {args.year}  |  位次: {args.rank_min}-{args.rank_max}")
    if args.school:
        print(f"  学校关键词: {args.school}")
    if args.major:
        print(f"  专业关键词: {args.major}")

    # 打印统计信息
    print(f"\n{Colors.BOLD}📊 筛选结果统计：{Colors.RESET}")
    print(f"  共 {stats['count']} 条专业录取记录，来自 {stats['school_count']} 所院校")
    if stats["count"] > 0:
        print(f"  分数区间: {stats['score_range'][0]}-{stats['score_range'][1]} 分")
        print(f"  位次区间: {stats['rank_range'][0]}-{stats['rank_range'][1]} 名")
        print(f"  涉及院校: {'、'.join(stats['schools'])}")

    # 5. 输出
    if args.stats:
        # 仅统计模式
        return

    if args.detail:
        print_detailed_info(
            filtered,
            schools_info,
            courses=courses,
            show_courses=args.courses,
        )
    else:
        print_summary_table(filtered)

    # 6. 导出
    if args.export:
        filepath = args.export
        if filepath.endswith(".json"):
            export_json(filtered, filepath)
        else:
            export_csv(filtered, filepath)


if __name__ == "__main__":
    main()
