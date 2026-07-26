"""
パチスロ/パチンコ情報スクレイピング メインモジュール

対象ページの各台について、以下を取得する:
- 台番号
- 大当り回数 / 確変突入回数 / 大当り確率 / 累計スタート / 最終スタート
- グラフの最終値（差玉）と、最終「out」値（総回転数相当）

グラフは amCharts (v3) で描画されており、JS実行で
window.AmCharts.charts[].dataProvider から最終値を直接取得する。
"""
import os
import sys
import json
import time
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException

from config import (
    TARGET_PAGES, CHROME_DRIVER_PATH, HEADLESS, CHROME_PROFILE_DIR,
    CHROME_DEBUG_PORT, TIMEOUT, DATA_DIR, LATEST_JSON, HISTORY_DIR
)

# ページ内で実行する抽出スクリプト
EXTRACT_JS = r"""
function extractField(text, label, nextLabels) {
  const idx = text.indexOf(label);
  if (idx === -1) return null;
  let rest = text.slice(idx + label.length).trim();
  for (const nl of nextLabels) {
    const i2 = rest.indexOf(nl);
    if (i2 !== -1) { rest = rest.slice(0, i2); }
  }
  return rest.trim();
}

const labels = ['大当り回数','確変突入回数','大当り確率','累計スタート','最終スタート'];
const chartDivs = document.querySelectorAll('[id^="ca-"]');

const chartsByDiv = {};
if (typeof AmCharts !== 'undefined') {
  AmCharts.charts.forEach(c => { if (c.div) chartsByDiv[c.div.id] = c; });
}

const results = [];
chartDivs.forEach(div => {
  const id = div.id;
  const machineNo = id.replace('ca-', '');
  const li = div.closest('li');
  const text = li ? li.innerText.replace(/\s+/g, ' ').trim() : '';

  const rec = { machine_no: machineNo };
  for (let i = 0; i < labels.length; i++) {
    const label = labels[i];
    const nextLabels = labels.slice(i + 1);
    rec[label] = extractField(text, label, nextLabels);
  }

  const c = chartsByDiv[id];
  if (c && c.dataProvider && c.dataProvider.length) {
    const last = c.dataProvider[c.dataProvider.length - 1];
    rec['graph_final_value'] = last.value;
    rec['graph_final_out'] = last.out;
    rec['graph_points'] = c.dataProvider.length;
  } else {
    rec['graph_final_value'] = null;
    rec['graph_final_out'] = null;
    rec['graph_points'] = 0;
  }
  results.push(rec);
});

return JSON.stringify(results);
"""


class PachiSlotScraper:
    def __init__(self, headless=None):
        self.driver = None
        self.headless = HEADLESS if headless is None else headless
        self.attached_to_existing = False

    def start_browser(self):
        """
        ブラウザ起動。優先順位:
        1. start_chrome_debug.bat で起動済みのChrome（毎日ログインする方式）に接続
        2. 見つからなければ、専用プロファイルで新規起動（前回のセッションを再利用）
        """
        # 1. 起動済みのデバッグChromeに接続を試みる
        debug_options = webdriver.ChromeOptions()
        debug_options.debugger_address = f"127.0.0.1:{CHROME_DEBUG_PORT}"

        try:
            service = Service(executable_path=CHROME_DRIVER_PATH)
            self.driver = webdriver.Chrome(service=service, options=debug_options)
            self.attached_to_existing = True
            print(f"✓ 起動中のChrome（デバッグポート {CHROME_DEBUG_PORT}）に接続しました")
            return
        except WebDriverException:
            print(f"[情報] デバッグChromeが見つかりません（ポート{CHROME_DEBUG_PORT}）")
            print("  → start_chrome_debug.bat を起動してログインしておくと、")
            print("    そのセッションをそのまま使えます")
            print("  → 見つからないため、専用プロファイルで新規起動します")

        # 2. 専用プロファイルで新規起動（フォールバック）
        options = webdriver.ChromeOptions()

        if self.headless:
            options.add_argument("--headless=new")

        profile_dir = os.path.abspath(CHROME_PROFILE_DIR)
        os.makedirs(profile_dir, exist_ok=True)
        options.add_argument(f"--user-data-dir={profile_dir}")

        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")

        service = Service(executable_path=CHROME_DRIVER_PATH)
        self.driver = webdriver.Chrome(service=service, options=options)

    def scrape_page(self, page_config):
        """1ページ分をスクレイピング"""
        name = page_config["name"]
        url = page_config["url"]

        print(f"[アクセス] {name}: {url[:60]}...")
        self.driver.get(url)

        # ページロード待機（機種一覧の要素が出るまで）
        try:
            WebDriverWait(self.driver, TIMEOUT).until(
                lambda d: d.execute_script(
                    "return document.querySelectorAll('[id^=\"ca-\"]').length > 0"
                )
            )
        except Exception:
            print(f"  ⚠ タイムアウト: グラフ要素が見つかりませんでした")
            print(f"  → ログインが必要な可能性があります。HEADLESS=False で再実行してください")
            return None

        # amChartsの描画完了を少し待つ
        time.sleep(2)

        raw = self.driver.execute_script(EXTRACT_JS)
        machines = json.loads(raw)

        print(f"  ✓ {len(machines)} 台のデータを取得")

        return {
            "machine_type": name,
            "url": url,
            "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "machines": machines,
        }

    def scrape_all(self):
        """設定された全ページをスクレイピング"""
        results = []
        try:
            self.start_browser()
            for page_config in TARGET_PAGES:
                result = self.scrape_page(page_config)
                if result:
                    results.append(result)
        finally:
            self.close_browser()
        return results

    def close_browser(self):
        if not self.driver:
            return
        if self.attached_to_existing:
            # 既存のChrome（ユーザーが使うブラウザ）には手を付けない
            print("[情報] 既存Chromeへの接続を切断（ブラウザ自体は閉じません）")
            return
        self.driver.quit()


def save_data(results):
    """データをJSONで保存（最新版 + 履歴）"""
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(HISTORY_DIR, exist_ok=True)

    payload = {
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "pages": results,
    }

    with open(LATEST_JSON, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(f"✓ 最新データ保存: {LATEST_JSON}")

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    history_file = os.path.join(HISTORY_DIR, f"{ts}.json")
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(f"✓ 履歴保存: {history_file}")


def main():
    print("=" * 60)
    print("パチスロ情報スクレイピング開始")
    print("=" * 60)

    scraper = PachiSlotScraper()
    results = scraper.scrape_all()

    if not results:
        print("\n❌ データ取得に失敗しました")
        return False

    save_data(results)

    print("\n" + "=" * 60)
    print("✓ スクレイピング完了")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
