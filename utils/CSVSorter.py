import pandas as pd
from datetime import datetime

class CSVSorter:
    @staticmethod
    def sort_csv(input_file, output_file):
        """
        读取CSV文件，首先按日期降序排序，然后对于日期相同的行按基金名称升序排序，最后保存为新的CSV文件
        
        :param input_file: 输入CSV文件的路径
        :param output_file: 输出CSV文件的路径
        """
        try:
            # 读取CSV文件，将第一行作为列名
            df = pd.read_csv(input_file)
            
            # 将日期列转换为datetime类型，指定格式
            df['日期'] = pd.to_datetime(df['日期'], format='%Y-%m-%d')
            
            # 首先按日期降序排序，然后对于日期相同的行按基金名称升序排序
            df = df.sort_values(by=['日期', '基金名称'], ascending=[False, True])
            
            # 保存排序后的数据为新的CSV文件
            df.to_csv(output_file, index=False, date_format='%Y-%m-%d')
            
            print(f"排序后的CSV文件已保存至: {output_file}")
        except Exception as e:
            print(f"处理CSV文件时发生错误: {str(e)}")

    @staticmethod
    def print_sorted_data(input_file, num_rows=10):
        """
        读取CSV文件，首先按日期降序排序，然后对于日期相同的行按基金名称升序排序，最后打印前几行数据
        
        :param input_file: 输入CSV文件的路径
        :param num_rows: 要打印的行数，默认为10
        """
        try:
            # 读取CSV文件，将第一行作为列名
            df = pd.read_csv(input_file)
            
            # 将日期列转换为datetime类型，指定格式
            df['日期'] = pd.to_datetime(df['日期'], format='%Y-%m-%d')
            
            # 首先按日期降序排序，然后对于日期相同的行按基金名称升序排序
            df = df.sort_values(by=['日期', '基金名称'], ascending=[False, True])
            
            # 打印前几行数据
            print(df.head(num_rows).to_string(index=False))
        except Exception as e:
            print(f"处理CSV文件时发生错误: {str(e)}")
