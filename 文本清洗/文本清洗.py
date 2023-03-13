# -*- coding:utf-8 -*-
import jieba
if __name__ == "__main__":
    file_name = 'dict.txt'  # 自定义的词典
    jieba.load_userdict(file_name)
    fname1 = 'D:\大学\毛泽东思想概论\\b站爬虫\第五次\领风者\第七集\去重后\去重后弹幕.csv'
    f = open(fname1 ,encoding='utf-8')
    txt = f.read()  #   读取
    wordlist = jieba.lcut(txt)
    wordfile = 'D:\大学\毛泽东思想概论\\b站爬虫\第五次\领风者\第七集\去重后\弹幕文本清洗.txt'
    with open(wordfile, 'w+', encoding='utf-8') as f:
        for word in wordlist:
            f.write(word)
            if word != '\n':
                f.write(' ')