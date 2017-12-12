import urllib.request
import re
import os
#20080501 op

def obtsrc(year,month):
	dirs = []
	if (month < 10):
		strmonth = '0' + str(month)
	else:
		strmonth = str(month)
	request = urllib.request.Request('https://www.pixiv.net/ranking.php?mode=monthly&date=' + str(year) + strmonth +'01')
	response = urllib.request.urlopen(request)
	content = response.read().decode('utf-8')
	pattern = re.compile('<div class="ranking-image-item">.*?target="_blank">')
	srcs = re.findall(pattern,content)
	n = 1
	for src in srcs:
		src = 'https://www.pixiv.net' + src[41:72] + src[76:-38]
		request = urllib.request.Request(src)
		response = urllib.request.urlopen(request)
		content2 = response.read().decode('utf-8')
		pattern2 = re.compile('<div class="img-container">.*?alt')
		downurl = re.findall(pattern2,content2)
		dirs = dirs + downurl
	newdirs = []
	for dir in dirs:
		dir = dir[209:-5]
		dir = 'https://i.pximg.net/img-original/img/' + dir[45:-15] + '.jpg'
		newdirs.append(dir)
	return newdirs

def main():
	year = 2008
	srcs = []
	for month in range(5,13):
		srcs = srcs + obtsrc(year,month)
	file = open(str(year) + '.txt',"w",encoding="utf-8")
	file.writelines(srcs)
	file.close()

main()
