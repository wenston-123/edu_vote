"""
筛选引擎 - 支持多条件组合筛选录取数据
"""
from dataclasses import dataclass


@dataclass
class FilterCriteria:
    """筛选条件"""
    province: str = "山西"
    category: str = "物理类"
    year: int = 2025
    rank_min: int = 4000
    rank_max: int = 5000
    school: str | None = None          # 按学校名筛选（模糊匹配）
    major_keyword: str | None = None   # 按专业关键词筛选（模糊匹配）


def flatten_admission_records(admission_data: list[dict]) -> list[dict]:
    """
    将嵌套的录取数据展开为扁平记录列表
    每个专业组下的每个专业展开为一条独立记录
    """
    records = []
    for entry in admission_data:
        base = {
            "school": entry["school"],
            "group_code": entry["group_code"],
            "group_note": entry.get("group_note", ""),
            "category": entry["category"],
            "sub_requirement": entry.get("sub_requirement", ""),
            "year": entry["year"],
            "province": entry["province"],
        }
        for major in entry.get("majors", []):
            record = base.copy()
            record["major_name"] = major["major_name"]
            record["major_detail"] = major.get("major_detail", "")
            record["min_score"] = major["min_score"]
            record["min_rank"] = major["min_rank"]
            records.append(record)
    return records


def filter_records(
    records: list[dict],
    criteria: FilterCriteria,
) -> list[dict]:
    """
    根据筛选条件过滤录取记录

    :param records: 展开后的录取记录列表
    :param criteria: 筛选条件
    :return: 符合条件的记录列表，按位次升序排列
    """
    result = []
    for r in records:
        # 省份筛选
        if criteria.province and r.get("province") != criteria.province:
            continue

        # 科类筛选
        if criteria.category and r.get("category") != criteria.category:
            continue

        # 年份筛选
        if criteria.year and r.get("year") != criteria.year:
            continue

        # 位次范围筛选
        rank = r.get("min_rank")
        if rank is not None:
            if criteria.rank_min is not None and rank < criteria.rank_min:
                continue
            if criteria.rank_max is not None and rank > criteria.rank_max:
                continue

        # 学校名筛选（模糊匹配）
        if criteria.school and criteria.school not in r.get("school", ""):
            continue

        # 专业关键词筛选（模糊匹配）
        if criteria.major_keyword:
            major_name = r.get("major_name", "")
            major_detail = r.get("major_detail", "")
            kw = criteria.major_keyword
            if kw not in major_name and kw not in major_detail:
                continue

        result.append(r)

    # 按位次升序排列
    result.sort(key=lambda x: x.get("min_rank", float("inf")))
    return result


def get_statistics(records: list[dict]) -> dict:
    """获取筛选结果的统计信息"""
    if not records:
        return {"count": 0}

    schools = set(r["school"] for r in records)
    ranks = [r["min_rank"] for r in records]
    scores = [r["min_score"] for r in records]

    return {
        "count": len(records),
        "school_count": len(schools),
        "schools": sorted(schools),
        "rank_range": (min(ranks), max(ranks)),
        "score_range": (min(scores), max(scores)),
    }
