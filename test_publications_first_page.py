import time
import csv
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


TEACHER_CSV = "teacher_links.csv"


def build_driver():
    options = Options()
    options.debugger_address = "127.0.0.1:9222"
    return webdriver.Chrome(options=options)


def load_teacher_links(csv_path):
    teachers = []
    with open(csv_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = (row.get("teacher_name") or "").strip()
            profile_url = (row.get("teacher_profile_url") or "").strip()
            if name and profile_url:
                teachers.append({
                    "teacher_name": name,
                    "teacher_profile_url": profile_url,
                })
    return teachers


def get_publications_first_page(driver, teacher_name, profile_url):
    pub_url = profile_url.rstrip("/") + "/publications/"
    driver.get(pub_url)
    time.sleep(4)

    print(f"\n老师 / Teacher: {teacher_name}")
    print(f"页面 / Page: {pub_url}")
    print(f"标题 / Title: {driver.title}")

    elems = driver.find_elements(By.CSS_SELECTOR, "h3.title a.link")

    rows = []
    seen = set()

    for e in elems:
        title = e.text.strip()
        href = (e.get_attribute("href") or "").strip()

        if not title or not href:
            continue

        # 只保留文章详情页 / Keep only publication detail pages
        if "/en/publications/" not in href:
            continue

        key = (teacher_name, title, href)
        if key in seen:
            continue
        seen.add(key)

        rows.append({
            "teacher_name": teacher_name,
            "teacher_profile_url": profile_url,
            "publication_title": title,
            "publication_url": href,
        })

    print(f"本页抓到文章数 / Publications found on this page: {len(rows)}")
    for i, row in enumerate(rows[:5], 1):
        print(f"  {i}. {row['publication_title']}")

    return rows


def main():
    teachers = load_teacher_links(TEACHER_CSV)
    print(f"读取到老师数量 / Number of teachers loaded: {len(teachers)}")

    driver = build_driver()
    try:
        Path("debug").mkdir(exist_ok=True)

        all_rows = []

        for i, teacher in enumerate(teachers, 1):
            print(f"\n[{i}/{len(teachers)}] 正在处理 / Processing: {teacher['teacher_name']}")
            try:
                rows = get_publications_first_page(
                    driver,
                    teacher["teacher_name"],
                    teacher["teacher_profile_url"]
                )
                all_rows.extend(rows)

                # 可选：保存当前页源码，调试用 / Optional: save current page HTML for debugging
                # with open(f"debug/{teacher['teacher_name']}_publications.html", "w", encoding="utf-8") as f:
                #     f.write(driver.page_source)

            except Exception as e:
                print(f"处理失败 / Failed: {teacher['teacher_name']} -> {e}")

        out_csv = "teacher_publications_first_page.csv"
        with open(out_csv, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "teacher_name",
                    "teacher_profile_url",
                    "publication_title",
                    "publication_url",
                ]
            )
            writer.writeheader()
            writer.writerows(all_rows)

        print(f"\n已保存 / Saved: {out_csv}")
        print(f"总共抓到记录数 / Total records collected: {len(all_rows)}")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()