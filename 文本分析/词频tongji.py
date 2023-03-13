# -*- coding:utf-8 -*-
import jieba
txt = open("D:\大学\毛泽东思想概论\\b站爬虫\第五次\领风者\第七集\去重后\弹幕文本清洗.txt", "r", encoding='utf-8').read()

stop_words = ['这是','孩子','儿子','一集','咕咕','一点','呜呜','啊啊啊','有点','哈哈','哈哈哈','哈哈哈哈','就是','不是','什么','这个','真的','可以','这么','一个','没有',' ','?','!',',']
file_stop = r'D:\\大学\\毛泽东思想概论\b站爬虫\\第五次\stopwords.txt'  # 停用词表
with open(file_stop,'r',encoding='utf-8-sig') as f :
    lines = f.readlines()  # lines是list类型
    for line in lines:
        lline  = line.strip()     # line 是str类型,strip 去掉\n换行符
        stop_words.append(lline)        # 将stop 是列表形式

file_name = 'dict.txt'  # 自定义的词典
jieba.load_userdict(file_name)
words  = jieba.lcut(txt)    #分词处理，形参列表
counts = {}     #构造字典

for word in words:
    if len(word) == 1:
        continue
    elif word in stop_words :
        continue
    else:
        counts[word] = counts.get(word,0) + 1

items = list(counts.items())    #转换为列表类型
with open('D:\大学\毛泽东思想概论\\b站爬虫\第五次\领风者\第七集\去重后\词频统计.txt', 'w+', encoding='utf-8') as f:
    items.sort(key=lambda x:x[1], reverse=True) 
    for i in range(100):
        word, count = items[i]
        f.write("{0:<10}{1:>5}".format(word, count))
        f.write('\n')
        print ("{0:<10}{1:>5}".format(word, count))