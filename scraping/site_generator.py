"""
スクレイピングデータから、携帯で見やすい静的HTMLサイトを生成する
"""
import os
import json
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import LATEST_JSON, SITE_DIR, SITE_INDEX

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>パチスロ情報モニター</title>
<style>
  :root {{
    --bg: #0f1115;
    --card: #1a1d24;
    --text: #e8e8ec;
    --muted: #9a9ba5;
    --plus: #ff5c5c;
    --minus: #5c9dff;
    --zero: #6b6f7a;
    --border: #2a2d36;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    background: var(--bg);
    color: var(--text);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Hiragino Sans", sans-serif;
    padding: 12px;
  }}
  header {{
    margin-bottom: 16px;
  }}
  h1 {{
    font-size: 18px;
    margin: 0 0 4px 0;
  }}
  .updated {{
    color: var(--muted);
    font-size: 12px;
  }}
  .page-block {{
    margin-bottom: 24px;
  }}
  .page-title {{
    font-size: 15px;
    font-weight: 600;
    margin: 0 0 8px 2px;
    padding-bottom: 6px;
    border-bottom: 1px solid var(--border);
  }}
  table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
  }}
  th, td {{
    padding: 8px 6px;
    text-align: right;
    border-bottom: 1px solid var(--border);
    white-space: nowrap;
  }}
  th:first-child, td:first-child {{
    text-align: left;
  }}
  th {{
    color: var(--muted);
    font-weight: 500;
    font-size: 11px;
  }}
  .machine-no {{
    font-weight: 600;
  }}
  .val-plus {{ color: var(--plus); font-weight: 600; }}
  .val-minus {{ color: var(--minus); font-weight: 600; }}
  .val-zero {{ color: var(--zero); }}
  .card-wrap {{
    display: block;
  }}
  @media (max-width: 480px) {{
    table, thead, tbody, th, td, tr {{ display: block; }}
    thead {{ display: none; }}
    tr {{
      background: var(--card);
      border-radius: 10px;
      margin-bottom: 8px;
      padding: 10px 12px;
      border: 1px solid var(--border);
    }}
    td {{
      border: none;
      display: flex;
      justify-content: space-between;
      padding: 4px 0;
    }}
    td::before {{
      content: attr(data-label);
      color: var(--muted);
      font-size: 11px;
    }}
    td:first-child {{
      font-size: 15px;
      padding-bottom: 6px;
      border-bottom: 1px solid var(--border);
      margin-bottom: 4px;
    }}
    td:first-child::before {{ content: ""; }}
  }}
  footer {{
    color: var(--muted);
    font-size: 11px;
    text-align: center;
    margin-top: 24px;
    padding: 12px 0;
  }}
</style>
</head>
<body>
<header>
  <h1>パチスロ情報モニター</h1>
  <div class="updated">最終更新: {updated_at}</div>
</header>

{page_blocks}

<footer>自動スクレイピング &middot; データ提供元の内容と実際が異なる場合があります</footer>
</body>
</html>
"""

PAGE_BLOCK_TEMPLATE = """
<div class="page-block">
  <div class="page-title">{machine_type}</div>
  <table>
    <thead>
      <tr>
        <th>台番号</th>
        <th>差玉(最終)</th>
        <th>大当り回数</th>
        <th>確変突入</th>
        <th>大当り確率</th>
        <th>累計スタート</th>
        <th>最終スタート</th>
      </tr>
    </thead>
    <tbody>
      {rows}
    </tbody>
  </table>
</div>
"""


def value_class(v):
    try:
        n = int(v)
    except (TypeError, ValueError):
        return "val-zero"
    if n > 0:
        return "val-plus"
    if n < 0:
        return "val-minus"
    return "val-zero"


def fmt(v):
    if v is None or v == "":
        return "-"
    return str(v)


def build_rows(machines):
    # 差玉の大きい順に並び替え
    def sort_key(m):
        try:
            return int(m.get("graph_final_value") or 0)
        except (TypeError, ValueError):
            return 0

    sorted_machines = sorted(machines, key=sort_key, reverse=True)

    rows_html = []
    for m in sorted_machines:
        gval = m.get("graph_final_value")
        vclass = value_class(gval)
        gval_display = f"{gval:+d}" if isinstance(gval, int) else fmt(gval)

        rows_html.append(f"""      <tr>
        <td data-label="台番号" class="machine-no">{fmt(m.get('machine_no'))}</td>
        <td data-label="差玉(最終)" class="{vclass}">{gval_display}</td>
        <td data-label="大当り回数">{fmt(m.get('大当り回数'))}</td>
        <td data-label="確変突入">{fmt(m.get('確変突入回数'))}</td>
        <td data-label="大当り確率">{fmt(m.get('大当り確率'))}</td>
        <td data-label="累計スタート">{fmt(m.get('累計スタート'))}</td>
        <td data-label="最終スタート">{fmt(m.get('最終スタート'))}</td>
      </tr>""")
    return "\n".join(rows_html)


def generate_site():
    if not os.path.exists(LATEST_JSON):
        print(f"❌ データファイルが見つかりません: {LATEST_JSON}")
        print("  先に scraper.py を実行してください")
        return False

    with open(LATEST_JSON, "r", encoding="utf-8") as f:
        payload = json.load(f)

    page_blocks = []
    for page in payload.get("pages", []):
        rows = build_rows(page.get("machines", []))
        block = PAGE_BLOCK_TEMPLATE.format(
            machine_type=page.get("machine_type", "不明"),
            rows=rows,
        )
        page_blocks.append(block)

    html = HTML_TEMPLATE.format(
        updated_at=payload.get("updated_at", "-"),
        page_blocks="\n".join(page_blocks),
    )

    os.makedirs(SITE_DIR, exist_ok=True)
    with open(SITE_INDEX, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✓ サイト生成完了: {SITE_INDEX}")
    return True


if __name__ == "__main__":
    success = generate_site()
    sys.exit(0 if success else 1)
