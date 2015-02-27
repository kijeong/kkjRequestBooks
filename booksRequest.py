#!/opt/python34/bin/python3
# coding=euc-kr

# @author : kijeong@netman.co.kr
# @date : 2015-02-26

import sys
import os
import bs4
import http.client

def getBookInfo(strPath):
	#sample https://www.kangcom.com/sub/view.asp?topid=1&sku=201309169340
	strURL = 'www.kangcom.com'
	strPage = strPath.split(strURL)[1]
	if strPage == '':
		return

	c = http.client.HTTPSConnection(strURL, 443)
	#c.request("GET", "/sub/view.asp?topid=1&sku=201309169340")
	c.request("GET", strPage)
	response = c.getresponse()
	#print(response.status, response.reason)
	if response.status != 200:
		print("error status")
		return
	data = response.read()
	soup = bs4.BeautifulSoup(data.decode('euc-kr'))
	strTitle = soup.body.find_all(id='item-title')[0].contents[0]
	strPublisher = soup.body.find_all('a')[-3].contents[0]

	fIsStr = lambda x : type(x) == bs4.element.NavigableString 
	if fIsStr(soup.body.find_all('a')[-4].contents[0]):
		strAuthor = soup.body.find_all('a')[-4].contents[0]
	else:
		#strAuthor = "NOTLINK"
		strAuthor = soup.body.find_all('td', "detail_title")[0].contents[3].span.next_sibling.split('\n')[1].strip()
	strAuthor = strAuthor.replace(',', '&')

	strPrice = soup.body.find_all('span', 'listfont4')[0].contents[0].strip('원')
	strPrice = strPrice.replace(',', '')
	strDate = soup.body.find_all('td', 'listfont3')[0].contents[0].split('|')[0].strip()

	# isbn10 | isbn13(barcode)
	strISBN = soup.body.find_all('td', 'listfont3')[1].contents[2].split('|')[0].strip()
	line = ', '
	print(line.join((strTitle, strAuthor, strPublisher, strDate, strPrice, strISBN)))	

if __name__ == "__main__" :
	if len(sys.argv) == 1 :
		print("[usage] : " + sys.argv[0] + " {\"the kangcom book url\"|the url listed file name}") 
		sys.exit()
	if os.access(sys.argv[1], os.R_OK) == True:
		fileIn = open(sys.argv[1], 'r')
		lstFileIn = fileIn.readlines()
		fileIn.close()
		for line in lstFileIn:
			strStripLine = line.strip()
			if strStripLine == '':
				continue
			getBookInfo(strStripLine)
	else:	
		getBookInfo(sys.argv[1])
