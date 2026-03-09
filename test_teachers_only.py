import time
import csv
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

PERSONS_URL = "https://research.ucc.ie/en/organisations/school-of-mathematical-sciences-8/persons/"


def build_driver():
    options = Options()
    options.debugger_address = "127.0.0.1:9222"
    return webdriver.Chrome(options=options)


def main():
    # 先手动启动带远程调试端口的 Chrome，再让 Selenium 连接进去
    # (First manually start Chrome with the remote debugging port, then let Selenium connect.)
    # Mac 命令示例： (Mac command example:)
    # /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
    #   --remote-debugging-port=9222 \
    #   --user-data-dir=/tmp/chrome-selenium-profile
    #
    # 然后在那个新开的 Chrome 里手动访问 PERSONS_URL，等 Cloudflare 验证通过，
    # (Then in that newly opened Chrome, manually visit PERSONS_URL and wait for Cloudflare verification.)
    # 确认老师列表页已经正常显示后，再运行这个脚本。
    # (Ensure the teacher list page is displayed normally before running this script.)
    driver = build_driver()
    try:
        driver.get(PERSONS_URL)
        time.sleep(3)

        print("当前 URL (Current URL):", driver.current_url)
        print("页面标题 (Page Title):", driver.title)
        print("提示：如果这里的标题还是“请稍候…”或验证页标题，说明你还没有在手动打开的 Chrome 里完成验证。"
              " (Tip: If the title here is still “Please wait…” or the verification page title, "
              "it means you haven't completed the verification in the manually opened Chrome.)")

        # 保存截图和源码，别猜 (Save screenshot and HTML source; don't guess)
        Path("debug").mkdir(exist_ok=True)
        driver.save_screenshot("debug/persons_page.png")
        with open("debug/persons_page.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)

        print("已保存截图 (Screenshot saved): debug/persons_page.png")
        print("已保存源码 (HTML source saved): debug/persons_page.html")

        # 先确认三个选择器的命中情况
        elems1 = driver.find_elements(By.CSS_SELECTOR, "h3.title a.link.person")
        print("选择器1 命中数量 (Selector 1 match count):", len(elems1))

        elems2 = driver.find_elements(By.CSS_SELECTOR, "a[rel='Person']")
        print("选择器2 命中数量 (Selector 2 match count):", len(elems2))

        elems3 = driver.find_elements(By.CSS_SELECTOR, "a[href*='/en/persons/']")
        print("选择器3 命中数量 (Selector 3 match count):", len(elems3))

        # 用最准确的选择器提取老师主页链接，避免把 /en/persons/ 这个总入口混进去
        teacher_elems = driver.find_elements(By.CSS_SELECTOR, "h3.title a.link.person")
        teacher_rows = []
        seen = set()

        for e in teacher_elems:
            name = e.text.strip()
            href = (e.get_attribute("href") or "").strip()

            if not name or not href:
                continue
            if not href.startswith("https://research.ucc.ie/en/persons/"):
                continue

            key = (name, href)
            if key in seen:
                continue
            seen.add(key)

            teacher_rows.append({
                "teacher_name": name,
                "teacher_profile_url": href,
            })

        print("提取到老师数量 (Number of teachers extracted):", len(teacher_rows))
        for i, row in enumerate(teacher_rows[:10], 1):
            print(i, row["teacher_name"], "->", row["teacher_profile_url"])

        # 保存老师列表，便于下一步抓每位老师的 publications 页面
        csv_path = "teacher_links.csv"
        with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=["teacher_name", "teacher_profile_url"])
            writer.writeheader()
            writer.writerows(teacher_rows)

        print(f"已保存老师链接 (Teacher links saved): {csv_path}")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()