from PIL import Image
import jieba
import wordcloud
import numpy as np

if __name__ == "__main__":
    fname1 = 'D:\大学\毛泽东思想概论\\b站爬虫\第五次\领风者\第六集\去重后\去重后弹幕.csv'
    f = open(fname1 ,encoding='utf-8')
    txt = f.read()  #   读取
    file_name = 'dict.txt'  # 自定义的词典
    jieba.load_userdict(file_name)
    wordlist = jieba.lcut(txt)
    wordlist = [word for word in wordlist if len(word)>1]# 该条主要是为了排除一个字符以下的词，没有这条文本将会分出都是单字。
    string = ' '.join(wordlist)
    img = Image.open('3.1.png')
    img_array = np.array(img)

    stop_words = ['这是','孩子','儿子','一集','咕咕','一点','呜呜','啊啊啊','有点','哈哈','哈哈哈','哈哈哈哈','就是','不是','什么','这个','真的','可以','这么','一个','没有',' ','?','!',',']
    file_stop = r'D:\\大学\\毛泽东思想概论\b站爬虫\\第五次\stopwords.txt'  # 停用词表
    with open(file_stop,'r',encoding='utf-8-sig') as f :
      lines = f.readlines()  # lines是list类型
      for line in lines:
        lline  = line.strip()     # line 是str类型,strip 去掉\n换行符
        stop_words.append(lline)        # 将stop 是列表形式
    
    wc = wordcloud.WordCloud(
		  font_path='simhei.ttf',     #字体
		  colormap='Blues', #给每个词分颜色
		  collocations=False,
		  background_color='white',   #背景颜色
		  width=1000,
		  height=1000,
		  scale=1.5,
		  max_font_size=150,
		  min_font_size=5,
		  mask = img_array,  #背景图片
		  max_words=500,  #词的最大个数
		  stopwords=stop_words
	)
    wc.generate_from_text(string)
    fname2 = 'D:\大学\毛泽东思想概论\\b站爬虫\第五次\领风者\第六集\去重后\\result.png'
    wc.to_file(fname2)