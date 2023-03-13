#点赞数排序
import pandas as pd
fname1 = 'D:\大学\毛泽东思想概论\\b站爬虫\第五次\\file\第七集\第7集data.csv'
df_loc = pd.read_csv(fname1)
df_loc = df_loc.sort_values(axis=0, by='评论点赞数', ascending=False)
df_loc.to_csv('D:\大学\毛泽东思想概论\\b站爬虫\第五次\\file\第七集\第7集点赞数排序.csv',header=True,index=False)
