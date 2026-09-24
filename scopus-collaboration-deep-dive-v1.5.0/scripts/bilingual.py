"""Bilingual label generation (English + 中文).

Generates bilingual strings with 'English | 中文' format for XLSX cells
and HTML sections. Centralizes all known translations.
"""

# Region name translations
REGION_TRANSLATIONS = {
    'Stanford (source)': '斯坦福（源）',
    'Shanghai Jiao Tong (target)': '上海交大（目标）',
    'Mainland China': '中国大陆（其他）',
    'US (other top)': '美国（其他顶级大学）',
    'Hong Kong / Macau / Taiwan': '香港 / 澳门 / 台湾',
    'US (Federal/DOE)': '美国（联邦/DOE）',
    'Germany / Switzerland': '德国 / 瑞士',
    'UK': '英国',
    'Singapore': '新加坡',
    'US (National Labs)': '美国（国家实验室）',
    'Europe (physics labs)': '欧洲（物理实验室）',
    'Japan': '日本',
    'Korea': '韩国',
    'Other International': '其他国际',
    'CERN': 'CERN',
}

# Common label translations (extend as needed)
LABEL_TRANSLATIONS = {
    # Sheet / Section titles
    'Overview': '概览',
    'Top 20 Partner Institutions': 'Top 20 合作机构',
    'Top 10 Research Fields': 'Top 10 研究领域',
    'Top 10 Researchers': 'Top 10 研究者',
    'Trends & Patterns': '趋势与模式',
    'Deep Dive': '深度分析',
    'Signatures & Funding': '代表性论文与资助代理',
    'Year Range': '年份范围',
    'Total Publications': '总发表数',
    'Total Citations': '总引用',
    'Avg FWCI': '平均 FWCI',
    'Max FWCI': '最大 FWCI',
    'Distinct ASJC Fields': '独立 ASJC 领域数',
    'Distinct Institutions': '独立机构数',
    'Most Frequent Journal': '最高产期刊',
    'Papers in Top Journal': 'Top 期刊论文数',
    'Data Source': '数据来源',
    'Analysis Date': '分析日期',
    'Quick Navigation': '快速导航',
    'Note': '说明',
    'Partner Institutions': '合作机构',
    'Research Fields': '研究领域',
    'Top Researchers': 'Top 研究者',
    'Rank': '排名',
    'Institution': '机构',
    'Collaboration Papers': '合著论文',
    'Share of Total': '占总论文比例',
    'Papers (n)': '论文数',
    'ASJC Research Field': 'ASJC 研究领域',
    'Papers': '论文数',
    'Total Citations Received': '论文总引用',
    'Avg Citations / Paper': '平均引用 / 篇',
    'Avg FWCI (Field-Normalized)': '平均 FWCI (学科归一化)',
    'Avg FWVI (Field-Normalized Views)': '平均 FWVI',
    'Researcher': '研究者',
    'Citations': '引用',
    'Primary Partner Institution': '主要合作机构',
    'Core Research Field': '核心研究领域',
    'Quality Score': '质量评分',
    'Year-over-Year Trends': '年度趋势',
    'Papers Published': '发表论文数',
    'YoY Growth %': '同比增长率',
    'Average FWCI': '平均 FWCI',
    'Topic Evolution by Year': '主题年度演变',
    'Topic Rank': '主题排名',
    'Field & Institution Concentration': '学科与机构集中度',
    'Distinct Fields': '独立学科数',
    'Region Breakdown': '区域分布',
    'Affiliations': '机构署名',
    'Share': '占比',
    'Researcher Archetypes': '研究者原型',
    'Top 20 High-Impact Journals': 'Top 20 高影响期刊',
    'Metric': '指标',
    'Detail': '详情',
    'Year': '年份',
    'Scopus': 'Scopus',
    'Note on name disambiguation': '姓名消歧说明',
    # Sheet 6/7 extras
    'ASJC Major Category Breakdown': 'ASJC 主要学科大类分布',
    'Major ASJC Category': '主要学科大类',
    'Papers in Category': '该类论文数',
    'AI / Machine Learning Cluster': 'AI / 机器学习集群',
    'Cluster Definition': '集群定义',
    'H-Index Analysis': 'H 指数分析',
    'Multi-US Partnership Profile': '多美国机构合作画像',
    'Multi-US Collaboration Papers': '多美国合作论文数',
    'Stanford + Other US Partners (%)': '斯坦福 + 其他美国机构比例',
    'Top US Universities': 'Top 美国大学',
    'US University': '美国大学',
    'Co-authored Papers': '合著论文数',
    'Funding Horizon Proxies': '资助前瞻代理',
    'Top 1% Papers (by FWCI)': 'Top 1% 论文（按 FWCI）',
    'Top 5% Papers by FWCI': 'Top 5% 论文（按 FWCI）',
    'Multi-Sector Collaboration': '多区域合作',
    'Open Access Status': '开放获取状态',
    'Document Type Distribution': '文档类型分布',
    'Document Type': '文档类型',
    'Note on Funding Analysis': '资助分析说明',
    'Cluster Subfields': '集群子领域',
    'Cluster Journals': '集群期刊',
    'Cluster Top Researchers': '集群 Top 研究者',
    'Papers by Year': '年度论文数',
    'Title': '标题',
    'Journal': '期刊',
    'Notable Multi-Sector Papers': '重要多区域论文',
    'Open Access Papers': '开放获取论文',
    'H-index': 'H 指数',
    'Total Papers': '总论文数',
}


def B(en: str, zh: str) -> str:
    """Build bilingual label with pipe separator.

    Example:
        >>> B('Total Publications', '总发表数')
        'Total Publications | 总发表数'
    """
    return f"{en} | {zh}"


def translate_region(region_name: str) -> str:
    """Translate a region name to Chinese. Falls back to original if unknown."""
    return REGION_TRANSLATIONS.get(region_name, region_name)


def bilingual_region_table(regions_data: dict) -> list:
    """Build (region_en, region_zh, count) tuples for region breakdown tables.

    Args:
        regions_data: Dict mapping region name → count.

    Returns:
        List of (en_name, zh_name, count, share_pct) tuples.
    """
    total = sum(regions_data.values())
    return [(en, translate_region(en), count, count/total*100)
            for en, count in sorted(regions_data.items(), key=lambda x: -x[1])]


# Long explanatory text translations
QUALITY_SCORE_DESC = {
    'en': "Quality Score = sqrt(N_papers) × avg_FWCI × ln(1 + Total_Citations). Balances productivity, field-normalized citation impact (FWCI), and total citation reach.",
    'zh': "质量评分 = sqrt(论文数) × 平均 FWCI × ln(1 + 总引用)。平衡生产力、学科归一化引用影响 (FWCI) 和总引用覆盖度。",
}

NAME_DISAMBIGUATION_DESC = {
    'en': "Scopus author names use 'Last, Initial' format. Names like 'Wang, Y.' or 'Li, J.' may aggregate multiple distinct researchers. Institution and field analysis is based on co-author paper affiliations, so the listed primary affiliation reflects the most common institution across this researcher's co-authored papers in the dataset, not necessarily the researcher's personal affiliation.",
    'zh': "Scopus 学者姓名采用「姓, 名首字母」格式，可能聚合多个不同研究者。机构与领域分析基于合著者论文署名。",
}

AI_CLUSTER_DESC = {
    'en': "AI / ML cluster: researchers named Wang, Li, Liu, Zhang, Ma, Zhao, Chen, Tang, Sun, Cai, Hu (the most common co-author names in CS/AI papers)",
    'zh': "AI/ML 集群：合著者姓氏匹配最常见的 CS/AI 中文学者姓名（王、李、刘、张、马、赵、陈、唐、孙、蔡、胡）",
}

FILTER_DESC = {
    'en': "Papers with >50 authors excluded (removes mega-author consortium papers from physics/GBD).",
    'zh': "排除作者数 >50 的论文（剔除大型物理/医学联盟论文）。",
}