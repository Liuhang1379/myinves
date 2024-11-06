from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def fetch_fund_data():
    # 设置 Chrome 选项
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # 无头模式，不显示浏览器窗口

    # 初始化 WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # 打开网页
        url = 'https://fundf10.eastmoney.com/jjjz_017093.html'
        driver.get(url)

        # 等待表格加载
        wait = WebDriverWait(driver, 10)
        table = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'w782')))

        # 找到所有行
        rows = table.find_elements(By.TAG_NAME, 'tr')

        # 提取数据
        for row in rows[1:6]:  # 跳过表头，只处理前5行
            cols = row.find_elements(By.TAG_NAME, 'td')
            if len(cols) >= 4:
                date = cols[0].text
                net_value = cols[1].text
                growth_rate = cols[3].text
                print(f"日期: {date}, 净值: {net_value}, 日增长率: {growth_rate}")

    finally:
        driver.quit()

fetch_fund_data()
