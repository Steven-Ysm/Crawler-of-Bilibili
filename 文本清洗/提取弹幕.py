import pandas as pd
path = 'D:\大学\毛泽东思想概论\\b站爬虫\第五次\领风者\第七集\去重后\\result去重.csv'
# 使用pandas读入
data = pd.read_csv(path) #读取文件中所有数据
# 按列分离数据
output_file='D:\大学\毛泽东思想概论\\b站爬虫\第五次\领风者\第七集\去重后\\去重后弹幕.csv'
data.to_csv(output_file,sep=',',columns=['弹幕'],header=None,index=False)
