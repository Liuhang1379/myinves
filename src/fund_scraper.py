import csv
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def fetch_fund_data():
    funds = {
        'https://fundf10.eastmoney.com/jjjz_017093.html': ("景顺长城纳斯达克科技", "017093"),
        'https://fundf10.eastmoney.com/jjjz_270042.html': ("广发纳斯达克100", "270042"),
        'https://fundf10.eastmoney.com/jjjz_017641.html': ("摩根标普500", "017641")
    }

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    csv_file = 'fund_data.csv'
    
    try:
        try:
            existing_data = pd.read_csv(csv_file, dtype={'基金代码': str})
            existing_data['日期'] = pd.to_datetime(existing_data['日期']).dt.strftime('%Y-%m-%d')
        except FileNotFoundError:
            existing_data = pd.DataFrame(columns=['日期', '基金名称', '基金代码', '净值', '日增长率'])
            print("未找到现有CSV文件，创建新的DataFrame")

        new_data = []

        for url, (fund_name, fund_code) in funds.items():
            driver.get(url)
            wait = WebDriverWait(driver, 10)
            table = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'w782')))
            rows = table.find_elements(By.TAG_NAME, 'tr')

            for row in rows[1:]:
                cols = row.find_elements(By.TAG_NAME, 'td')
                if len(cols) >= 4:
                    date = pd.to_datetime(cols[0].text).strftime('%Y-%m-%d')
                    net_value = cols[1].text
                    growth_rate = cols[3].text.rstrip('%')

                    is_existing = ((existing_data['日期'] == date) & 
                                   (existing_data['基金代码'] == fund_code)).any()

                    if not is_existing:
                        new_data.append([date, fund_name, fund_code, net_value, growth_rate])

        if new_data:
            new_df = pd.DataFrame(new_data, columns=['日期', '基金名称', '基金代码', '净值', '日增长率'])
            combined_df = pd.concat([existing_data, new_df], ignore_index=True)
            combined_df.drop_duplicates(subset=['日期', '基金代码'], keep='first', inplace=True)
            combined_df.to_csv(csv_file, index=False, encoding='utf-8')
            print(f"已添加 {len(new_data)} 条新数据到 {csv_file}")
        else:
            print("没有新数据需要添加")

    finally:
        driver.quit()

    df = pd.read_csv(csv_file, dtype={'基金代码': str})
    df['日期'] = pd.to_datetime(df['日期'])
    df_sorted = df.sort_values(by=['基金代码', '日期'], ascending=[True, False])
    df_sorted.to_csv(csv_file, index=False)
    print(f"排序后的CSV文件已保存至: {csv_file}")

    CSVDeduplicator.deduplicate_csv(csv_file, csv_file, ['日期', '基金代码'])

class CSVDeduplicator:
    @staticmethod
    def deduplicate_csv(input_file: str, output_file: str, columns: list[str] = None) -> None:
        try:
            df = pd.read_csv(input_file, dtype={'基金代码': str})
            original_rows = len(df)
            if columns:
                df.drop_duplicates(subset=columns, keep='first', inplace=True)
            else:
                df.drop_duplicates(keep='first', inplace=True)
            deduplicated_rows = len(df)
            df.to_csv(output_file, index=False, header=True)
            print(f"去重完成。原始行数: {original_rows}, 去重后行数: {deduplicated_rows}")
            print(f"删除的重复行数: {original_rows - deduplicated_rows}")
        except Exception as e:
            print(f"处理CSV文件时发生错误: {str(e)}")
