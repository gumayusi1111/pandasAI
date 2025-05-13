import pandas as pd
   
   # 方法1: 读取已有数据文件
df = pd.read_csv('/Users/wenbai/Desktop/pandasAi_to_pandas/sample_data.csv')  # 替换为你的文件路径
   
   # 方法2: 创建测试数据
   # df = pd.DataFrame({
   #     '单价': [10, 20, 30, 40, 50]
   # })
   
   # 计算平均值
average_price = df['单价'].mean()
   
   # 打印结果
print(average_price)