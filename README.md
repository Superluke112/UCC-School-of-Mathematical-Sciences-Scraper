# UCC 数学学院信息爬取 / UCC School of Mathematical Sciences Scraper

## 简介 / Introduction
此项目包含两个 Python 脚本，用于从爱尔兰科克大学（UCC）数学学院网站抓取教师主页和其发表文章信息。脚本采用 Selenium 驱动浏览器，通过人工绕过 Cloudflare 验证后，自动提取信息。  
This project contains two Python scripts to scrape teacher profiles and their publication information from the University College Cork (UCC) School of Mathematical Sciences website. The scripts use Selenium to control Chrome; after manually bypassing Cloudflare verification, the code automatically extracts the data.

## 环境准备 / Prerequisites
在开始之前，请确保安装了以下软件和库：  
Before you start, ensure the following are installed:

- Python 3.9 或更高版本 / Python 3.9 or higher  
- Google Chrome 浏览器 / Google Chrome browser  
- pip 工具 / pip package manager  
- Selenium、webdriver-manager 和 Pandas 库 / Python packages: Selenium, webdriver-manager, and Pandas

在终端中安装依赖：/ Install dependencies via pip:

```bash
pip install selenium webdriver-manager pandas
```
## 使用步骤 / Usage

## 步骤一：启动远程调试 Chrome / Step 1: Start Chrome with remote debugging

由于目标网站采用 Cloudflare 保护，必须通过人工验证。首先，以远程调试模式启动 Chrome，例如在 macOS 上执行：
Because the target site is protected by Cloudflare, you must manually complete a verification step. First, start Chrome with remote debugging enabled, for example on macOS:
```
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir=/tmp/chrome-selenium-profile
```

## 在 Windows 或 Linux 上，请根据系统调整 Chrome 路径。
Adjust the Chrome path accordingly on Windows or Linux.

在这个新开的 Chrome 窗口中，访问教师列表页面：
https://research.ucc.ie/en/organisations/school-of-mathematical-sciences-8/persons/

完成 Cloudflare 验证并确保页面上出现教师列表。
In this new Chrome window, navigate to the persons page at the URL above. Complete the Cloudflare verification and ensure the list of teachers is visible.

## 步骤二：抓取教师链接 / Step 2: Extract teacher profiles

在同一个虚拟环境中运行脚本 test_teachers_only.py：
In the same environment, run the script test_teachers_only.py:

```
python test_teachers_only.py
```

## 脚本将连接到已经启动的 Chrome（通过远程调试端口），读取教师列表，并将姓名及个人主页链接保存到 teacher_links.csv 文件中，同时在终端输出进度信息（中英双语）。
The script attaches to the running Chrome via the remote debugging port, reads the list of teachers, and saves their names and profile URLs to a file named teacher_links.csv. It prints progress information in both Chinese and English.

## 步骤三：抓取发表文章信息 / Step 3: Scrape publications

第二个脚本 test_publications_first_page.py 会读取 teacher_links.csv，访问每位教师的 research output 页面，并抓取第一页的论文标题及链接。
The second script, test_publications_first_page.py, reads teacher_links.csv, visits each teacher’s research output page, and captures the titles and links from the first page of results.

运行脚本：/ Run the script:
```
python test_publications_first_page.py

```
## 该脚本同样依赖于已经打开的 Chrome 窗口，且默认只抓取第一页数据。输出将保存为 teacher_publications_first_page.csv，并在终端中以中英双语汇报抓取情况。
This script also attaches to the open Chrome instance and captures only the first page by default. The output is saved to teacher_publications_first_page.csv, and progress is printed in bilingual messages.

结果说明 / Output Explanation

生成的 CSV 文件包含以下字段：
The generated CSV files contain the following columns:
	•	teacher_name – 教师姓名 / Teacher name
	•	teacher_profile_url – 教师个人主页链接 / Teacher profile URL
	•	publication_title – 文章标题（仅在第二个 CSV 中）/ Publication title (in the second CSV)
	•	publication_url – 文章详情链接（仅在第二个 CSV 中）/ Link to publication details (in the second CSV)

注意：第二个脚本仅抓取每位老师的第一个分页页码中的论文。如果需要抓取所有分页，请根据页面的分页参数扩展脚本逻辑。     
Note: The second script captures only the first page of publications for each teacher. If you need to collect all pages, extend the script to loop through pagination.

## 版权和许可证 / License

此项目使用 MIT License，可自由修改和分发。    
This project is licensed under the MIT License. You are free to modify and distribute it.
