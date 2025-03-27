#Final code to fetch 7 day's weather forecasting information from IMD for city guwahati
#Updation of those data to a mysql database
import pandas as pd
from pandas.io import sql
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
from sqlalchemy import create_engine
import requests
from bs4 import BeautifulSoup

url_list=['http://14.139.247.11/citywx/city_weather.php?id=40001','http://14.139.247.11/citywx/city_weather.php?id=42406']
          #'http://14.139.247.11/citywx/city_weather.php?id=42314','http://14.139.247.11/citywx/city_weather.php?id=42407',
          #'http://14.139.247.11/citywx/city_weather.php?id=42420','http://14.139.247.11/citywx/city_weather.php?id=42410']
while url_list:
    url1=url_list.pop()
    page=requests.get(url1)
    soup=BeautifulSoup(page.text, 'html.parser')
    table_only=soup.find_all('table')
    #FOR CITY NAME
    t1_data=table_only[0]
    #print (t1_data.prettify())
    t1_data.prettify()
    t1_rows=t1_data.find("tr")
    #print (t1_rows)
    t1_column1=t1_rows.find("img")
    img_name=t1_column1['alt']
    city_name=[img_name]
    #print (img_name)# prints output as guwahati
    #FOR FIRST TABLE CONTENTS
    #tr_txt1=soup.find_all('tr')[2:11]
    tr_txt1=soup.find_all('tr')[6:7]
    #print (tr_txt1)
    column1=[]
    column2=[]
    for rw1 in tr_txt1:
        column1.append(rw1.find('td').text.strip())
        column2.append(rw1.find_all('td')[1].text.strip())
    #FOR SECOND TABLE CONTENTS
        c1_date=[]
        c2_mintemp=[]
        c3_maxtemp=[]
        c4_img=[]
        c5_desc=[]
        rowss=soup.find_all('tr')[13:20]
        #print (rowss)
    for row in rowss:
        columns=row.find_all('td')[0:]
        cols1=columns[0]
        c1_date.append(cols1.text.strip())
        cols2=columns[1]
        c2_mintemp.append(cols2.text.strip())
        cols3=columns[2]
        c3_maxtemp.append(cols3.text.strip())
        cols4=columns[3]
        cols4_img=cols4.find("img")
        cols4_imgname=cols4_img['src']
        c4_img.append([cols4_imgname])
    columns5=soup.find_all("td",attrs={"width":"255","align":"center"})
    for cols5 in columns5:
        c5_desc.append(cols5.text.strip())
    weather1=pd.DataFrame({
    "City Name": city_name
     })
    #print (weather1)
    weather2=pd.DataFrame({
    "City Name": city_name,
    "Rainfall Status": column1,
    "data": column2
    })
    #print (weather2)
    weather3=pd.DataFrame({
    "7 days weather forecasting Info - date:":c1_date,
    "Min temp":c2_mintemp,
    "Max temp":c3_maxtemp,
    "Weather Image":c4_img,
    "Description":c5_desc
    })
    #print (weather3)
    engine=create_engine("mysql+mysqldb://root:Pwd123@127.0.0.1/assamdb")
    if(url1=="http://14.139.247.11/citywx/city_weather.php?id=40001"):
        weather2.to_sql(name='barpeta_name',con=engine, if_exists='replace', index=False)
        weather3.to_sql(name='barpeta_weather',con=engine, if_exists='replace', index=True)
        print(pd.read_sql(('select * from barpeta_name'),engine))
        print(pd.read_sql(('select * from barpeta_weather'),engine))
    elif(url1=="http://14.139.247.11/citywx/city_weather.php?id=42406"):
        weather2.to_sql(name='dhubri_name',con=engine, if_exists='replace', index=False)
        weather3.to_sql(name='dhubri_weather',con=engine, if_exists='replace', index=True)
        print(pd.read_sql(('select * from dhubri_name'),engine))
        print(pd.read_sql(('select * from dhubri_weather'),engine))

    
#print(pd.read_sql(('select * from citynamedb'),engine))
#print(pd.read_sql(('select * from guwahati_weather'),engine))




