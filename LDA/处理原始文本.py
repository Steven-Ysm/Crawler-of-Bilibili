# -*- coding:utf-8 -*-
import jieba
if __name__ == "__main__":
    stopwords = ['这是','孩子','儿子','一集','咕咕','一点','呜呜','啊啊啊','有点','哈哈','哈哈哈','哈哈哈哈','就是','不是','什么','这个','真的','可以','这么','一个','没有',' ','?','!',',']
    file_stop = r'D:\\大学\\毛泽东思想概论\b站爬虫\\第五次\stopwords.txt'  # 停用词表
    with open(file_stop,'r',encoding='utf-8-sig') as f :
      lines = f.readlines()  # lines是list类型
      for line in lines:
        lline  = line.strip()     # line 是str类型,strip 去掉\n换行符
        stopwords.append(lline)        # 将stop 是列表形式
        
    file_name = 'dict.txt'  # 自定义的词典
    jieba.load_userdict(file_name)
    fname1 = 'D:\大学\毛泽东思想概论\\b站爬虫\第五次\领风者\第七集\去重后\\去重后弹幕.csv'
    f = open(fname1 ,encoding='utf-8')
    txt = f.read()  #   读取
    wordlist = jieba.lcut(txt)
    wordfile = 'D:\大学\毛泽东思想概论\\b站爬虫\第五次\LDA\第七集弹幕文本清洗.txt'
    with open(wordfile, 'w+', encoding='utf-8') as f:
        for word in wordlist:
            if word not in stopwords and word.__len__()>1:
                f.write(word)
                f.write(' ')
                f.write('\n')