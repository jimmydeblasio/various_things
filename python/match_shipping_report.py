import json,gspread,smtplib,unicodedata, collections,glob,os
from oauth2client.client import SignedJwtAssertionCredentials
from datetime import datetime,date,timedelta
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText



#import info and shipping report spreadsheet
import xlrd
workbook = xlrd.open_workbook(max(glob.iglob(' removed '), key=os.path.getctime))
worksheet = workbook.sheet_by_index(0)
u_pos = worksheet.col_values(1)
idates = worksheet.col_values(7)
u_pos.pop(0)
idates.pop(0)
upcoming_processed = []
ok = []
check = [] 

file_used = os.path.basename(os.path.realpath(max(glob.iglob('removed '), key=os.path.getctime)))

#send email if error if not processed

def isfloat(x):
	try:
		float(x)
		return True
	except ValueError:
		return False

def send_mail(body):
	info_wb = xlrd.open_workbook('removed')
	info_ws = info_wb.sheet_by_index(0)
	creds = info_ws.col_values(1)
	fromaddr = creds[0]
	toaddr = creds[2]
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	now = datetime.now()
	msg['Subject'] = 'Match Procesed Orders Against Shipping Report// %s-%s-%s %s:%s:%s' % (now.month, now.day, now.year, now.hour, now.minute, now.second)

	body =  '%s' % body 
	msg.attach(MIMEText(body, 'plain'))
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(fromaddr, creds[1])
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()


#create class and normalize 
class PurchaseOrder:
	def __init__ ( self, x ):
		self.Division = x['Division']
		self.ModifiedOrder = x['Modified Order']
		self.Component_ID = str(x['Component ID']).replace('_','').upper().replace('-','')
		CPM_str = x['CPM'][1:]
		self.po_no = str(x['PO Number'])
		if isfloat(CPM_str):
			self.CPM = float(CPM_str)
		else:
			self.CPM = 0
		Quantity_str = str(x['Quantity Ordered']).replace(',','')
		if isfloat(Quantity_str):
			self.Qty = float(Quantity_str)/1000
		else:
			self.Qty = 0
		self.Buyer = x['Buyer']
		self.odate = x['Order Date']
		if self.odate:
			self.odate = datetime.strptime(self.odate,'%m/%d/%Y').date()
		else:
			self.odate = datetime.strptime('1/1/1111','%m/%d/%Y').date()
		self.sdate = x['Ship Date']
		if self.sdate:
			self.sdate = datetime.strptime(self.sdate,'%m/%d/%Y').date()
		else:
			self.sdate = datetime.strptime('1/1/1111','%m/%d/%Y').date()	
		#self.date = datetime.strptime(x['Order Date'],'%m/%d/%y')

#json auth
json_key = json.load(open('removed '))
scope = ['https://spreadsheets.google.com/feeds']

credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)

gc = gspread.authorize(credentials)
gco = gc.open_by_url(' removed')

boworksheet = gco.worksheet("Bradford Orders")
all_data  = boworksheet.get_all_records(empty2zero=False, head=1)
purchaseorders = [PurchaseOrder(x) for x in all_data]


#upcoming pos processed
#d = date.today() #- timedelta(days=7)
for x in purchaseorders:
	#if x.sdate >= d:
	upcoming_processed.append(x.po_no)

#verify shipping report pos have been processed
for y in u_pos:
	if y in upcoming_processed:
		ok.append(y)
	else:
		check.append(y)

#find duplicates in upcoming_processed
dups = [item for item, count in collections.Counter(upcoming_processed).items() if count > 1]

#send mail 
send_mail('https://docs.google.com/spreadsheets/d/1mmVPa1xTwxWwJUweyi0HGoOjRqr9Hl9GpcUVFg5Tdog/edit#gid=0\n\n\nfile used: %s\n\n\nthese have not been processed:\n%s\n\n\n possible duplicates(remove first instance):%s' % (file_used,'\n'.join(map(str, check)),'\n'.join(map(str, dups))))






