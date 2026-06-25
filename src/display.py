"""
展示模块 - 格式化输出筛选结果
支持表格、详细信息、课程展示三种模式
"""
import re
from typing import Any


# ANSI 颜色代码
class Colors:
    HEADER = "\033[1;36m"       # 粗体青色
    SCHOOL = "\033[1;33m"       # 粗体黄色
    MAJOR = "\033[1;32m"        # 粗体绿色
    SCORE = "\033[1;35m"        # 粗体洋红
    LABEL = "\033[1;37m"        # 粗体白色
    DIM = "\033[2;37m"          # 暗灰色
    RESET = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def _pad(text: str, width: int, align: str = "left") -> str:
    """
    中英文混排字符串填充
    中文字符宽度按2计算，英文按1计算
    """
    text_str = str(text)
    # 计算显示宽度（中文全角字符占2）
    display_width = sum(2 if ord(c) > 127 else 1 for c in text_str)

    if display_width >= width:
        return text_str

    padding = width - display_width
    if align == "left":
        return text_str + " " * padding
    elif align == "right":
        return " " * padding + text_str
    else:  # center
        left = padding // 2
        right = padding - left
        return " " * left + text_str + " " * right


def _truncate(text: str, width: int) -> str:
    """截断文本以适应指定宽度"""
    text_str = str(text)
    display_width = 0
    result = []
    for c in text_str:
        cw = 2 if ord(c) > 127 else 1
        if display_width + cw > width - 1:  # 留一个字符给省略号
            result.append("…")
            break
        display_width += cw
        result.append(c)
    return "".join(result)


def _match_major_category(major_name: str, courses: dict) -> str | None:
    """根据专业名称匹配课程分类"""
    # 按优先级匹配
    patterns = [
        (r"计算机|软件|网络|人工智能|信息安全|数据科学", "计算机类"),
        (r"软件", "软件工程"),
        (r"电子|通信|信息工程|集成电路|微电子|电磁场|遥感|光电", "电子信息类"),
        (r"电气|电网", "电气类"),
        (r"自动[化控]|机器人|智能制造|测控", "自动化类"),
        (r"机械|车辆|工业工程|工业设计", "机械类"),
        (r"航空|航天|飞行器", "航空航天类"),
        (r"临床|口腔|医学|医[学药]", "临床医学类"),
        (r"数学|统计|数据科学", "数学类"),
        (r"物理", "物理学类"),
        (r"化学|化工", "化学类"),
        (r"药学|药物|制药", "药学类"),
        (r"食品", "食品科学与工程"),
        (r"土木|建筑|桥梁|给排水", "土木类"),
        (r"材料|高分子|功能材料", "材料类"),
        (r"能源|动力|储能|新能源|核[工能电]", "能源动力类"),
        (r"经济|金融|财政|会计|财务|工商管理|市场|管理科学", "经济学类"),
        (r"管理科学|信息管理|工程管理|大数据管理|项目管理|物流", "管理科学与工程类"),
        (r"金融工程|金融学|投资", "金融学"),
        (r"生物工程|生物技术", "生物工程类"),
        (r"海洋|船舶", "海洋工程类"),
        (r"法学|法律", "法学"),
        (r"核[工能电]|反应堆", "核工程类"),
    ]

    for pattern, category in patterns:
        if re.search(pattern, major_name):
            if category in courses:
                return category

    # 回退：尝试包含匹配
    for cat_name in courses:
        if cat_name in major_name:
            return cat_name

    return None


def print_summary_table(records: list[dict]) -> None:
    """打印汇总表格"""
    if not records:
        print(f"{Colors.DIM}没有找到符合条件的录取记录。{Colors.RESET}")
        return

    # 列宽定义
    col_widths = {
        "school": 22,
        "group": 8,
        "major": 36,
        "score": 7,
        "rank": 8,
        "req": 12,
    }

    # 表头
    header = (
        f"{Colors.HEADER}{Colors.BOLD}"
        f"{_pad('学校', col_widths['school'])}"
        f"{_pad('专业组', col_widths['group'])}"
        f"{_pad('专业名称', col_widths['major'])}"
        f"{_pad('最低分', col_widths['score'], 'right')}"
        f"{_pad('最低位次', col_widths['rank'], 'right')}"
        f"{_pad('选科要求', col_widths['req'])}"
        f"{Colors.RESET}"
    )

    # 分隔线
    total_width = sum(col_widths.values())
    separator = Colors.DIM + "─" * total_width + Colors.RESET

    print(f"\n{separator}")
    print(header)
    print(separator)

    # 数据行
    for i, r in enumerate(records):
        # 交替行颜色
        row_color = "" if i % 2 == 0 else Colors.DIM

        school_display = f"{Colors.SCHOOL}{_truncate(r['school'], col_widths['school'])}{Colors.RESET}"
        group_display = f"{_pad(r['group_code'], col_widths['group'])}"
        major_display = f"{Colors.MAJOR}{_truncate(r['major_name'], col_widths['major'])}{Colors.RESET}"
        score_display = f"{Colors.SCORE}{_pad(str(r['min_score']), col_widths['score'], 'right')}{Colors.RESET}"
        rank_display = f"{_pad(str(r['min_rank']), col_widths['rank'], 'right')}"
        req_display = f"{_pad(r.get('sub_requirement', ''), col_widths['req'])}"

        row = (
            f"{row_color}"
            f"{school_display}"
            f"{group_display}"
            f"{major_display}"
            f"{score_display}"
            f"{rank_display}"
            f"{req_display}"
            f"{Colors.RESET}"
        )
        print(row)

    print(separator)
    print(f"{Colors.LABEL}共 {len(records)} 条记录{Colors.RESET}\n")


def print_detailed_info(
    records: list[dict],
    schools_info: dict,
    courses: dict | None = None,
    show_courses: bool = False,
) -> None:
    """打印详细信息（学校+专业详情+可选课程）"""
    if not records:
        print(f"{Colors.DIM}没有找到符合条件的录取记录。{Colors.RESET}")
        return

    # 按学校分组
    from collections import defaultdict
    schools = defaultdict(list)
    for r in records:
        schools[r["school"]].append(r)

    for school_name in sorted(schools.keys()):
        school_records = schools[school_name]
        info = schools_info.get(school_name, {})

        # 学校名和分隔线
        print(f"\n{Colors.BOLD}{'═' * 80}{Colors.RESET}")
        print(f"\n{Colors.SCHOOL}{Colors.BOLD}🏫 {school_name}{Colors.RESET}")

        # 学校信息
        if info:
            print(f"  {Colors.LABEL}类型：{Colors.RESET}{info.get('type', '未知')}")
            print(f"  {Colors.LABEL}所在地：{Colors.RESET}{info.get('location', '未知')}")
            print(f"  {Colors.LABEL}简介：{Colors.RESET}{info.get('description', '暂无')}")
            if info.get("notable_disciplines"):
                print(f"  {Colors.LABEL}优势学科：{Colors.RESET}{', '.join(info['notable_disciplines'])}")
            if info.get("website"):
                print(f"  {Colors.LABEL}官网：{Colors.RESET}{info['website']}")

        # 专业列表
        print(f"\n  {Colors.UNDERLINE}该分数段录取专业：{Colors.RESET}")
        for r in sorted(school_records, key=lambda x: x.get("min_rank", float("inf"))):
            group_info = f" [{r['group_code']}]" if r.get("group_code") else ""
            note = f" ({r['group_note']})" if r.get("group_note") else ""
            print(f"    {Colors.MAJOR}◆ {r['major_name']}{Colors.RESET}{group_info}{Colors.DIM}{note}{Colors.RESET}")
            print(f"      最低分: {Colors.SCORE}{r['min_score']}{Colors.RESET}  |  "
                  f"最低位次: {Colors.SCORE}{r['min_rank']}{Colors.RESET}  |  "
                  f"选科要求: {r.get('sub_requirement', '无')}")
            if r.get("major_detail"):
                print(f"      {Colors.DIM}{r['major_detail']}{Colors.RESET}")

            # 课程信息
            if show_courses and courses:
                category = _match_major_category(r["major_name"], courses)
                # 也用 major_detail 辅助匹配
                if category is None and r.get("major_detail"):
                    category = _match_major_category(r["major_detail"], courses)

                if category:
                    course_info = courses[category]
                    print(f"      {Colors.LABEL}📚 课程体系（{category}）：{Colors.RESET}")
                    print(f"      {Colors.LABEL}学位/学制：{Colors.RESET}"
                          f"{course_info.get('degree', '未知')} / {course_info.get('duration', '未知')}")

                    # 核心课程（显示前8门）
                    core = course_info.get("core_courses", [])
                    if core:
                        core_names = [c["name"] if isinstance(c, dict) else c for c in core[:8]]
                        print(f"      {Colors.LABEL}核心课程：{Colors.RESET}{'、'.join(core_names)}")
                        if len(core) > 8:
                            print(f"      {Colors.DIM}        ...共{len(core)}门核心课程{Colors.RESET}")

                    # 选修课程（显示前5门）
                    elective = course_info.get("elective_courses", [])
                    if elective:
                        elec_names = [c["name"] if isinstance(c, dict) else c for c in elective[:5]]
                        print(f"      {Colors.LABEL}选修课程：{Colors.RESET}{'、'.join(elec_names)}")
                        if len(elective) > 5:
                            print(f"      {Colors.DIM}        ...共{len(elective)}门选修课程{Colors.RESET}")

                    # 典型学期安排（摘要）
                    plan = course_info.get("typical_semester_plan", {})
                    if plan:
                        semesters = list(plan.keys())[:4]  # 显示前4个学期
                        print(f"      {Colors.LABEL}前四学期：{Colors.RESET}")
                        for sem in semesters:
                            courses_list = plan[sem]
                            courses_str = "、".join(courses_list[:3])
                            if len(courses_list) > 3:
                                courses_str += f"等{len(courses_list)}门"
                            print(f"        {Colors.DIM}{sem}：{Colors.RESET}{courses_str}")
                else:
                    print(f"      {Colors.DIM}（暂无匹配的课程信息）{Colors.RESET}")

        print()

    print(f"{Colors.BOLD}{'═' * 80}{Colors.RESET}")


def export_csv(records: list[dict], filepath: str) -> None:
    """导出为 CSV 文件"""
    import csv
    if not records:
        print("没有数据可导出。")
        return

    fieldnames = ["school", "group_code", "group_note", "major_name", "major_detail",
                  "min_score", "min_rank", "sub_requirement", "category", "year", "province"]

    with open(filepath, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(records)

    print(f"已导出 {len(records)} 条记录到 {filepath}")


def export_json(records: list[dict], filepath: str) -> None:
    """导出为 JSON 文件"""
    if not records:
        print("没有数据可导出。")
        return

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    print(f"已导出 {len(records)} 条记录到 {filepath}")


import json  # noqa: E402 (already imported in loader, need here for export_json)
