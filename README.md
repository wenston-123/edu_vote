# Gaokao Report Generator

高考录取数据 PDF 报告生成器 —— 将官方录取数据转化为结构化的、可读性强的 PDF 分析报告。

## 功能

- 📊 按位次区间筛选全部录取专业，生成全景总览表
- ⭐ 重点位次区间四维深度解读（专业概述·培养方向·就业前景·位次策略）
- 🏫 每所院校含：学校简介、优势学科、招生办电话、专业录取表
- 📚 自动匹配课程体系（核心课程·选修方向·学期安排）
- 💡 填报策略框架（品牌优先/专业优先/产业风口/稳妥保底/城市优先）

## 快速开始

```bash
# 默认参数（山西 物理类 2025 年 4000-6000 名，重点 4600-5300）
./run.sh

# 自定义参数
./run.sh \
  --province 山西 --category 物理类 --year 2025 \
  --rank-min 3000 --rank-max 6000 \
  --highlight-min 3500 --highlight-max 4500

# 指定输出文件
./run.sh --output 我的报告.pdf
```

## 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--province` | 山西 | 省份名称 |
| `--category` | 物理类 | 科类（物理类/历史类） |
| `--year` | 2025 | 高考年份 |
| `--rank-min` | 4000 | 位次区间下限 |
| `--rank-max` | 6000 | 位次区间上限 |
| `--highlight-min` | 4600 | 重点位次区间下限 |
| `--highlight-max` | 5300 | 重点位次区间上限 |
| `--output` | 自动生成 | 输出 PDF 路径 |

## 报告结构

```
一、数据总览        —— 全景总览表 + 分数段分布 + 梯度分析
二、各院校专业详情    —— 每校逐一详解（含招办电话、课程体系）
三、⭐ 重点推荐区间   —— 四维深度解读（概述/培养/就业/策略）
四、保底区间详解      —— 逐校逐专业详解
五、填报策略建议      —— 五种决策框架
六、数据说明          —— 免责声明
```

## 数据格式

### admission_2025.json
```json
[{
  "province": "山西",
  "category": "物理类",
  "year": 2025,
  "school": "学校名称",
  "group_code": "第301组",
  "group_note": "国家专项计划",
  "sub_requirement": "物理+化学",
  "majors": [
    {"major_name": "专业名称", "major_detail": "方向说明",
     "min_score": 631, "min_rank": 4000}
  ]
}]
```

### schools_info.json
```json
{
  "学校名称": {
    "full_name": "全称",
    "type": "985/211/双一流A类",
    "category": "理工类",
    "location": "北京市",
    "website": "https://...",
    "description": "学校简介",
    "notable_disciplines": ["学科（评级）"]
  }
}
```

### courses.json
按专业大类组织的课程体系，含核心课程、选修课程、典型学期安排。

## 项目结构

```
├── run.sh                  # 入口脚本
├── generate_pdf.py         # PDF 生成器（主程序）
├── main.py                 # 终端查询工具
├── data/
│   ├── admission_2025.json # 录取数据
│   ├── schools_info.json   # 学校信息
│   ├── courses.json        # 课程数据
│   └── contacts.json       # 联系方式
├── src/                    # 查询工具模块
└── output/                 # PDF 输出目录
```

## 依赖

- Python 3.10+
- [reportlab](https://pypi.org/project/reportlab/)

## License

MIT
