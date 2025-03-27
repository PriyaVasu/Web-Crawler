#Earthquake code with phantomjs webdriver
from selenium import webdriver
import os
from selenium.webdriver.support.ui import Select
import pandas as pd
from pandas.io import sql
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb 
from sqlalchemy import create_engine
import re
from bs4 import BeautifulSoup
import requests
from pprint import pprint
import threading
from threading import Thread
import time

def earthquake():
    while True:        
        try:
            engine5=create_engine("mysql+mysqldb://root:Pwd123@127.0.0.1/disaster_eq_backup")
            with engine5.connect() as con5:
                driver=webdriver.Firefox()
                url="http://seismo.imd.gov.in/eq_info/eq.html"
                driver.get(url)
                html_source=driver.page_source
                soup=BeautifulSoup(html_source,"html.parser")

                c1_date=[]
                c2_utc=[]
                c3_ist=[]
                c4_lat=[]
                c5_long=[]
                c6_depth=[]
                c7_mag=[]
                c8_region=[]
                #cols=[]

                table2_row1=soup.find_all("tr")[0:2]
                cols=table2_row1[1].find_all('td')[0:]
                c1_date.append(cols[0].text.strip())
                c2_utc.append(cols[1].text.strip())
                c3_ist.append(cols[2].text.strip())
                c4_lat.append(cols[3].text.strip())
                c5_long.append(cols[4].text.strip())
                c6_depth.append(cols[5].text.strip())
                c7_mag.append(cols[6].text.strip())
                c8_region.append(cols[7].text.strip())

                pd_eq=pd.DataFrame({
                    "date_eq":c1_date,
                    "time_utc":c2_utc,
                    "time_ist":c3_ist,
                    "epicentre_lat":c4_lat,
                    "epicentre_long":c5_long,
                    "depth_km":c6_depth,
                    "magnitute":c7_mag,
                    "region":c8_region
                    })
                #print (str(c1_date))
                #print(pd_eq)
                
                if url=="http://seismo.imd.gov.in/eq_info/eq.html":
                    #To get recent date from table
                    result1=con5.execute("SELECT date_eq FROM `eq` ORDER BY id DESC LIMIT 1")
                    for recent_date in result1:
                        #print("recent date="+recent_date[0])
                        recent_dt=recent_date[0]
                        #print(recent_dt)
                    #To get recent time_utc from table
                    result3=con5.execute("SELECT time_ist FROM `eq` ORDER BY id DESC LIMIT 1")
                    for recent_itime in result3:
                        #print ("recent time="+recent_itime[0])
                        rec_itime=recent_itime[0]
                        #print(rec_itime)
                    
                    #To get old date in table
                    result2=con5.execute("SELECT date_eq FROM `eq` ORDER BY id ASC LIMIT 1")
                    for old_date in result2:
                        #print(old_date[0])
                        old_dt=old_date[0]
                        #print(old_dt)

                    x=True
                    while x:    
                        if (str(c1_date)=="['"+recent_dt+"']") and (str(c3_ist=="['"+rec_itime+"']")):
                            #print("date and time gets matches")
                            x=False
                            break
                        
                        elif str(c1_date)=="['"+recent_dt+"']":
                            pd_eq.to_sql(name='eq', con=engine5, if_exists='append', index=False)
                            pd_eq.to_sql(name='eq_backup', con=engine5, if_exists='append', index=False)
                            con5.execute("ALTER TABLE `eq` DROP `id`")
                            con5.execute("ALTER TABLE `eq` AUTO_INCREMENT = 1")
                            con5.execute("ALTER TABLE `eq` ADD `id` int(25) UNSIGNED NOT NULL AUTO_INCREMENT FIRST, ADD INDEX(`id`)")
                            con5.execute("ALTER TABLE `eq_backup` DROP `id`")
                            con5.execute("ALTER TABLE `eq_backup` AUTO_INCREMENT = 1")
                            con5.execute("ALTER TABLE `eq_backup` ADD `id` int(25) UNSIGNED NOT NULL AUTO_INCREMENT FIRST, ADD INDEX(`id`)")
                            x=False
                            
                        else:
                            pd_eq.to_sql(name='eq', con=engine5, if_exists='append', index=False)
                            pd_eq.to_sql(name='eq_backup', con=engine5, if_exists='append', index=False)
                            row_count=con5.execute("SELECT COUNT(*) FROM `eq`")
                            for count in row_count:
                                cnt=count[0]
                                #print(cnt)
                            while (cnt>0):
                                result3=con5.execute("SELECT date_eq FROM `eq` ORDER BY id ASC LIMIT 1")
                                for row_del in result3:
                                    row_del[0]
                                    #print(row_del[0])
                                if old_dt==row_del[0]:
                                    con5.execute("DELETE FROM `eq` ORDER BY `id` ASC LIMIT 1")
                                    con5.execute("ALTER TABLE `eq` DROP `id`")
                                    con5.execute("ALTER TABLE `eq` AUTO_INCREMENT = 1")
                                    con5.execute("ALTER TABLE `eq` ADD `id` int(25) UNSIGNED NOT NULL AUTO_INCREMENT FIRST, ADD INDEX(`id`)")
                                else:
                                    break
                                cnt=cnt-1
                                x=False
        finally:
            con5.close()

        driver.quit()
        time.sleep(1800)

def executeSomething():
    while True:
        engine1=create_engine("mysql+mysqldb://root:Pwd123@127.0.0.1/weather_db")
        try:
            with engine1.connect() as con1:

                def func(url_list,loc_id):
                    while url_list and loc_id:
                            loc_pid=loc_id.pop()
                            url1=url_list.pop()
                            driver.get(url1)
                            html_source=driver.page_source
                            soup=BeautifulSoup(html_source,"html.parser")
                            t_row=False
                            tables=[]
                            c1_date=[]
                            c2_rain=[]
                            c3_maxtemp=[]
                            c4_mintemp=[]
                            c5_cloud=[]
                            c6_maxhum=[]
                            c7_minhum=[]
                            c8_windsd=[]
                            c9_windir=[]
                            count=0
                            for line in soup.pre.get_text().splitlines():
                                if not t_row and "DAY-1" in line:
                                    t_row=True
                                    table=[]
                                    continue

                                if t_row and not line.strip():
                                    t_row=False
                                    tables.append(table)
                                    continue
                                if t_row:
                                    count=count+1
                                    if not (str(count)=='2' or str(count)=='11'):
                                        table=re.split("\s{2,}",line)
                                        if str(count)=='1':
                                            c1_date=table[1:]
                                        elif str(count)=='3':
                                            c2_rain=table[1:]
                                        elif str(count)=='4':
                                            c3_maxtemp=table[1:]
                                        elif str(count)=='5':
                                            c4_mintemp=table[1:]
                                        elif str(count)=='6':
                                            c5_cloud=table[1:]
                                        elif str(count)=='7':
                                            c6_maxhum=table[1:]
                                        elif str(count)=='8':
                                            c7_minhum=table[1:]
                                        elif str(count)=='9':
                                            c8_windsd=table[1:]
                                        elif str(count)=='10':
                                            c9_windir=table[1:]
                                            
                            day1_rain=con1.execute("SELECT day_rainfall FROM `m2_rainfall_all` WHERE location_id=%s ORDER BY rainfall_ai_id DESC LIMIT 3,1",(loc_pid))
                            day1_name=con1.execute("SELECT day_name FROM `m2_rainfall_all` WHERE location_id=%s ORDER BY rainfall_ai_id DESC LIMIT 3,1",(loc_pid))
                            for r1 in day1_rain:
                                if str(r1)=="("+c2_rain[0]+","+")":
                                    break;
                                else:
                                    for d1 in day1_name:
                                        if str(d1)=="('"+c1_date[0]+"',)":
                                            con1.execute("UPDATE `m2_rainfall_all` SET day_rainfall=%s WHERE location_id=%s AND day_name=%s",(c2_rain[0],loc_pid,c1_date[0]))
                                    
                            day2_rain=con1.execute("SELECT day_rainfall FROM `m2_rainfall_all` WHERE location_id=%s ORDER BY rainfall_ai_id DESC LIMIT 2,1",(loc_pid))
                            day2_name=con1.execute("SELECT day_name FROM `m2_rainfall_all` WHERE location_id=%s ORDER BY rainfall_ai_id DESC LIMIT 2,1",(loc_pid))
                            for r2 in day2_rain:                
                                if str(r2)=="("+c2_rain[1]+","+")":
                                    break;
                                else:
                                    for d2 in day2_name:
                                        if str(d2)=="('"+c1_date[1]+"',)":
                                            con1.execute("UPDATE `m2_rainfall_all` SET day_rainfall=%s WHERE location_id=%s AND day_name=%s",(c2_rain[1],loc_pid,c1_date[1]))

                            day3_rain=con1.execute("SELECT day_rainfall FROM `m2_rainfall_all` WHERE location_id=%s ORDER BY rainfall_ai_id DESC LIMIT 1,1",(loc_pid))
                            day3_name=con1.execute("SELECT day_name FROM `m2_rainfall_all` WHERE location_id=%s ORDER BY rainfall_ai_id DESC LIMIT 1,1",(loc_pid))
                            for r3 in day3_rain:                
                                if str(r3)=="("+c2_rain[2]+","+")":
                                    break;
                                else:
                                    for d3 in day3_name:
                                        if str(d3)=="('"+c1_date[2]+"',)":
                                            con1.execute("UPDATE `m2_rainfall_all` SET day_rainfall=%s WHERE location_id=%s AND day_name=%s",(c2_rain[2],loc_pid,c1_date[2]))

                            day4_rain=con1.execute("SELECT day_rainfall FROM `m2_rainfall_all` WHERE location_id=%s ORDER BY rainfall_ai_id DESC LIMIT 0,1",(loc_pid))
                            day4_name=con1.execute("SELECT day_name FROM `m2_rainfall_all` WHERE location_id=%s ORDER BY rainfall_ai_id DESC LIMIT 0,1",(loc_pid))
                            for r4 in day4_rain:                
                                if str(r4)=="("+c2_rain[3]+","+")":
                                    break;
                                else:
                                    for d4 in day4_name:
                                        if str(d4)=="('"+c1_date[3]+"',)":
                                            con1.execute("UPDATE `m2_rainfall_all` SET day_rainfall=%s WHERE location_id=%s AND day_name=%s",(c2_rain[3],loc_pid,c1_date[3]))

                            con1.execute("""INSERT INTO `m2_rainfall_all`(rainfall_ai_id,location_id,day_name,day_rainfall) VALUES (NULL,%s,%s,%s)""",(loc_pid,c1_date[4],c2_rain[4]))

                            #print(url1,loc_pid)
                            #print(c1_date[0],c1_date[1],c1_date[2],c1_date[3],c1_date[4])
                            #print(c2_rain[0],c2_rain[1],c2_rain[2],c2_rain[3],c2_rain[4])
                            
                #Passing URL Statewise
                #os.environ['NO_PROXY'] = '127.0.0.1'
                driver = webdriver.Firefox()
                state_url=['http://nwp.imd.gov.in/blf/blf_temp/dis.php?value=23manipur',
                           'http://nwp.imd.gov.in/blf/blf_temp/dis.php?value=34tripura',
                           'http://nwp.imd.gov.in/blf/blf_temp/dis.php?value=31sikkim',                                         
                           'http://nwp.imd.gov.in/blf/blf_temp/dis.php?value=24meghalaya',
                           'http://nwp.imd.gov.in/blf/blf_temp/dis.php?value=25mizoram',
                           'http://nwp.imd.gov.in/blf/blf_temp/dis.php?value=26nagaland',
                           'http://nwp.imd.gov.in/blf/blf_temp/dis.php?value=03arunachal-pradesh',
                           'http://nwp.imd.gov.in/blf/blf_temp/dis.php?value=04assam']
                while state_url:
                    state_id=state_url.pop()
                    driver.get(state_id)
                    
                    #Assam State
                    if state_id=="http://nwp.imd.gov.in/blf/blf_temp/dis.php?value=04assam":
                        el=driver.find_element_by_name('dis')
                        for option in el.find_elements_by_tag_name('option'):
                            if (option.text=='BARPETA'):
                                option.click()
                                el.submit()
                                break                  
                        driver.get("http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=04BARPETA")
                        el2=driver.find_element_by_name('block')
                        for option in el2.find_elements_by_tag_name('option'):
                            if (option.text=='BAJALI'):
                                option.click()
                                el2.submit()
                                break
                            
                        url_list=['http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=ROWTA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=PASCHIM-MANGALDAI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=ODALGURI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=MAZBAT',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=KHOIRABARI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=KALAIGAON',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=DALGAON-SIALMARI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=BORSOLA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=BHERGAON',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=BECHIMARI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=04UDALGURI',#UDALGURI
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=SAIKHOWA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=SADIYA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=MARGHERITA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=KAKOPATHAR',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=HAPJAN',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=GUIJAN',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=04TINSUKIA',#TINSUKIA
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=SOOTEA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=SAKOMATHA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=RANGAPARA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=GABHORU',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=DHEKIAJULI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=CHAIDUAR',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=BISWANATH',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=BIHAGURI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=BEHALI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=BALIPARA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=BAGHMARA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=04SONITPUR',#SONITPUR
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=WEST-ABHAIPUR',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=SONARI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=SIVASAGAR',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=SAPEKHATI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=NAZIRA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=LAKUWA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=GAURISAGAR',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=DEMOW',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=AMGURI',#Siva Sagar
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=NEW-SANGBAR',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=JATINGA-VALLEY',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=HARANGAJAO',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=DIYUNGBRA',#North-cachar-hills
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=TIHU',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=PASCHIM-NALBARI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=MADHUPUR',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=BARKHETRI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=04NALBARI',#Narbari
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=RUPAHI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=RAHA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=PACHIM-KALIABOR',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=MOIRABARI-PART',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=LUMDING',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=LAOKHOWA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=KATHIATOLI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=KALIABOR',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=JURIA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=DHALPUKHURI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=BINAKANDI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=BATADRAVA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=BARHAMPUR',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=BAJIAGAON',#Nagaon
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=MOIRABARI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=MAYANG',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=LAHARIGHAT',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=BHURBANDHA',#Marigaon
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=NOWBOICHA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=NARAYANPUR',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=LAKHIMPUR',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=GHILAMARA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=DHAKUAKHANA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=BOGINADI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=BIHPURIA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=04LAKHIMPUR',#LAKHIMPUR
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=RUPSHI-BTC',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=KOKRAJHAR',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=KACHUGAON',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=HATIDHURA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=GOSSAIGAON',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=GOLAKGANJ-BTC',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=DOTMA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=DEBITOLA-BTC',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=CHAPOR-SALKOCHA-BTC',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=BILASHIPARA-BTC',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=04KOKRAJHAR',#KOKRAJHAR
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=RAMKRISHNA-NAGAR',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=PATHARKANDI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=NORTH-KARIMGANJ',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=LOWAIRPOA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=DULLAVCHERRA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=BADARPUR',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=04KARIMGANJ',#KARIMGANJ
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=SAMELANGSO',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=RONGKHANG',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=HOWRAGHAT',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=BOKAJAN',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=04KARBI-ANGLONG',#
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=SUALKUCHI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=RANI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=RANGIA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=RAMPUR',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=KAMALPUR',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=HAJO',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=GOROIMARI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=BONGAON',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=BOKO',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=BIHIDIA-JAJIKONA',#kamrup
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=RANI%28PT%29',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=DIMORIA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=CHANDRAPUR',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=BEZERA%28PT%29',#Bezera(PT)
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=UJANI-MAJULI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=TITABOR',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=MAJULI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=KALIAPANI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=JORHAT-EAST',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=JORHA-CENTRAL',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=JORHAT',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=04JORHAT',#JORHAT
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=LALA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=KATLICHERRA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=HAILAKANDI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=ALGAPUR',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=04HAILAKANDI',#HAILAKANDI
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=KAKODONGA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=GOMARIGURI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=GOLAGHAT-WEST',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=GOLAGHAT-SOUTH',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=GOLAGHAT-NORTH',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=GOLAGHAT-EAST',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=GOLAGHAT-CENTRAL',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=04GOLAGHAT',#GOLAGHAT
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=RONGJULI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=MATIA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=LAKHIPUR',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=KUCHDHOWA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=KRISHNAI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=KHARMUZA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=JALESWAR',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=BALIJANA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=04GOALPARA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=TINGKHONG',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=TENGAKHAT',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=PANITOLA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=LAHOAL',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=KHOWANG',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=JOYPUR',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=BARBARUAH',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=04DIBRUGARH',#DIBRUGARH
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=SOUTH-SALMARA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=RUPSHI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=NAYERALGA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=MANKACHAR',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=MAHAMAYA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=JAMADARHAT',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=HATIDHURA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=GOLAKGANJ',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=GAURIPUR',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=FEKAMARI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=DEBITOLA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=CHAPAR-SALKOCHA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=BILASIPARA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=AGOMANI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=04DHUBRI',#Dhubri
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=SISSIBORGAON',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=MURKONGSELEK',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=MACHKHOWA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=DHEMAJI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=BORDOLONI',#Dhemaji
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=SIPAJHAR',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=PACHIM-MANGALDAI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=KALAIGAON',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=DALGAON-SIALMARI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=BECHIMARI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=04DARRANG',#DARRANG
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=SIDLI-CHIRANG-PART',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=04CHIRANG',#CHIRANG
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=UDHARBOND',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=SONAI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=SILCHAR',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=SALCHAPRA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=RAJABAZAR',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=PALONGHAT',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=NARSINGPUR',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=LAKHIPUR',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=KATIGORAH',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=KALAIN',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=BORKHOLA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=BINNAKANDI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=BANSKANDI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=04CACHAR',#Cachar
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=SRIJANGRAM',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=MANIKPUR',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=BOITAMARI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=DANGTOL',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=04BONGAIGAON',#BONGAIGAON Dist
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=RUPAHI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=PAKABETBARI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=MANDIA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=GOMAPHULBARI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=GOBARDHANA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=CHANGA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=CHAKCHAKA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=BHABANIPUR',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=BARPETA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=BAJALI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=04BARPETA',#Barpeta District
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=TAMULPUR',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=NAGRIJULI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=JALAH',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=GORESWAR',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=DHAMDHAMA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=BASKA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=BARAMA'] #BARAMA District               
                        loc_id=[232,231,230,229,228,227,226,225,224,223,222,
                                221,220,219,218,217,216,215,
                                214,213,212,211,210,209,208,207,206,205,204,203,
                                202,201,200,199,198,197,196,195,194,
                                192,191,190,189,
                                187,186,185,184,183,
                                182,181,180,179,178,177,176,175,174,173,172,171,170,169,
                                167,166,165,164,
                                162,161,160,159,158,157,156,155,
                                154,153,152,151,150,149,148,147,146,145,144,
                                143,142,141,140,139,138,137,
                                136,135,134,133,132,
                                131,130,129,128,127,126,125,124,123,122,
                                120,119,118,117,
                                115,114,113,112,111,110,109,108,
                                107,106,105,104,103,
                                102,101,100,99,98,97,96,95,
                                94,93,92,91,90,89,88,87,86,
                                85,84,83,82,81,80,79,78,
                                77,76,75,74,73,72,71,70,69,68,67,66,65,64,63,
                                62,61,60,59,58,
                                56,55,54,53,52,51,
                                50,49,
                                48,47,46,45,44,43,42,41,40,39,38,37,36,35,
                                34,33,32,31,30,
                                29,28,27,26,25,24,23,22,21,20,19,
                                18,17,16,15,14,13,12]
                        func(url_list,loc_id)
                        
                    #Arunachal-Pradesh
                    elif state_id=="http://nwp.imd.gov.in/blf/blf_temp/dis.php?value=03arunachal-pradesh":
                        el=driver.find_element_by_name('dis')

                        for option in el.find_elements_by_tag_name('option'):
                            if (option.text=='CHANGLANG'):
                                option.click()
                                el.submit()
                                break                  
                        driver.get("http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=03CHANGLANG")
                        el2=driver.find_element_by_name('block')
                        for option in el2.find_elements_by_tag_name('option'):
                            if (option.text=='BORDUMSA'):
                                option.click()
                                el2.submit()
                                break
                            
                        url_list=['http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=MECHUKA-TATO',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=LIROMOBA-YOMCHA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=LIKABALI-KANGKU',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=GENSI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=DARING',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=DARAK-KAMBA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=BASAR',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=ALONG-EAST-LOWER',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=03WEST-SIANG',#WEST-SIANG
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=SINGCHUNG',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=RUPA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=NAFRA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=KALATANG-BALEMU',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=DIRANG',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=BHALUKPONG-JAMIRI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=03WEST-KAMENG',#WEST-KAMENG
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=SOHA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=PONGCHAU',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=LONGDING',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=LAJU',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=KHONSA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=DEOMALI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=DADAM',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=03TIRAP',#TIRAP
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=ZEMITHANG-DUDUNGHAR',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=TAWANG',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=MUKTO',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=LUMLA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=KITPI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=JANG-THINGBU',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=03TAWANG',#TAWANG
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=NACHO',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=DAPORIJO-SIGIN-II',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=DAPORIJO-SIGIN-I',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=DAPORIJO',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=03UPPER-SUBANSIRI',#UPPER-SUBANSIRI
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=TUTING',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=MARIYANG',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=GEKU-KATAN',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=03UPPER-SIANG',#UPPER-SIANG
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=SAGALEE',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=LOWER-BALIJAN',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=KIMIN',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=DOIMUKH',
                                  #'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=03PAPUM-PARE',#PAPUM-PARE
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=YAZALI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=YACHULI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=TAJANG',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=RAGA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=HIJA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=HARI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=DIIBO',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=03LOWER-SUBANSIRI',#LOWER-SUBANSIRI
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=ROING',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=IDULI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=DAMBUK',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=03LOWER-DIBANG-VALLEY',#LOWER-DIBANG-VALLEY
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=WAKRO',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=TEZU',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=SUNPURA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=NINGROO',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=NAMSAI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=CHOWKHAM',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=03LOHIT',#LOHIT
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=TALI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=NYAPIN',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=LOWER-KOLORIANG',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=CHAMBANG',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=03KURUNG-KUMEY',#KURUNG-KUMEY
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=RIGA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=PANGIN',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=MEBO',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=BOLENG-PEGGING-BOTE',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=03EAST-SIANG',#East-Siang
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=SEPPA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=SEIJOSA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=CHAYANGTAJO',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=BAMENG-WEST',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=BAMENG-EAST',#East-Kameng
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=ANINI-MEPI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=ANELIH-ARZOO',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=03DIBANG-VALLEY',#DIBANG-VALLEY
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=NAMPONG-RIMA-PUTOK',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=MIAO',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=MANMAO-JAIRAMPUR',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=CHANGLANG',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=BORDUMSA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=03CHANGLANG',#CHANGLANG
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=HAYULIANG',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=HAWAI-WALONG',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=CHONGLONGAM']#Arunachal Pradesh -Anzaw District]                
                        loc_id=[463,462,461,460,459,458,457,456,455,
                                454,453,452,451,450,449,448,
                                309,308,307,306,305,304,303,302,
                                301,300,299,298,297,296,295,
                                294,293,292,291,290,
                                289,288,287,286,
                                285,284,283,282,
                                280,279,278,277,276,275,274,273,
                                272,271,270,269,
                                268,267,266,265,264,263,262,
                                261,260,259,258,257,
                                256,255,254,253,252,
                                251,250,249,248,247,
                                245,244,243,
                                242,241,240,239,238,237,
                                236,235,234]                
                        func(url_list,loc_id)
                        
                    #Meghalaya
                    elif state_id=="http://nwp.imd.gov.in/blf/blf_temp/dis.php?value=24meghalaya":
                        el=driver.find_element_by_name('dis')
                        for option in el.find_elements_by_tag_name('option'):
                            if (option.text=='EAST-GARO-HILLS'):
                                option.click()
                                el.submit()
                                break                 
                        driver.get("http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=24EAST-GARO-HILLS")
                        el2=driver.find_element_by_name('block')
                        for option in el2.find_elements_by_tag_name('option'):
                            if (option.text=='DAMBO-RONGUENG'):
                                option.click()
                                el2.submit()
                                break
                        url_list=['http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=NONGSTOIN',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=RANIKOR',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=MAWTHADRAISHAN',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=MAWKYRWAT',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=MAIRANG',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=24WEST-KHASI-HILLS',#WEST-KHASI-HILLS
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=ZIKZAK',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=TIKRIKILLA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=SELSELLA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=RONGRAM',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=GAMBEGRE',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=DALU',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=DADENGGRE',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=BETASING',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=24WEST-GARO-HILLS',#WEST-GARO-HILLS
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=RONGARA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=CHOKPOT',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=BAGHMARA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=24SOUTH-GARO-HILLS',#SOUTH-GARO-HILLS
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=UMSNING',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=UMLING',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=24RI-BHOI',#RI-BHOI
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=THADLASKEIN',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=SAIPUNG',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=LASKEIN',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=KHLIEHRIAT',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=AMLAREM',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=24JAINTIA-HILLS',#JAINTIA-HILLS
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=SHELLA-BHOLAGANJ',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=PYNURSLA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=MYLLIEM',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=MAWSYNRAM',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=MAWRYNGKNENG',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=MAWPHLANG',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=MAWKYNREW',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=24EAST-KHASI-HILLS',#EAST-KHASI-HILLS
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=SONGSAK',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=SAMANDA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=RESUBELPARA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=KHARKUTTA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=DAMBO-RONGUENG',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=24EAST-GARO-HILLS'] #Meghalaya-EAST-GARO-HILLS        
                        loc_id=[447,446,445,444,443,442,
                                441,440,439,438,437,436,435,434,433,
                                432,431,430,429,
                                428,427,426,
                                425,424,423,422,421,420,
                                419,418,417,416,415,414,413,412,
                                411,410,409,408,407,406]                
                        func(url_list,loc_id)
                        
                    #Manipur
                    elif(state_id=="http://nwp.imd.gov.in/blf/blf_temp/dis.php?value=23manipur"):
                        el=driver.find_element_by_name('dis')
                        for option in el.find_elements_by_tag_name('option'):
                            if (option.text=='BISHNUPUR'):
                                option.click()
                                el.submit()
                                break                  
                        driver.get("http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=23BISHNUPUR")
                        el2=driver.find_element_by_name('block')
                        for option in el2.find_elements_by_tag_name('option'):
                            if (option.text=='BISHNUPUR'):
                                option.click()
                                el2.submit()
                                break
                            
                        url_list=['http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=UKHRUL',                  
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=PHUNGYAR',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=KASOM-KHULLEN',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=KAMJONG',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=CHINGAI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=23UKHRUL',#UKHRUL
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=THOUBAL',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=KAKCHING',#Thoubal
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=TOUSEM',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=TAMENGLONG',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=TAMEI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=NUNGBA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=KHOUPUM',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=23TAMENGLONG',#TAMENGLONG
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=TADUBI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=SAITU-GAMPHAZOL',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=SAIKUL',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=PURUL',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=PAOMATA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=KANGPOKPI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=23SENAPATI',#SENAPATI
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=IMPHAL-WEST-II',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=IMPHAL-WEST-I',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=23IMPHAL-WEST',#IMPHAL-WEST
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=JIRIBAM',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=IMPHAL-EAST-II',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=IMPHAL-EAST-I',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=23IMPHAL-EAST',#IMPHAL-EAST
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=TUIBUANG',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=TIPAIMUKH',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=THANION',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=SINGNGAT',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=SANGAIKOT',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=SAIKOT',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=LAMKA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=HENGLEP',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=23CHURACHANDPUR',#CHURACHANDPUR
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=TENGNOUPAL',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=MACHI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=KHENGJOY',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=CHANDEL',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=CHAKPIKARONG',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=23CHANDEL',#CHANDEL
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=MOIRANG',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=BISHNUPUR',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=23BISHNUPUR']#Manipur--BISHNUPUR
                        loc_id=[592,591,590,589,588,587,
                                586,585,
                                583,582,581,580,579,578,
                                577,576,575,574,573,572,571,
                                570,569,568,
                                567,566,565,564,
                                563,562,561,560,559,558,557,556,555,
                                554,553,552,551,550,549,
                                548,547,546]
                        func(url_list,loc_id)
                        
                    #Mizoram
                    elif(state_id=="http://nwp.imd.gov.in/blf/blf_temp/dis.php?value=25mizoram"):
                        el=driver.find_element_by_name('dis')
                        for option in el.find_elements_by_tag_name('option'):
                            if (option.text=='AIZAWL'):
                                option.click()
                                el.submit()
                                break                  
                        driver.get("http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=25AIZAWL")
                        el2=driver.find_element_by_name('block')
                        for option in el2.find_elements_by_tag_name('option'):
                            if (option.text=='AIBAWK'):
                                option.click()
                                el2.submit()
                                break
                        url_list=['http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=SERCHHIP',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=EAST-LUNGDAR',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=25SERCHHIP',#SERCHHIP
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=TUIPANG',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=SAIHA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=25SAIHA',#SAIHA
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=ZAWLNUAM',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=WEST-PHAILENG',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=REIEK',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=25MAMIT',#MAMIT
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=LUNGSEN',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=LUNGLEI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=HNAHTHIAL',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=BUNGHMUN',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=25LUNGLEI',#LUNGLEI
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=SANGAU',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=LAWNGTLAI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=CHAWNGTE',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=BUNGTLANG-SOUTH',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=25LAWNGTLAI',#LAWNGTLAI
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=THINGDAWL',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=BILKHAWTHLIR',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=25KOLASIB',#KOLASIB
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=NGOPA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=KHAWZAWL',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=KHAWBUNG',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=CHAMPHAI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=25CHAMPHAI',#Champhai
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=TLANGNUAM',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=THINGSULTHLIAH',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=PHULLEN',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=DARLAWN',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=AIBAWK',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=25AIZAWL']#Mizoram--AIZAWL
                        loc_id=[405,404,403,
                                402,401,400,
                                399,398,397,396
                                ,395,394,393,392,391,
                                390,389,388,387,386,
                                385,384,383,
                                382,381,380,379,378,
                                377,376,375,374,373,372]
                        func(url_list,loc_id)
                        
                    #Nagaland
                    elif(state_id=="http://nwp.imd.gov.in/blf/blf_temp/dis.php?value=26nagaland"):
                        el=driver.find_element_by_name('dis')
                        for option in el.find_elements_by_tag_name('option'):
                            if (option.text=='DIMAPUR'):
                                option.click()
                                el.submit()
                                break                  
                        driver.get("http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=26DIMAPUR")
                        el2=driver.find_element_by_name('block')
                        for option in el2.find_elements_by_tag_name('option'):
                            if (option.text=='DHANSIRIPAR'):
                                option.click()
                                el2.submit()
                                break
                        url_list=['http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=ZUNHEBOTO',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=TOKIYE',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=SURUHOTO',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=SATAKHA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=GHATHASHI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=AKULUTO',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=26ZUNHEBOTO',#ZUNHEBOTO
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=WOZHURO-RALAN',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=WOKHO',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=SANIS',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=CHUKITONG',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=BHANDARI',#Wokho
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=SHAMATOR',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=THONOKNYU',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=SANGSANGYU',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=NOKSEN',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=NOKLAK',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=LONGKHIM',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=CHESSORE',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=CHARE',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=26TUENSANG',#TUENSANG
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=SEKRUZU',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=PHEK',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=PFUTSERO',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=MELURI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=KIKRUMA',#Phek                                      
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=PEREN',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=TENING',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=JALUKIE',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=26PEREN',#PEREN
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=WAKCHING',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=TOBU',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=TIZIT',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=PHOMCHING',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=MON',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=CHEN',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=26MON',#Mon
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=ONGPANGKONG%28SOUTH%29',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=ONGPANGKONG%28NORTH%29',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=MANGKOLEMBA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=LONGCHEM',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=KUBOLONG',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=CHANGTONGYA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=26MOKOKCHUNG',#MOKOKCHUNG
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=TAMLU',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=LONGLENG',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=26LONGLENG',#Longleng
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=TSEMINYU',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=CHIEPHOBOZOU',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=KOHIMA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=JAKHAMA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=26KOHIMA',#KOHIMA
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=SITIMI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=PUNGRO',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=KIPHIRE',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=26KIPHIRE',#KIPHIRE
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=NIULAND',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=MEDZIPHEMA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=KUHUBOTO',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=DHANSIRIPAR',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=26DIMAPUR']#Nagaland--DIMAPUR
                        loc_id=[371,370,369,368,367,366,365,
                                364,363,362,361,360,
                                358,357,356,355,354,353,352,351,350,
                                349,348,347,346,345,
                                344,343,342,341,
                                340,339,338,337,336,335,334,
                                333,332,331,330,329,328,327,
                                326,325,324,
                                323,322,321,320,319,
                                318,317,316,315,
                                314,313,312,311,310]
                        func(url_list,loc_id)
                    
                    #Sikkim
                    elif (state_id=="http://nwp.imd.gov.in/blf/blf_temp/dis.php?value=31sikkim"):
                        el=driver.find_element_by_name('dis')                
                        for option in el.find_elements_by_tag_name('option'):
                            if (option.text=='EAST-DISTRICT'):
                                option.click()
                                el.submit()
                                break              
                        driver.get("http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=31EAST-DISTRICT")
                        el2=driver.find_element_by_name('block')
                        for option in el2.find_elements_by_tag_name('option'):
                            if (option.text=='DUGA'):
                                option.click()
                                el2.submit()
                                break            
                        url_list=['http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=YUKSOM',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=SORENG',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=KALUK',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=GYALSHING',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=DENTAM',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=DARAMDIN',#West District
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=YANGANG',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=TEMI-TARKU',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=SUMBUK',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=RAVONG',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=NAMTHANG',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=NAMCHI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=JORETHANG',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=31SOUTH-DISTRICT',#SOUTH-DISTRICT
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=MANGAN',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=KABI-TINGDA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=DZONGU',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=CHUNGTHANG',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=31NORTH-DISTRICT',#NORTH-DISTRICT
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=RHENOCK',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=RANKA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=RAKDONG-TINTEK',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=PAKYONG',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=MARTAM',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=KHAMDONG',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=GANGTOK',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=DUGA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=31EAST-DISTRICT']#Sikkim---EAST-DISTRICT
                        loc_id=[492,491,490,489,488,487,
                                485,484,483,482,481,480,479,478,
                                477,476,475,474,473,
                                472,471,470,469,468,467,466,465,464]
                        func(url_list,loc_id)

                    #Tripura
                    elif(state_id=="http://nwp.imd.gov.in/blf/blf_temp/dis.php?value=34tripura"):
                        el=driver.find_element_by_name('dis')
                        for option in el.find_elements_by_tag_name('option'):
                            if (option.text=='DHALAI'):
                                option.click()
                                el.submit()
                                break                  
                        driver.get("http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=34DHALAI")
                        el2=driver.find_element_by_name('block')
                        for option in el2.find_elements_by_tag_name('option'):
                            if (option.text=='AMBASSA'):
                                option.click()
                                el2.submit()
                                break
                        url_list=['http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=MOHANPUR',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=MANDWAI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=LEFUNGA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=JIRANIA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=HEJAMARA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=DUKLI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=34WESTTRIPURA',#WESTTRIPURA
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=PECHARTHAL',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=KUMARGHAT',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=GOURNAGAR',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=34UNAKOTI',#Unakoti
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=SILACHARI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=SATCHAND',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=RUPAICHARI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=RAJNAGAR',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=JOLAIBARI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=HARISHYAMUKH',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=BAGAFA',#South Tripura
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=MELAGHAR',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=KATHALIA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=JAMPUIJALA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=BOXANAGAR',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=BISHALGARH',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=34SEPAHIJALA',#SEPAHIJALA
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=PANISAGAR',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=KADAMTALA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=JUBARAJNAGAR',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=JAMPUIHILLS',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=DASDA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=DAMCHERRA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=34NORTH-TRIPURA',#NORTH-TRIPURA
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=TULASHIKHAR',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=TELIAMURA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=PADMABIL',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=MUNGIAKAMI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=KHOWAI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=KALYANPUR',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=34KHOWAI',#KHOWAI
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=AMPI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=MATABARI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=KILLA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=KARBUK',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=KAKRABAN',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=AMARPUR',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=34GOMATI',#GOMATI
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=SALEMA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=MANU',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=DURGACHOWMUHANI',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=DUMBURNAGAR',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=CHHAMANU',
                                  'http://nwp.imd.gov.in/blf/blf_temp/table2.php?block=AMBASSA',
                                  'http://nwp.imd.gov.in/blf/blf_temp/block.php?dis=34DHALAI']#Tripura---DHALAI        
                        loc_id=[545,544,543,542,541,540,539,
                                538,537,536,535,
                                534,533,532,531,530,529,528,
                                526,525,524,523,522,521,
                                520,519,518,517,516,515,514,
                                513,512,511,510,509,508,507,
                                506,505,504,503,502,501,500,
                                499,498,497,496,495,494,493]
                        func(url_list,loc_id)

        finally:
            con1.close()

        driver.quit()
        time.sleep(86400)
        
if __name__ == '__main__':
    p1=Thread(target = earthquake)
    p2=Thread(target = executeSomething)
    p1.start()
    p2.start()
    p1.join()
    p2.join()


    
    
        
