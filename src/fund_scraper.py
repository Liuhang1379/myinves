import requests
from lxml import html
import re
from datetime import datetime
import csv

def fetch_fund_data():
    # 定义需要遍历的网址及其对应的基金名称和代号
    funds = {
        'https://fundf10.eastmoney.com/jjjz_017093.html': ("景顺长城纳斯达克科技", "017093"),
        'https://fundf10.eastmoney.com/jjjz_270042.html': ("广发纳斯达克100", "270042"),
        'https://fundf10.eastmoney.com/jjjz_017641.html': ("摩根标普500", "017641")
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # 获取今天的日期
    today_date = datetime.now().strftime("%Y-%m-%d")

    # 准备 CSV 文件
    csv_file = 'investment\\fund_data.csv'
    with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # 写入 CSV 文件的标题行
        # writer.writerow(['日期', '基金名称', '基金代码', '净值', '日增长率'])

        # 遍历每个网址
        for url, (fund_name, fund_code) in funds.items():
            response = requests.get(url, headers=headers)
            
            # 检查请求是否成功
            if response.status_code != 200:
                print(f"请求失败，状态码: {response.status_code}")
                continue  # 如果请求失败，跳过当前网址

            tree = html.fromstring(response.content)

            # 使用XPath提取数据
            xpath = '//label[contains(text(), "单位净值")]'
            elements = tree.xpath(xpath)

            if elements:
                for element in elements:
                    # 将 LabelElement 转换为字符串
                    label_string = html.tostring(element, encoding='UTF-8').decode('utf-8')
                    
                    # 提取 <b> 标签中的内容
                    b_element = element.xpath('./b/text()')
                    if b_element:
                        b_text = b_element[0].strip()  # 获取 <b> 标签内的文本并去除空白

                        # 使用正则表达式从 <b> 文本中提取单位净值和增长率
                        net_value_match = re.search(r'([\d.]+)', b_text)  # 提取单位净值
                        growth_rate_match = re.search(r'\(\s*([-]?\d+\.?\d*)%\s*\)', b_text)  # 提取日增长率

                        # 提取单位净值
                        net_value = float(net_value_match.group(1)) if net_value_match else None
                        # 提取增长率
                        growth_rate = growth_rate_match.group(1) + '%' if growth_rate_match else None
                        
                        # 写入 CSV 文件
                        writer.writerow([today_date, fund_name, fund_code, net_value, growth_rate])
                        print(f"{today_date} {fund_name} {fund_code} 净值: {net_value}, 日增长率: {growth_rate}")
            else:
                print("未找到匹配的元素")
