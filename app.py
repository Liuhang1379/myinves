from src.fund_scraper import fetch_fund_data
from utils.CSVDeduplicator import CSVDeduplicator
from utils.CSVSorter import CSVSorter
from src.investment_analysis import fund_investment_analysis  # Import the missing function




if __name__ == "__main__":

    '''
    抓取数据
    '''
    fetch_fund_data()

    '''
    清洗csv多于数据
    '''
    csv_path = r"investment\fund_data.csv"
    # 直接调用静态方法，无需实例化
    CSVDeduplicator.deduplicate_csv(csv_path, csv_path)

    '''
    计算是否补仓以及补仓数量
    '''
    #fund_investment_analysis(csv_path)


    # 排序并保存CSV文件
    CSVSorter.sort_csv(csv_path, csv_path)
