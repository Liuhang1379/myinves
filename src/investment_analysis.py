import pandas as pd
from datetime import datetime, timedelta

def fund_investment_analysis(file_path):
    def calculate_investment(today_price, high_price):
        drop_percentage = (high_price - today_price) / high_price * 100
        if drop_percentage <= 0:
            return 0
        investment_ratio = 8 * drop_percentage
        return investment_ratio

    data = pd.read_csv(file_path)
    data['基金名称'] = data['基金名称'].str.strip()

    today = datetime.now()
    day_before_yesterday = today - timedelta(days=2)
    day_before_yesterday_str = day_before_yesterday.strftime('%Y-%m-%d')

    funds = data['基金名称'].unique()
    print("可选择的基金有：")
    for idx, fund in enumerate(funds):
        print(f"{idx + 1}. {fund}")

    fund_choice = int(input("请选择您关注的基金（输入编号）：")) - 1
    selected_fund = funds[fund_choice]

    yesterday_data = data[(data['日期'] == day_before_yesterday_str) & (data['基金名称'] == selected_fund)]
    if yesterday_data.empty:
        recent_data = data[(data['基金名称'] == selected_fund) & (data['日期'] < day_before_yesterday_str)]
        if not recent_data.empty:
            last_friday_price = float(recent_data['净值'].values[0])
            last_friday_date = recent_data['日期'].values[0]
            print(f"前天没有数据，使用最近的可用净值: {last_friday_price} (日期: {last_friday_date})")
        else:
            print(f"前天({day_before_yesterday_str})没有基金数据，请检查数据文件。")
            return
    else:
        last_friday_price = float(yesterday_data['净值'].values[0])
        print(f"前天的基金净值为: {last_friday_price} (日期: {day_before_yesterday_str})")

    data['日期'] = pd.to_datetime(data['日期'])
    data = data.sort_values(by='日期', ascending=False)

    recent_20_days = data[(data['基金名称'] == selected_fund) & (data['日期'] <= today)].head(20)
    if recent_20_days.empty:
        print("没有找到最近20个交易日的数据，请检查数据文件。")
        return
    else:
        high_price = recent_20_days['净值'].max()
        high_price_date = recent_20_days[recent_20_days['净值'] == high_price]['日期'].values[0]
        high_price_date = pd.to_datetime(high_price_date)
        high_price_date_str = high_price_date.strftime('%Y-%m-%d')
        print(f"近20个交易日的最高净值为: {high_price} (日期: {high_price_date_str})")

    investment_ratio = calculate_investment(last_friday_price, high_price)

    if investment_ratio > 0:
        print(f"当前跌幅为 {(high_price - last_friday_price) / high_price * 100:.2f}%")
        print(f"建议补仓比例为 {investment_ratio:.2f}%")
        
        regular_investment = float(input("请输入您的单次定投数额: "))
        
        additional_investment = regular_investment * (investment_ratio / 100)
        
        print(f"建议补仓 {investment_ratio:.2f}%，即 {additional_investment:.2f} 元")
        print(f"总投资额为: {regular_investment + additional_investment:.2f} 元")
    else:
        print("当前无需补仓")

# 使用示例
# file_path = r'D:\_Develop\programmierung\python\fund_data.csv'
# fund_investment_analysis(file_path)
