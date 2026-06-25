"""
数据加载模块 - 统一加载和管理 JSON 数据文件
"""
import json
import os
from typing import Any


DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


def _load_json(filename: str) -> Any:
    """加载 JSON 数据文件"""
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"数据文件不存在: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def load_admission_data(year: int | None = None) -> list[dict]:
    """
    加载录取数据
    :param year: 指定年份，None 则加载所有年份数据
    :return: 录取记录列表
    """
    data = _load_json("admission_2025.json")
    if year is not None:
        data = [r for r in data if r.get("year") == year]
    return data


def load_schools_info() -> dict:
    """加载学校详细信息"""
    return _load_json("schools_info.json")


def load_courses() -> dict:
    """加载课程信息"""
    return _load_json("courses.json")


def load_all_data(year: int | None = None) -> tuple[list[dict], dict, dict]:
    """
    一次性加载所有数据
    :return: (admission_data, schools_info, courses)
    """
    return (
        load_admission_data(year),
        load_schools_info(),
        load_courses(),
    )
