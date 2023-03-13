import pandas as pd
import csv
fname1 = 'D:\大学\毛泽东思想概论\\b站爬虫\第五次\\file\第七集\第7集data.csv'
fname2 = 'D:\大学\毛泽东思想概论\\b站爬虫\第五次\\file\第七集\第7集评论字数排序.csv'
with open(fname1,'r',encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    column = [row[5] for row in reader]
wordlength = []
for c in column:
    wordlength.append(len(c))

with open(fname1,'r',encoding='utf-8') as csvFile:  #此处的csv是源表，即想要写入的表
    rows = csv.reader(csvFile)
    with open(fname2,'w',newline='',encoding='utf-8') as f: #这里的csv则是最后输出得到的新表
        writer = csv.writer(f)
        i = 0
        for row in rows:
            row.append(wordlength[i])
            i = i + 1
            writer.writerow(row)
df_loc = pd.read_csv(fname2,encoding='utf-8')
df_loc = df_loc.sort_values(axis=0, by=str(wordlength[0]), ascending=False)
df_loc.to_csv(fname2,header=True,index=False)