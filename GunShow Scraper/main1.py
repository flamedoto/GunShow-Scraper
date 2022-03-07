#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from tqdm import tqdm
import sys
import random
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import *
from selenium.webdriver.support.ui import *
import re
import os
from datetime import datetime
from bs4 import BeautifulSoup as bs4
import dateparser
import urllib.request
import requests
import math
from selenium.webdriver.common.action_chains import ActionChains

import mysql.connector

mydb = mysql.connector.connect(
  host="206.189.200.14",
  user="c1_mags_bf",
  password="sncwLU!7V",
  database="c1_mags_battlefield"
)

#mydb = mysql.connector.connect(
#  host="db4free.net",
#  user="gunshowdb",
#  password="31175209",
# database="gunshow"
#)
mycursor = mydb.cursor(buffered=True)



## Defining options for chrome browser
options = webdriver.ChromeOptions()
options.add_argument("--ignore-certificate-errors")
Browser = webdriver.Chrome(executable_path = "chromedriver",options = options)
States = []
ShowUrls = []
#Name of all US states
USstates = ['alabama','alaska','arizona','arkansas','nebraska','california','colorado','connecticut','delaware','florida','georgia','hawaii','idaho','illinois','indiana','iowa','kansas','kentucky','louisiana','districtofcolumbia','maine','maryland','massachusetts','michigan','minnesota','mississippi','missouri','montana','nevada','newhampshire','newjersey','newmexico','newyork','northcarolina','northdakota','ohio','oklahoma','oregon','pennsylvania','rhodeisland','southcarolina','southdakota','tennessee','texas','utah','vermont','virginia','washington','westvirginia','wisconsin','wyoming']
Main_Url = 'https://gunshowtrader.com/sitemap/'

#Regex to find website URL
URLregex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?������]))"


def checkforimagefolder():
	if os.path.isdir("Images") == False:
		os.mkdir("Images")
    

#This function will check that the date exists or not return True if exists else False
def checkexists(gunshowid,promoterid,startDate,endDate,cancelDate):
	boolvar = False
	#converting cancelDate to 0 or 1 to prevent SQL syntax error
	cd = "0"
	if cancelDate == True:
		cd = "1"
	else:
		cd = "0"
	#if enddate is null 
	if endDate == '':
		mycursor.execute("SELECT * from dates WHERE `gun_show_id` = '"+str(gunshowid)+"' AND `promoter_id` = '"+str(promoterid)+"' AND `start_date` = '"+str(startDate)+"' AND `cancelled` = '"+str(cd)+"'")

	else:
		mycursor.execute("SELECT * from dates WHERE `gun_show_id` = '"+str(gunshowid)+"' AND `promoter_id` = '"+str(promoterid)+"' AND `start_date` = '"+str(startDate)+"' AND `end_date` = '"+str(endDate)+"' AND `cancelled` = '"+str(cd)+"'")
	msg = mycursor.fetchone()  
	#check if msg has something 
	if not msg:
		boolvar = False
	else:
		boolvar = True
	return boolvar


#Inserting data to gun show table
def gunshowinsert(promoter_id,name,city,state,hours,admission,description,venue,venue_address,venue_city,vendor_info,venue_zip,venue_state,url):
	Query = ("INSERT INTO gun_shows (promoter_id,name,city,state,hours,admission,description,venue,venue_address,venue_city,vendor_info,venue_zip,venue_state,url) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
	#values = (name,city,state,hours,admission,description,venue,venue_address,venue_city,vendor_info,venue_zip,venue_state,url)
	mycursor.execute(Query,(promoter_id,name,city,state,hours,admission,description,venue,venue_address,venue_city,vendor_info,venue_zip,venue_state,url))	
	mydb.commit()
	return mycursor.lastrowid




#Inserting date to Promoters table
def promotersinsert(logo,name,contact,phone,email,website):
	Query = ("INSERT INTO promoters (logo,name,contact,phone,email,website) VALUES (%s,%s,%s,%s,%s,%s)")
	values = (logo,name,contact,phone,email,website)
	mycursor.execute(Query, values)	
	mydb.commit()
	return mycursor.lastrowid




#Inserting data to Dates table
def datesinsert(gun_show_id,promoter_id,start_date,end_date,cancelled):
	#if end date is null
	if end_date == '':
		Query = ("INSERT INTO dates (gun_show_id,promoter_id,start_date,cancelled) VALUES (%s,%s,%s,%s)")
		#values = (gun_show_id,promoter_id,start_date,end_date,cancelled)
		try:
			mycursor.execute(Query,(gun_show_id,promoter_id,start_date,cancelled))	
			mydb.commit()
			return mycursor.lastrowid
		except Exception as e:
			print(str(e))
	#if end date is not null
	else:
		Query = ("INSERT INTO dates (gun_show_id,promoter_id,start_date,end_date,cancelled) VALUES (%s,%s,%s,%s,%s)")
		#values = (gun_show_id,promoter_id,start_date,end_date,cancelled)
		try:
			mycursor.execute(Query,(gun_show_id,promoter_id,start_date,end_date,cancelled))	
			mydb.commit()
			return mycursor.lastrowid
		except Exception as e:
			print(str(e))




def UrlsofShow():
	Browser.get(Main_Url)
	time.sleep(5)
	indexes = []
	#Finding every h3 and ul after Gunshow Heading
	statesh3s = Browser.find_elements_by_xpath('//h2[@id="gunshows"]/following::h3')
	showslist = Browser.find_elements_by_xpath('//h2[@id="gunshows"]/following::ul')
	#if state on h3 is in the US state array then append it to another array and store its index to seperate array
	for idx,state in enumerate(statesh3s):
		if state.text.lower().replace(' ','') in USstates:
			States.append(state.text)
			indexes.append(idx)

	#state h3 and ul has the same index its getting from all the us state that we filter UP  //ul //li //a href
	for idx in indexes:
		uls = showslist[idx].get_attribute('innerHTML')
		ulbs4 = bs4(uls,"html.parser")
		lis = ulbs4.findAll("li")
		for li in lis:
			adata = li.find("a")
			if adata['href'] not in ShowUrls:
				ShowUrls.append(adata['href'])
	print("Found "+str(len(ShowUrls))+" Gunshow URLs")


#splitting dates into 2
def SplitingDates(date):
	startDate = ""
	endDate=""
	#if date is like nov 13th, 2019
	if '–' not in date:
		DateVar = date.split(',')
		Year = DateVar[-1].lstrip()
		DateVar1 = DateVar[0].split('–')

		if len(DateVar1) == 1:
			startDate = dateparser.parse(date)
			endDate = ""
	else:
		#if date is like nov 13 2019 - nov 14 2019
		checkdate = date.split('–')
		checkdate = checkdate[0].split(',')
		if len(checkdate) > 1:
			date1 = date.split('–')
			startDate = dateparser.parse(date1[0])
			endDate = dateparser.parse(date1[-1])
		else:
			#if date is like nov13 - 14,2019 or nov13-dec 1, 2019
			DateVar = date.split(',')
			Year = DateVar[-1].lstrip()
			DateVar1 = DateVar[0].split('–')
			
			FirstDateMain = DateVar1[0].rstrip().split(' ')

			FirstDateDay = FirstDateMain[-1]

			FirstDateMonth = FirstDateMain[0].lower()


			SecondDateMain = DateVar1[-1].lstrip().split(' ')

			if len(SecondDateMain) == 1:
				SecondDateMonth = FirstDateMonth
			else:
				SecondDateMonth = SecondDateMain[-0].lower()
			SecondDateDay = SecondDateMain[-1]

			startDate = FirstDateMonth +" "+ FirstDateDay +" "+ Year
			endDate = SecondDateMonth +" "+ SecondDateDay +" "+ Year


			startDate = dateparser.parse(startDate)
			endDate = dateparser.parse(endDate)

	return startDate,endDate

def connector():
	checkforimagefolder()
	UrlsofShow()
	print("scraping show data")
	for url in ShowUrls:
		ShowDataScrape(url)


def ShowDataScrape(url):
	#url = "https://gunshowtrader.com/gun-shows/columbus-sporting-arms-blade-show/"
	#url = 'https://gunshowtrader.com/gun-shows/fort-oglethorpe-gun-show/'
	#url = 'https://gunshowtrader.com/gun-shows/hoover-gun-show/'
	#url = 'https://gunshowtrader.com/gun-shows/montgomery-militaria-show/'
	Browser.get(url)
	time.sleep(3)

	try:
		ShowTitle = Browser.find_element_by_xpath("//h1[@class='entry-title']").text
	except:
		ShowTitle = ""

	try:
		csfind = Browser.find_element_by_xpath("//div[@class='three-fourths text city/state']")

		csfind = csfind.text.split(',')

		ShowCity = csfind[0].replace(' ','')
		ShowState = csfind[1].replace(' ','')
	except:
		ShowCity = ""
		ShowState = ""



	try:
		ShowHours = Browser.find_element_by_xpath("//div[@class='three-fourths text hours']").text
	except:
		ShowHours = ""

	try:
		ShowAdmission = Browser.find_element_by_xpath('//div[@class="three-fourths text admission"]').text
	except:
		ShowAdmission = ""


	try:
		ShowDescription = Browser.find_element_by_xpath('//div[@class="three-fourths text"]//p').text
	except:
		ShowDescription = ""

	try:
		PromoterName = Browser.find_element_by_xpath("//span[@class='organization-name']").text
		PromoterName = PromoterName.replace("'","")
	except:
		PromoterName = ""



	#Retrieveing promoter logo image from webpage
	try:
		PIN = "Images/"+PromoterName+'.jpg'
		PromoterImage = Browser.find_element_by_xpath("//img[@alt='"+PromoterName+"']").get_attribute('src')
		r = requests.get(PromoterImage)
		with open(PIN, 'wb') as outfile:
			outfile.write(r.content)
		
	except Exception as e: 
		PIN = 'NA'
	PromoterContact=""
	PromoterPhone = ''
	PromoterEmail = ''
	PromoterWebsite = ''

	try:
		Promoterlis = Browser.find_elements_by_xpath("//ul[@class='organization-contact']//li")

		for li in Promoterlis:
			if "Contact" in li.text:
				PromoterContact  = li.text.split(':')[-1]
			elif "Phone" in li.text:
				PromoterPhone = li.text.split(':')[-1]
			elif "Email" in li.text:
				PromoterEmail = li.text.split(':')[-1]
			else:
				try:
					PromoterWebsite = re.findall(URLregex,li.text.strip())[0][0]
				except:
					pass
	except:
		pass



	try:
		VendorInfo = Browser.find_element_by_xpath("//div[@class='three-fourths text vendor']").text
	except:
		VendorInfo = ""

	try:
		venuename = Browser.find_element_by_xpath("//div[@class='three-fourths text location']//div[@class='location']//a").text
	except:
		venuename = ""

	try:	
		venueaddress = Browser.find_element_by_xpath("//div[@class='three-fourths text location']//div[@class='location']//address[@class='address']").text.split('\n')


		venueaddress1 = venueaddress[-1].split(',')


		venuestate = (venueaddress1[-1].lstrip().split(' '))[0].replace(' ','')


		venuezip = (venueaddress1[-1].lstrip().split(' '))[-1]


		venuecity = (venueaddress1[0])


		venueaddress = venueaddress[0]
	except:
		venueaddress = ""
		venuestate = ""
		venuecity = ""
		venuezip = ""
	gunshowid = ""
	alreadyexists = False
	promoterid = ""



	#Insert data into promoter if promoter name already exists set alreadexists true
	try:
		promoterid = promotersinsert(PIN,str(PromoterName),str(PromoterContact),str(PromoterPhone),str(PromoterEmail),str(PromoterWebsite))
	except mysql.connector.IntegrityError as error:
		#print(error)
		alreadyexists = True


	#if promoter name already exists
	if alreadyexists == True:
		#find promoter id by its name
		mycursor.execute("SELECT `id` FROM `promoters` WHERE `name` ='"+str(PromoterName)+"' ")
		promoter = mycursor.fetchall()
		for id1 in promoter:
			promoterid = id1[0]
			#print("Promoter ID : "+str(id1[0]))

		#if gunshow name already exists
		try:
			gunshowid = gunshowinsert(promoterid,ShowTitle,ShowCity,ShowState,ShowHours,ShowAdmission,ShowDescription,venuename,venueaddress,venuecity,VendorInfo,venuezip,venuestate,url)
		except mysql.connector.IntegrityError as error:
			#then find its ID by gun show name
			mycursor.execute("SELECT `id` FROM `gun_shows` WHERE `name` ='"+str(ShowTitle)+"' ")
			gunshow1 = mycursor.fetchall()
			for id1 in gunshow1:
				gunshowid = id1[0]
	else:
		#if promoter name exists
		try:
			gunshowid = gunshowinsert(promoterid,ShowTitle,ShowCity,ShowState,ShowHours,ShowAdmission,ShowDescription,venuename,venueaddress,venuecity,VendorInfo,venuezip,venuestate,url)
		except mysql.connector.IntegrityError as error:
			#gunshow name already in the table then find its ID by gun show name
			mycursor.execute("SELECT `id` FROM `gun_shows` WHERE `name` ='"+str(ShowTitle)+"'")
			gunshow1 = mycursor.fetchall()
			for id1 in gunshow1:
				gunshowid = id1[0]
	#print(PromoterWebsite)

	try:
		date = True
		Dates = Browser.find_elements_by_xpath("//div[@class='date-display']")

		cancelDate = False
		for idx,date in enumerate(Dates):
			canceldatega = date.get_attribute('innerHTML')
			#if strike tag in the date then Cancel date is true
			if '<strike>' in canceldatega:
				cancelDate = True
			else:
				cancelDate = False
			#split date into date start date and end date
			startDate,endDate = SplitingDates(date.text)
			#check if data exists in database
			ce = checkexists(gunshowid,promoterid,startDate,endDate,cancelDate)
			#print(ce)
			#if does skip it if not add it
			if ce == True:
				continue
			else:
				dateid = datesinsert(gunshowid,promoterid,startDate,endDate,cancelDate)
	except Exception as e:
		print(str(e))
		date = False



connector()
#ShowDataScrape()
#UrlsofShow()
