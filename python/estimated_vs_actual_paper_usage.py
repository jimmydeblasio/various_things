import urllib2
import xml.etree.ElementTree as ElementTree
import pandas
import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials
import xlrd
import pymysql
from datetime import datetime,date,timedelta
from tabulate import tabulate
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from datetime import datetime
import smtplib


#date variables 
end_date = date.today()
start_date = date.today() #- timedelta(days=7)
start_date = start_date.strftime('%m/%d/%y')
end_date = end_date.strftime('%m/%d/%y')

#import sql and credentials
info_wb = xlrd.open_workbook('/Users/jimmydeblasio/Desktop/python_scripts/info.xls')
info_ws = info_wb.sheet_by_index(0)
creds = info_ws.col_values(1)
conn = pymysql.connect(host= creds[5], port=3306, user= creds[6], passwd= creds[7], db=creds[8])
sql = "select job_no,paper_amount0 from tbl_projects_job" 
dfsql = pandas.read_sql_query(sql,conn)
dfsql['paper_amount0'] = dfsql['paper_amount0'].convert_objects(convert_numeric=True)

#import mail
def send_mail(body):
	fromaddr = creds[0]
	toaddr = 'reports@jdgraphic.com'
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	now = datetime.now()
	msg['Subject'] = 'Daily Web Report// %s-%s-%s %s:%s:%s' % (now.year, now.day, now.year, now.hour, now.minute, now.second)

	body =  '%s' % body 
	msg.attach(MIMEText(body, 'html'))
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(fromaddr, creds[1])
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()


#import gocanvas data
url = urllib2.urlopen(' removed link'  % (start_date, end_date))  
tree = ElementTree.parse(url)
doc = tree.getroot()
labels = []
values = []
job_no = []
total_weight = []

for elem in doc.iter('Label'):
	labels.append(elem.text)

for elem in doc.iter('Value'):
	values.append(elem.text)

adict = zip(labels,values)

for key, value in adict:
		if key == 'Job No':
			job_no.append(value)

for key, value in adict:
		if key == 'Pounds Used': 
			total_weight.append(value)


#analyze data with pandas
dictionary = zip(job_no, total_weight)	
df = pandas.DataFrame(dictionary,columns=['job_no', 'amount_used'])
df['amount_used'] = df['amount_used'].convert_objects(convert_numeric=True)
df = df.groupby(['job_no']).sum()
df = pandas.DataFrame(df).reset_index()

df = df[['job_no','amount_used']]
total_df = pandas.merge(df, dfsql, on='job_no', how='left')
total_df['difference'] = total_df['amount_used'] - total_df['paper_amount0']
total_df = total_df.set_index('job_no')

#print data 
send_mail(tabulate(total_df, headers=["job_no","actual_usage", "projected_usage","difference"], tablefmt="html"))


