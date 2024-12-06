from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

# 初始化 Selenium WebDriver
def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # 无头模式，不弹出浏览器
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)
    return driver

# 抓取单页数据
def scrape_page(driver):
    holders_data = []
    rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
    
    for row in rows:
        columns = row.find_elements(By.TAG_NAME, "td")
        if columns:
            address = columns[0].text
            balance = columns[1].text
            percentage = columns[2].text
            holders_data.append({
                "Address": address,
                "Balance": balance,
                "Percentage": percentage
            })
    return holders_data

# 保存数据到 Excel
def save_to_excel(data, filename="atom_holders.xlsx"):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False, engine='openpyxl')
    print(f"数据已保存到 {filename}")

def scrape_and_save_atom_holders(base_url):
    driver = setup_driver()
    all_holders_data = []  # 用于存储所有页面的数据
    page_num = 1  # 初始页数

    while True:
        url = f"{base_url}&holderpage={page_num}"
        driver.get(url)
        time.sleep(5)  # 等待页面加载

        page_data = scrape_page(driver)
        if not page_data:
            print("没有更多数据，停止抓取。")
            break  # 如果没有数据，说明已经抓取完所有页面

        all_holders_data.extend(page_data)  # 将当前页的数据合并到所有数据中

        # 每抓取完一页数据，立即保存到 Excel
        save_to_excel(all_holders_data, filename="atom_holders_combined.xlsx")

        page_num += 1  # 增加页面编号

    driver.quit()

# 主函数
if __name__ == "__main__":
    base_url = "https://atomscan.org/token/atom?table=holder&section=trend"
    scrape_and_save_atom_holders(base_url)

