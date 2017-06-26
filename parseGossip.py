import requests
from bs4 import BeautifulSoup
import re

domain = 'https://www.ptt.cc'
payload = {
  'from': '/bbs/Gossiping/index.html',
  'yes': 'yes',
}

rs = requests.session()
res = rs.post(domain + '/ask/over18', verify = False, data = payload)
res = rs.get(domain + '/bbs/Gossiping/index21444.html', verify = False)

for i in range(10):
  soup = BeautifulSoup(res.text)

  for entry in soup.select('.r-ent'):
    if entry.find('a') is not None:
      newUrl = entry.find('a')['href']
      res = rs.get(domain + newUrl, verify = False)
      subSoup = BeautifulSoup(res.text)
      whole = subSoup.find(id = 'main-content')

      if whole is None:
        continue
      strOut = whole.find(text=True, recursive=False)
      if strOut is not None:
        print(re.sub(r'[\s+\.\!\?\[\]\\\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）：；《）《》“”()»ω～=:ヽ・∀・ノ○★「」<>′`〒∫＜＞【／】＄〔〕-]+', ' ', strOut))
      for remark in whole.select('.push-content'):
        if remark is None:
          continue
        strOut = remark.text[1:]
        print(re.sub(r'[\s+\.\!\?\[\]\\\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）：；《）《》“”()»ω～=:ヽ・∀・ノ○★「」<>′`〒∫＜＞【／】＄〔〕-]+', ' ', strOut))

  newUrl = soup.find(class_ = 'btn-group-paging').select('a')[1]['href']
  res = rs.get(domain + newUrl, verify = False)
