import jieba
jieba.set_dictionary('dict.txt.big')

testIn = open('testOut', 'rb').read()
words = jieba.cut(testIn, cut_all=False)
for word in words:
  print(word, end = ' ')