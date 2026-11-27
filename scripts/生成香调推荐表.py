# -*- coding: utf-8 -*-
"""
生成"香调人格"推荐表
用途：把 Scento 香水数据集里的 14 个香族归并成 8 个香调人格，
      每个挑选 3 支国内常见、学生熟悉、买得到的香水，生成 Markdown 表格。

数据来源：https://github.com/Scento-com/perfume-dataset (CC BY 4.0)
数据文件：D:\香调人格项目\perfumes.csv
输出文件：D:\香调人格项目\香调人格推荐表.md
"""

import csv

CSV_PATH = r"D:\香调人格项目\perfumes.csv"
OUT_PATH = r"D:\香调人格项目\香调人格推荐表.md"

# 8 个香调人格 → (对应的 Scento 原始香族, 挑选的香水[(名字, 品牌)])
# 挑选原则：知名度高 + 国内好买 + 品牌档次适合学生/年轻人
PERSONA = [
    ("阳光派 · 柑橘调", ["Sunlit Citrus"], [
        ("Acqua di Giò", "Giorgio Armani"),
        ("Pour Homme", "Versace"),
        ("Ô de Lancôme", "Lancôme"),
    ]),
    ("温柔派 · 花香调", ["White Bloom", "Petal Garden"], [
        ("Libre", "Yves Saint Laurent"),
        ("Bloom", "Gucci"),
        ("Mon Paris", "Yves Saint Laurent"),
    ]),
    ("元气派 · 果香调", ["Orchard Fruit"], [
        ("Club de Nuit Intense Man", "Armaf"),
        ("Her", "Burberry"),
        ("Daisy Eau So Fresh", "Marc Jacobs"),
    ]),
    ("独处派 · 木质调", ["Wood & Root"], [
        ("Dylan Blue", "Versace"),
        ("9 PM Night Out", "Afnan"),
        ("Tam Dao", "Diptyque"),
    ]),
    ("清透派 · 绿叶水生", ["Green Leaf", "Salt & Mineral"], [
        ("Polo Blue", "Ralph Lauren"),
        ("HUGO Man", "Hugo Boss"),
        ("Luna Rossa Carbon", "Prada"),
    ]),
    ("治愈派 · 甜香调", ["Velvet Sweet"], [
        ("Black Opium", "Yves Saint Laurent"),
        ("Khamrah", "Lattafa"),
        ("Yara", "Lattafa"),
    ]),
    ("神秘派 · 辛香东方", ["Spice Route", "Amber & Resin", "Oud Court"], [
        ("La Nuit de L'Homme", "Yves Saint Laurent"),
        ("Asad", "Lattafa"),
        ("Oud Wood", "Tom Ford"),
    ]),
    ("沉稳派 · 粉感麝香", ["Powder Veil", "Skin Musk", "Smoke & Leather"], [
        ("For Her", "Narciso Rodriguez"),
        ("Gentleman", "Givenchy"),
        ("001 Woman", "Loewe"),
    ]),
]

CONC_MAP = {
    "eau-de-parfum": "EDP 香精",
    "eau-de-toilette": "EDT 淡香",
    "eau-de-cologne": "EDC 古龙",
    "extrait": "Extrait 香精",
    "parfum": "Parfum",
}


def main():
    with open(CSV_PATH, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    # 建立 (名字, 品牌) -> 行 的索引，方便精确查找
    index = {}
    for r in rows:
        index[(r["name"].strip(), r["house"].strip())] = r

    lines = []
    lines.append("# 香调人格 · 推荐香水表\n")
    lines.append("> 数据来源：Scento Perfume Database（CC BY 4.0）— https://www.scento.com/perfume-database")
    lines.append("> 说明：价格为国内电商参考，买之前请自行核对；推荐逻辑是「知名度 + 好买 + 适合年轻人」\n")

    missing = []
    for persona_name, families, picks in PERSONA:
        lines.append(f"\n## {persona_name}\n")
        lines.append(f"*对应香族：{' + '.join(families)}*\n")
        lines.append("| 香水 | 品牌 | 浓度 | 前调 | 中调 | 后调 | 气味关键词 |")
        lines.append("|---|---|---|---|---|---|---|")

        for name, house in picks:
            r = index.get((name, house))
            if r is None:
                missing.append(f"{name} / {house}")
                lines.append(f"| ⚠️ {name} | {house} | - | - | - | - | 数据集中未找到 |")
                continue

            def cut(s, n=45):
                s = (s or "").strip()
                return s[:n] + ("…" if len(s) > n else "")

            lines.append(
                "| {name} | {house} | {conc} | {top} | {heart} | {base} | {char} |".format(
                    name=name,
                    house=house,
                    conc=CONC_MAP.get((r.get("concentration") or "").strip(), "-"),
                    top=cut(r.get("top_notes")).replace("|", "/") or "-",
                    heart=cut(r.get("heart_notes")).replace("|", "/") or "-",
                    base=cut(r.get("base_notes")).replace("|", "/") or "-",
                    char=cut(r.get("character"), 40).replace("|", "/") or "-",
                )
            )

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"已生成：{OUT_PATH}")
    if missing:
        print("找不到的香水：")
        for m in missing:
            print("  -", m)
    else:
        print("全部匹配成功")


if __name__ == "__main__":
    main()
