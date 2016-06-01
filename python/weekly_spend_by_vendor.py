import pymysql
import pandas as pd
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from datetime import datetime
import smtplib
import xlrd
from prettytable import PrettyTable
from prettytable import from_db_cursor

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
	msg['Subject'] = 'Weekly Spend// %s-%s-%s %s:%s:%s' % (now.month, now.day, now.year, now.hour, now.minute, now.second)

	body =  '%s' % body 
	msg.attach(MIMEText(body, 'html'))
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(fromaddr, creds[1])
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()

def sql_email(x):
	conn = pymysql.connect(host= creds[5], port=3306, user= creds[6], passwd= creds[7], db=creds[8])
	cur = conn.cursor()
	cur.execute(x)
	pt = from_db_cursor(cur)
	send_mail(pt.get_html_string())
	cur.close()
	conn.close()


sql_email("SELECT supplier_name as 'Supplier', concat('$',FORMAT(sum(lineitem_cost),0)) as 'Total Spent'  FROM orders_supplies WHERE date >= Date_sub(now(), INTERVAL 7 DAY) GROUP BY supplier_name ORDER By sum(lineitem_cost) desc ")



