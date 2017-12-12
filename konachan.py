import urllib.request
import re
import os
def obtsrc(year,month,day):
	dirs = []
	request = urllib.request.Request('http://konachan.net/post/popular_by_day?day=' + str(day) + '&month=' + str(month) + '&year=' + str(year))
	response = urllib.request.urlopen(request)
	content = response.read().decode('utf-8')
	pattern = re.compile('<a class="thumb" href=.*?>')
	srcs = re.findall(pattern,content)
	n = 1
	for src in srcs:
		src = "http://konachan.net"+src[23:-3]
		request = urllib.request.Request(src)
		response = urllib.request.urlopen(request)
		content2 = response.read().decode('utf-8')
		pattern2 = re.compile('<a class="original-file-[changed|unchanged].*?>')
		downurl = re.findall(pattern2,content2)
		for down in downurl:
			dirs.append(down)
	newdirs = []
	for dir in dirs:
		if(dir.find('highres-show') == -1):
			newdirs.append(dir)
	pngdirs = []
	jpgdirs = []
	dirs = []
	for dir in newdirs:
		if (dir.find('png') != -1):
			pngdirs.append(dir)
			for jpgsrc in jpgdirs:
				if (jpgsrc.find(dir[62:94]) != -1):
					jpgdirs.remove(jpgsrc)
		else:
			jpgdirs.append(dir)
	for dir in jpgdirs:
		if (dir.find('unchanged') != -1):
			dir = 'http:' + dir[41:-15] + '\n'
		else:
			dir = 'http:' + dir[39:-15] + '\n'
		dirs.append(dir)
	for dir in pngdirs:
		dir = 'http:' + dir[41:-11] + '\n'
		dirs.append(dir)
	return dirs

def obtday(year,month):
	if(month == 2):
		if((year%4 == 0) and (year%100 != 0)):
			return 29
		else:
			return 28
	elif(month in [1,3,5,7,8,10,12]):
		return 31
	else:
		return 30
def main():
	srcs = []
	year = 2009
	for month in range(1,13):
		maxday = obtday(year,month) + 1
		for day in range(1,maxday):
			dirs = obtsrc(year,month,day)
			srcs += dirs
		file = open("src.txt","w",encoding="utf-8")
		file.writelines(srcs)
		file.close()

main()