# -*- coding: utf-8 -*-
"""
香水推荐筛选脚本
用途：读取 Scento 香水数据集，按香族分组，挑出知名度最高的一批香水，
      方便人工筛选出适合放进"香调人格测试"结果页的推荐款。

数据来源：https://github.com/Scento-com/perfume-dataset (CC BY 4.0)
数据文件：D:\香调人格项目\perfumes.csv
输出文件：D:\香调人格项目\香族香水清单.md
"""

import csv
import collections
import os

CSV_PATH = r"D:\香调人格项目\perfumes.csv"
OUT_PATH = r"D:\香调人格项目\香族香水清单.md"
TOP_N = 15  # 每个香族输出前多少支


def main():
    with open(CSV_PATH, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    by_family = collections.defaultdict(list)
    for r in rows:
        fam = (r.get("family") or "").strip()
        if not fam:
            continue
        rank_txt = (r.get("popularity_rank") or "").strip()
        # popularity_rank: 1 = 最知名；没有排名的排到最后
        r["_rank"] = int(rank_txt) if rank_txt.isdigit() else 99999
        by_family[fam].append(r)

    lines = []
    lines.append("# 香族香水清单（按知名度排序）\n")
    lines.append("> 数据来源：Scento Perfume Database，CC BY 4.0\n")
    lines.append("> popularity_rank 数字越小 = 越知名\n")

    # 按香族规模从大到小输出
    for fam, items in sorted(by_family.items(), key=lambda x: -len(x[1])):
        items.sort(key=lambda r: r["_rank"])
        lines.append(f"\n## {fam}（共 {len(items)} 支）\n")
        lines.append("| 排名 | 香水 | 品牌 | 浓度 | 年份 | 前调 | 中调 | 后调 |")
        lines.append("|---|---|---|---|---|---|---|---|")

        shown = 0
        for r in items:
            if shown >= TOP_N:
                break
            shown += 1
            rank = r["_rank"] if r["_rank"] != 99999 else "-"

            def cut(s, n=40):
                s = (s or "").strip()
                return s[:n] + ("…" if len(s) > n else "")

            lines.append(
                "| {rank} | {name} | {house} | {conc} | {year} | {top} | {heart} | {base} |".format(
                    rank=rank,
                    name=cut(r.get("name"), 30).replace("|", "/"),
                    house=cut(r.get("house"), 20).replace("|", "/"),
                    conc=cut((r.get("concentration") or "").replace("-", " "), 12),
                    year=(r.get("year") or "-").strip(),
                    top=cut(r.get("top_notes"), 30).replace("|", "/"),
                    heart=cut(r.get("heart_notes"), 30).replace("|", "/"),
                    base=cut(r.get("base_notes"), 30).replace("|", "/"),
                )
            )

    text = "\n".join(lines)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"已生成：{OUT_PATH}")
    print(f"共 {len(rows)} 支香水，{len(by_family)} 个香族")


if __name__ == "__main__":
    main()
