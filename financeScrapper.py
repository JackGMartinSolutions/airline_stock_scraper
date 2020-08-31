import requests
import csv
import smtplib
import re

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bs4 import BeautifulSoup

def AA():
    page = requests.get("https://ca.finance.yahoo.com/quote/AAL?p=AAL&.tsrc=fin-srch")
    #print("STATUS: ",page.status_code)
    soup = BeautifulSoup(page.content, 'html.parser')

    priceCatcher=soup.find(class_="D(ib) Va(m) Maw(65%) Ov(h)")
    priceAtClose=priceCatcher.find(class_="Trsdu(0.3s)").get_text()
    percentDifference=priceCatcher.find(class_="Fw(500)").get_text()
    actualPercent=re.search('\(([^)]+)',str(percentDifference)).group(1)
    actualPercent=actualPercent[:-1]


    #print(priceCatcher.prettify())
    #print('American Price at Close: ',priceAtClose.get_text())
    return [priceAtClose,actualPercent,"american"]

def Delta():
    page = requests.get("https://ca.finance.yahoo.com/quote/DAL?p=DAL")
    #print("STATUS: ",page.status_code)
    soup = BeautifulSoup(page.content, 'html.parser')

    priceCatcher=soup.find(class_="D(ib) Va(m) Maw(65%) Ov(h)")
    priceAtClose=priceCatcher.find(class_="Trsdu(0.3s)").get_text()
    percentDifference=priceCatcher.find(class_="Fw(500)").get_text()
    actualPercent=re.search('\(([^)]+)',str(percentDifference)).group(1)
    actualPercent=actualPercent[:-1]

    #print(priceCatcher.prettify())
    #print('Delta Price at Close: ',priceAtClose.get_text())
    return [priceAtClose,actualPercent,"delta"]

def SouthWest():
    page = requests.get("https://ca.finance.yahoo.com/quote/LUV?p=LUV")
    #print("STATUS: ",page.status_code)
    soup = BeautifulSoup(page.content, 'html.parser')

    priceCatcher=soup.find(class_="D(ib) Va(m) Maw(65%) Ov(h)")
    priceAtClose=priceCatcher.find(class_="Trsdu(0.3s)").get_text()
    percentDifference=priceCatcher.find(class_="Fw(500)").get_text()
    actualPercent=re.search('\(([^)]+)',str(percentDifference)).group(1)
    actualPercent=actualPercent[:-1]

    #print(priceCatcher.prettify())
    #print('SouthWest Price at Close: ',priceAtClose.get_text())
    return [priceAtClose,actualPercent,"southwest"]

def SendEmail(possible_buyers):
    myMessage=''
    for n in possible_buyers:
        print('---',n)
        myMessage+= n[2]+' Dropped '+n[1]+'%'+' Price: '+n[0]+'\n'
    print(myMessage)

    mail_content='''Fincae EMAIL.'''
    #The mail addresses and password
    sender_address='jgmartin318@gmail.com'
    sender_pass='Jackashforlife1'
    receiver_address='jimmyBean351@gmail.com'

    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'STOCK PRICE DROP'   #The subject line

    #The body and the attachments for the mail
    message.attach(MIMEText(myMessage, 'plain'))

    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')

airlines=[]
airlines.append(AA())
airlines.append(Delta())
airlines.append(SouthWest())

print(airlines)

possible_buyers=[]


for key,value,company in airlines:
    print("VALUE: ",value)
    if(float(value)<-1.5):
        possible_buyers.append([key,value,company])


print("possible buyers: ", possible_buyers)

SendEmail(possible_buyers)




# with open('airlineStocks.csv', 'w',newline='') as f:
#     writer = csv.writer(f)
#     writer.writerow(['AIRLINE','STOCK PRICE'])
#     for key,value in airlines.items():
#         writer.writerow([key,value])