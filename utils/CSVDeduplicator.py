import csv
import pandas as pd
from typing import List, Optional

class CSVDeduplicator:
    @staticmethod
    def deduplicate_csv(input_file: str, output_file: str, columns: Optional[List[str]] = None) -> None:
        """
        静态方法：读取CSV文件，去除重复行，并将结果保存到新的CSV文件。

        参数:
        input_file (str): 输入CSV文件的路径
        output_file (str): 输出CSV文件的路径
        columns (List[str], 可选): 用于判断重复的列名列表。如果为None，则使用所有列

        返回:
        None
        """
        try:
            # 读取CSV文件
            df = pd.read_csv(input_file)
            
            # 记录原始行数
            original_rows = len(df)

            # 去除重复行
            if columns:
                df.drop_duplicates(subset=columns, keep='first', inplace=True)
            else:
                df.drop_duplicates(keep='first', inplace=True)

            # 记录去重后的行数
            deduplicated_rows = len(df)

            # 保存结果到新的CSV文件，确保只写入一次表头
            df.to_csv(output_file, index=False, header=True)

            print(f"去重完成。原始行数: {original_rows}, 去重后行数: {deduplicated_rows}")
            print(f"删除的重复行数: {original_rows - deduplicated_rows}")
            print(f"结果已保存到: {output_file}")

        except Exception as e:
            print(f"处理CSV文件时发生错误: {str(e)}")

