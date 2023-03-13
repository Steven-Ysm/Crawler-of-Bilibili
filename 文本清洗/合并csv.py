import os
import pandas as pd
import glob

bvid = 'ep262057'
csv_list = glob.glob('领风者\第七集\去重后\*.csv') #查看同文件夹下的csv文件数

print(u'共发现%s个CSV文件'% len(csv_list))
print(u'正在处理............')

for i in csv_list: #循环读取同文件夹下的csv文件
    fr = open(i,'rb').read()
    with open(bvid + 'result.csv','ab') as f: #将结果保存为result.csv
        f.write(fr)

print(u'合并完毕！')

fname= bvid +'result.csv'
data = pd.read_csv(fname)

total1 = len(open(fname,"r",encoding='utf-8').readlines())
print("去重前数据：",total1)

datalist =data.drop_duplicates(subset = None, keep = 'first',inplace=False)

fname1 = bvid+'result去重.csv'
datalist.to_csv(fname1,index=False,encoding='utf_8_sig')

total2 = len(open(fname1,"r",encoding='utf-8').readlines())
print("去重后数量：",total2)

