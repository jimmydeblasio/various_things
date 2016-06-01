import urllib2
import xml.etree.ElementTree as ElementTree
import sys
import dropbox


#removed credentials

def cleanse(x):
	return x.replace("/","-")

def download_file(download_url,sch,day,loc,wat):
	rr = urllib2.urlopen(download_url)
	client.put_file('/canvas_submissions/%s -- %s -- %s -- %s.pdf' % (sch,cleanse(loc),cleanse(day), wat),rr.read(),True)

begin_date = raw_input('start date?')
end_date = raw_input('end date?')

master =  urllib2.urlopen('#removed link' % (begin_date,end_date))
tree1 = ElementTree.parse(master)
root1 = tree1.getroot()
total_pages = int(root1[0].text)

urls = [urllib2.urlopen('removed link' % (begin_date, end_date,i)) for i in range(1,total_pages+1)]

for u in urls:
	print u.geturl()

for url in urls:
	print url.geturl()
	tree2 = ElementTree.parse(url)
	root2 = tree2.getroot()
	submissions = root2[2]
	for val in submissions:
		for val2 in val:
			if val2.tag == 'WebAccessToken':
					WebAccessToken = val2.text
			for val3 in val2.iter('Response'):
				if val3.find('Label').text == 'Location':
					Location = val3.find('Value').text
				if val3.find('Label').text == 'School':
					School = val3.find('Value').text
				if val3.find('Label').text == 'Date of Delivery':
					Date = val3.find('Value').text	
					print WebAccessToken
					download_file('https://www.gocanvas.com/submission_files/%s/download' % WebAccessToken, School,Date,Location, WebAccessToken[:5])


				



