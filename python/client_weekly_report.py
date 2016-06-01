import gspread
import json
from oauth2client.client import SignedJwtAssertionCredentials
import pandas
from datetime import datetime,date,timedelta
import xlrd	
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from datetime import datetime
import smtplib
import numpy as np

info_wb = xlrd.open_workbook('/Users/jimmydeblasio/Desktop/python_scripts/info.xls')
info_ws = info_wb.sheet_by_index(0)
creds = info_ws.col_values(1)

def send_mail(body):
	fromaddr = creds[0]
	toaddr = 'reports@jdgraphic.com'
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	now = datetime.now()
	msg['Subject'] = 'Bradford Weekly Revenue Summary// %s-%s-%s %s:%s:%s' % (now.year, now.day, now.year, now.hour, now.minute, now.second)

	body =  '%s' % body 
	msg.attach(MIMEText(body, 'html'))
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(fromaddr, creds[1])
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()

def isfloat(x):
	try:
		float(x)
		return True
	except ValueError:
		return False

def remove_dollar(x):
	if x == 0:
		return 0
	else: 
		return x.replace('$','')

def remove_comma(x):
	if isfloat(x): 
		return float(x)
	else: 
		return x.replace(',','')

def upper_case(x):
	if isfloat(x):
		return x
	else: 
		return x.upper()

#to_datetime = lambda d: datetime.strptime(d,'%m/%d/%Y').date()

json_key = json.load(open('/Users/jimmydeblasio/Desktop/python_scripts/jimmy_test-95f0e3228561.json'))
scope = ['https://spreadsheets.google.com/feeds']

credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)

gc = gspread.authorize(credentials)
gco = gc.open_by_url('https://docs.google.com/spreadsheets/d/1mmVPa1xTwxWwJUweyi0HGoOjRqr9Hl9GpcUVFg5Tdog/edit#gid=466847261')
boworksheet = gco.get_worksheet(0)
all_data  = pandas.DataFrame(boworksheet.get_all_records(empty2zero=True, head=1))


all_data['Ship Date'] = pandas.to_datetime(all_data['Ship Date'])
all_data['CPM'] = all_data['CPM'].map(remove_dollar)
all_data['CPM'] = all_data['CPM'].convert_objects(convert_numeric=True)
all_data['Quantity Ordered'] = all_data['Quantity Ordered'].map(remove_comma)
all_data['Quantity Ordered'] = all_data['Quantity Ordered'].convert_objects(convert_numeric=True)
all_data['Component ID'] = all_data['Component ID'].map(upper_case)
all_data['Total Billed'] = np.round((all_data['Quantity Ordered'] / 1000) * all_data['CPM'],2)
all_data['Week Number'] = all_data['Ship Date'].dt.week


d = date.today() - timedelta(days=365)
filtered_data = all_data[all_data['Ship Date'] >= d].sort('Ship Date',ascending = True)
weekly_total_buyer = filtered_data.groupby(by=['Week Number'])['Total Billed'].sum()

df1 = weekly_total_buyer.to_frame()
send_mail(df1.to_html())


#send mail
#send_mail(filtered_data[['Ship Date','Component ID','Paper Lbs', 'Total Cost']].to_html())



