from snownlp import SnowNLP
import jieba

txt = open("D:\大学\毛泽东思想概论\\b站爬虫\第五次\领风者\七集弹幕文本清洗.txt", "r", encoding='utf-8').read()

stop_words = ['这是','孩子','儿子','一集','咕咕','一点','呜呜','啊啊啊','有点','哈哈','哈哈哈','哈哈哈哈','就是','不是','什么','这个','真的','可以','这么','一个','没有',' ','?','!',',']
file_stop = r'D:\\大学\\毛泽东思想概论\\从领风者的弹幕和评论看二次元文化对马克思主义意识形态大众化的效果及观看群体话语表征分析\\文本分析\stopwords.txt'  # 停用词表
with open(file_stop,'r',encoding='utf-8-sig') as f :
    lines = f.readlines()  # lines是list类型
    for line in lines:
        lline  = line.strip()     # line 是str类型,strip 去掉\n换行符
        stop_words.append(lline)        # 将stop 是列表形式

file_name = '文本分析\dict.txt'  # 自定义的词典
jieba.load_userdict(file_name)
words  = jieba.lcut(txt)    #分词处理，形参列表

positive = negative = middle = 0

for i in words:
   pingfen = SnowNLP(i)
   if pingfen.sentiments>0.7:
       positive+=1
   elif pingfen.sentiments<0.3:
       negative+=1
   else:
       middle+=1

sum=positive+middle+negative
print("总数",sum)
print("积极",positive)
print("中性",middle)
print("消极",negative)

import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 正常显示中文
plt.rcParams['axes.unicode_minus']=False      # 用来正常显示负号

labels ='积极','中性','消极'   #定义饼的标签名称
a = positive/sum
b = middle/sum
c = negative/sum
data = [a,b,c]              #每个标签所占的比例数据
plt.pie(data, labels= labels, autopct='%0.2f%%')     #绘制饼状图

plt.savefig('情感分析.jpg') # 保存到本地文件夹，当前路径下
plt.show()                 # 显示饼状图
