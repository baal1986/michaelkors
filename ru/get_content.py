#/usr/bin/python3

import requests
import os
from bs4 import BeautifulSoup
import re
import time
import ast

from selenium import webdriver
from selenium.webdriver.firefox.options import Options 
from selenium.webdriver.common.proxy import Proxy, ProxyType
import psycopg2
from psycopg2 import sql



'''
create table if not exists michaelkors (
    aid      serial  primary key ,
    articul  text    not null unique      ,
    

    fr_price text    not null default '0' ,
    fr_link  text    not null default '0' ,
    fr_title text    not null default '0' ,
    

    de_price text    not null default '0' ,
    de_link  text    not null default '0' ,
    de_title text    not null default '0' ,

    it_price text    not null default '0' ,
    it_link  text    not null default '0' ,
    it_title text    not null default '0' ,

    uk_price text    not null default '0' ,
    uk_link  text    not null default '0' ,
    uk_title text    not null default '0' ,
    

    us_price text    not null default '0' ,
    us_link  text    not null default '0' ,
    us_title text    not null default '0' ,
    

    ca_price text    not null default '0' ,
    ca_link  text    not null default '0' ,
    ca_title text    not null default '0' ,
    

    ru_price text    not null default '0' ,
    ru_link  text    not null default '0' ,
    ru_title text    not null default '0' ,
    
    fcomment text
) ;

create sequence michaelkors_sequence
  start 1
  increment 1;


'''

def SearchUnit( country, articul ) :
    #TODO :Сделать парсер ссылки поиска
    if(country == "fr") :
        url = "https://www.michaelkors.fr/search/_/N-0/Ntt-"+ articul
    if(country == "de") :
        url = "https://www.michaelkors.de/search/_/N-0/Ntt-"+ articul
    if(country == "it") :
        url = "https://www.michaelkors.it/search/_/N-0/Ntt-"+ articul
    if(country == "uk") :
        pass
    if(country == "us") :
        pass
    if(country == "ca") :
        url = "https://www.michaelkors.ca/search/_/Rtt-"+ articul
    if(country == "ru") :
        url = "https://www.michaelkors.global/en_RU/search/_/N-0/Ntt-"+ articul
    
    
    firefox_options = Options()
    firefox_options.add_argument('--headless')
    d = webdriver.Firefox(firefox_options=firefox_options)
    d.get(url)
    data=d.page_source
    d.close()

    soup = BeautifulSoup(data, features="lxml")
    link_list = soup.findAll('li', {'class': ['product-price-container']})
    for i in link_list :
        st = i
        st = str(st)
        
        #<span class="ada-link visually-hidden">RUB13,400.00</span></span></div></a></li>
        price_list = re.sub(r',','', st)
        price_list = re.findall('<span class="ada-link visually-hidden">RUB[0-9]*\.00', price_list)
        price_list = str(price_list)
        
        price = re.sub(r'<span class="ada-link visually-hidden">', '', price_list)
        price = re.sub( r'\.00', '', price)
        #$, £, €
        price = re.sub( r'($)|(£)|(€)|(RUB)', '', price)
        price = re.sub( r"'.*', ", "", price)
        ref   = i.find('a').get('href')
        title = i.find('a').get('title') 
        ref = str(ref)
        #/_/R-30F7GCYS2L
        articul = re.sub('.*\/_\/R-','' , ref)
        
        with open('search_ru.txt', 'a+') as output_file:
            print(articul, file=output_file)
            print(ref, file=output_file)
            print(title, file=output_file)
            print(price[2:-2], file=output_file)
            print("\n\n", file=output_file)
            
def ParsRU() :
    country = "ru" ;
        
    if(country == "fr") :
        url = "https://www.michaelkors.fr"
    if(country == "de") :
        url = "https://www.michaelkors.de"
    if(country == "it") :
        url = "https://www.michaelkors.it"
    if(country == "uk") :
        url = "https://www.michaelkors.co.uk"
    if(country == "us") :
        url = "https://www.michaelkors.com"
    if(country == "ca") :
        url = "https://www.michaelkors.ca"
    if(country == "ru") :
        url = "https://www.michaelkors.global/en_RU"


    # Get sale link RU####################################################################################
    firefox_options = Options()
    firefox_options.add_argument('--headless')
    d = webdriver.Firefox(firefox_options=firefox_options)
    d.get(url)
    data=d.page_source
    d.close()
    soup = BeautifulSoup(data, features="lxml")
    #<a class="menu-link main l1flyout css-p5yj9y e19yl8jt0" title="Sale" aria-label="Sale main.nav.keyboardGuide" href="/en_RU/sale/view-all-sale/_/N-voun1s" aria-hidden="false">sale</a>
    link_list = soup.findAll('a', {'class': ['menu-link main l1flyout css-p5yj9y e19yl8jt0']})
    pages = str(link_list)
    page = re.findall(r'/sale/view-all-sale/_/.*">sale</a>', pages)
    page = str(page)
    page_ = re.sub( r'" title="Sale">sale</a>', '', page)
    # Get sale link RU####################################################################################


    # Get units RU########################################################################################
    firefox_options = Options()
    firefox_options.add_argument('--headless')
    d = webdriver.Firefox(firefox_options=firefox_options)
    d.get(url + str(page_[2:-2]) )
    #d.get('https://www.michaelkors.global/en_RU/sale/view-all-sale/_/N-voun1s')
    data=d.page_source
    soup = BeautifulSoup(data, features="lxml")

    #<ul class="nav-category-list">
    link_list = soup.findAll('ul', {'class': ['nav-category-list']})
    j = 0
    link_ref=[]
    for i in link_list :
        link_ref.insert( j, (i.find('a').get('href')) )
        j = j + 1
        
    url = "https://www.michaelkors.global"    
    j = 1

    while( len(link_ref) > j ) :
        d.get( url + str(link_ref[j]) )
        data=d.page_source
        d.close()
        soup = BeautifulSoup(data, features="lxml")
        #<li class="product-price-container">
        link_list = soup.findAll('li', {'class': ['product-price-container']})
        for i in link_list :
            
            st = i
            st = str(st)
            
            #<span class="ada-link visually-hidden">RUB13,400.00</span></span></div></a></li>
            price_list = re.sub(r',','', st)
            price_list = re.findall('<span class="ada-link visually-hidden">RUB[0-9]*\.00', price_list)
            price_list = str(price_list)
            
            price = re.sub(r'<span class="ada-link visually-hidden">', '', price_list)
            price = re.sub( r'\.00', '', price)
            #$, £, €
            price = re.sub( r'($)|(£)|(€)|(RUB)', '', price)
            price = re.sub( r"'.*', ", "", price)
            ref   = i.find('a').get('href')
            title = i.find('a').get('title') 
            ref = str(ref)
            #/_/R-30F7GCYS2L
            articul = re.sub('.*\/_\/R-','' , ref)
            conn = BDConnect()
            cur = conn.cursor()
            try:
                sql = "insert into michaelkors (aid, articul, ru_price, ru_link, ru_title ) values(nextval('michaelkors_sequence'), %s, %s, %s, %s);"
                data = ( str(articul), str(price[2:-2]), str(ref), str(title) )
                cur.execute( sql, data )
                conn.commit()
                print("\n")
                print('[+] Query complite!')
                print("\n\n")
            except psycopg2.DatabaseError as e:
                print("\n")
                print('[+] Query error!')
                print("\n\n")
                print(f'Error {e}')
                
            finally:
                if conn:
                    conn.close()
            conn.close()
            '''
            with open('articul_ru.txt', 'a+') as output_file:
                print(articul, file=output_file)
                print(ref, file=output_file)
                print(title, file=output_file)
                print(price[2:-2], file=output_file)
                print("\n\n", file=output_file)
            '''
        j = j + 1
            
    
    
    # Get units RU########################################################################################





def BDConnect() :
    try:
        conn = psycopg2.connect( "dbname=michaelkors user=postgres host=localhost password=1" )
        print("DB connected!")
        return conn
    except:
        print("DB connected!")
        return 0
    
def QueryFetchall( conn, query ) :
    cur = conn.cursor()
    try:
        cur.execute(query)
        rows = cur.fetchall()
        return rows
        
    except psycopg2.DatabaseError as e:
        print(f'Error {e}')
        
    finally:
        if conn:
            conn.close()

def QueryInsertInto( conn, query ) :
    cur = conn.cursor()
    try:
        cur.execute(query)
        conn.commit()
        print(query)
        print("\n\n")
        print('[+] Query complite!')
        print("\n\n")
    except psycopg2.DatabaseError as e:
        print("\n\n")
        print('[+] Query error!')
        print("\n\n")
        print(f'Error {e}')
        
    finally:
        if conn:
            conn.close()

def QueryUpdate( conn, query ) :
    cur = conn.cursor()
    try:
        cur.execute(query)
        conn.commit()
        print(query)
        print("\n\n")
        print('[+] Query complite!')
        print("\n\n")
    except psycopg2.DatabaseError as e:
        print("\n\n")
        print('[+] Query error!')
        print("\n\n")
        print(f'Error {e}')
        
    finally:
        if conn:
            conn.close()

def QuerySelectReturnId( conn, query ) :
    cur = conn.cursor()
    try:
        cur.execute(query)
        rows = cur.fetchall()
        r = str(rows[0])
        return(r[1:-2])
        
    except psycopg2.DatabaseError as e:
        print(f'Error {e}')
        
    finally:
        if conn:
            conn.close()




'''# INSERT#################################################################################################################
query ="""insert into michaelkors (aid, articul, ru_price, ru_link, ru_title )
                VALUES (nextval('michaelkors_sequence'),
                        '40T9AUME5L',
                        '7800', 
                        'https://www.michaelkors.global/en_RU/augustine-woven-ankle-boot/_/R-40T9AUME5L',
                        'Augustine Woven Ankle Boot'
);"""
QueryInsertInto( conn, query )
# INSERT#################################################################################################################
'''

'''# SELECT#################################################################################################################
query = """select * from michaelkors;"""
rows = QueryFetchall( conn, query )
for row in rows:
    print(f"{row[0]} {row[1]} {row[2]}")


query = """select aid from michaelkors where articul='30T5GTVT2L';"""
rows = QuerySelectReturnId( conn, query )
print(rows)
# SELECT#################################################################################################################
'''

'''# UPDATE#################################################################################################################
query = """update michaelkors set ru_price='666' where articul='30T5GTVT2L' ;"""
QueryUpdate( conn, query )
# UPDATE#################################################################################################################
'''

ParsRU()








