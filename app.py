from src.fund_scraper import fetch_fund_data
from utils.CSVDeduplicator import CSVDeduplicator
from utils.CSVSorter import CSVSorter
from src.investment_analysis import fund_investment_analysis  # Import the missing function




if __name__ == "__main__":
  csv_path = "fund_data.csv"
  '''
  抓取数据并校准前一天的数据
  '''
  fetch_fund_data()



  '''
  清洗数据'''
  # 排序并保存CSV文件
  CSVSorter.sort_csv(csv_path, csv_path)



  '''
  清洗csv多于数据
  '''
  # 直接调用静态方法，无需实例化
  CSVDeduplicator.deduplicate_csv(csv_path, csv_path, columns=["日期", "基金名称"])



  '''
  计算是否补仓以及补仓数量,调试程序时请注释掉
  '''
  #fund_investment_analysis(csv_path)