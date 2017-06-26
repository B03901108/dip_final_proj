import sys
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
res = rs.get(domain + '/bbs/Gossiping/index.html', verify = False)

lenLwb = 8
numPush = 0
pushUpb = 5000
while True:
  soup = BeautifulSoup(res.text)

  for entry in soup.select('.r-ent'):
    if entry.find('a') is not None:
      titleIn = entry.find('div', attrs = {'class' : 'title'}).text
      if '母豬' not in titleIn:
        continue
      newUrl = entry.find('a')['href']
      res = rs.get(domain + newUrl, verify = False)
      subSoup = BeautifulSoup(res.text)
      whole = subSoup.find(id = 'main-content')

      if whole is None:
        continue
      for remark in whole.select('.push-content'):
        if remark is None:
          continue
        strOut = remark.text[2:]
        if len(re.sub(r'[\s+\.\!\?\[\]\\\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）：；《）《》“”()»ω～=:ヽ・∀・ノ○★「」<>′`〒∫＜＞【／】＄〔〕-]+', '', strOut)) >= lenLwb:
          numPush += 1
          print(re.sub(r'[\t]+', ' ', strOut))
          if numPush >= pushUpb:
            sys.exit(0)

  newUrl = soup.find(class_ = 'btn-group-paging').select('a')[1]['href']
  res = rs.get(domain + newUrl, verify = False)
