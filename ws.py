"""
Created on Sun Jul 12 19:07:38 2020

@author: Saurav
"""


from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import re
from datetime import datetime
from itertools import compress
import time
import os
import pandas as pd




def getCities():
    browser = webdriver.Chrome( executable_path="{}".format( chdriverpath), options=option)
    browser.get(url)
    timeout = 20
    try:
        WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.CLASS_NAME,"toggle")))
    except TimeoutException:
        print("Timed out waiting for page to load")
        browser.quit()
    time.sleep(1)
    browser.find_elements_by_class_name("toggle")[0].click()
    states = [elem.text for elem in browser.find_element_by_tag_name('ul').find_elements_by_tag_name('li')]
    d = {'StateName':[],'CityName':[]}
    data = pd.DataFrame(d)
    browser.find_elements_by_class_name("toggle")[0].click()
    for state in states:
        browser.find_elements_by_class_name("toggle")[0].click()
        browser.find_element_by_tag_name("input").send_keys(state)
        browser.find_element_by_class_name("options").click()
        browser.find_elements_by_class_name("toggle")[1].click()
        city = [elem.text for elem in browser.find_element_by_tag_name('ul').find_elements_by_tag_name('li')]
        for c in city:
            data = data.append({'StateName':state,'CityName':c},ignore_index = True)
        time.sleep(1)
    browser.quit()
    return data

def getStations(ddlState, ddlCity):
    browser = webdriver.Chrome(executable_path="{}".format(chdriverpath), options=option)
    browser.get(url)
    timeout = 40
    try:
        WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.CLASS_NAME,"toggle")))
    except TimeoutException:
        print("Timed out waiting for page to load")
        browser.quit()
    browser.find_elements_by_class_name("toggle")[0].click()
    browser.find_element_by_tag_name("input").send_keys(ddlState)
    browser.find_element_by_class_name("options").click()
    browser.find_elements_by_class_name("toggle")[1].click()
    browser.find_element_by_tag_name("input").send_keys(ddlCity)
    browser.find_element_by_class_name("options").click()
    browser.find_elements_by_class_name("toggle")[2].click()
    content = browser.page_source.encode('utf-8').strip()
    soup = BeautifulSoup(content,"html.parser")
    st = soup.find_all("div",{"class":"options"})
    st = st[0].text.split('\n')
    b = [bool(re.search(r"\w",x)) for x in st]
    st = list(compress(st,b))
    st = [x.strip() for x in st]
    browser.quit()
    return st

def parameters(br,param):
    br.find_element_by_class_name("list-filter").find_element_by_tag_name("input").send_keys(param)
    br.find_elements_by_class_name("pure-checkbox")[1].click()
    br.find_element_by_class_name("list-filter").find_element_by_tag_name("input").clear()

def getData(stateName, cityName, param,startdate,enddate,duration):
    stations = getStations(stateName,cityName)
    sd = datetime.strptime(startdate,"%d-%m-%Y")
    sd = sd.strftime("%d-%b-%Y").split("-")
    ed = datetime.strptime(enddate,"%d-%m-%Y")
    ed = ed.strftime("%d-%b-%Y").split("-")
    soups = []
    
    for station in stations:
        try:
            browser = webdriver.Chrome(executable_path="{}".format(chdriverpath), options=option)
            browser.get(url)
            timeout = 40
            try:
                WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.CLASS_NAME,"toggle")))
            except TimeoutException:
                print("Timed out waiting for page to load")
                browser.quit()
            browser.find_elements_by_class_name("toggle")[0].click()
            browser.find_element_by_tag_name("input").send_keys(stateName)
            browser.find_element_by_class_name("options").click()
            browser.find_elements_by_class_name("toggle")[1].click()
            browser.find_element_by_tag_name("input").send_keys(cityName)
            browser.find_element_by_class_name("options").click()
            browser.find_elements_by_class_name("toggle")[2].click()
            browser.find_element_by_tag_name("input").send_keys(station)
            browser.find_element_by_class_name("options").click()
            browser.find_elements_by_class_name("toggle")[4].click()
            browser.find_element_by_class_name("filter").find_element_by_tag_name("input").send_keys(duration)
            browser.find_element_by_class_name("options").click()
            browser.find_element_by_class_name("c-btn").click()
            for p in param:
                try:
                    parameters(browser,p)
                except:
                    browser.find_element_by_class_name("list-filter").find_element_by_tag_name("input").clear()
                    pass
            browser.find_element_by_class_name("wc-date-container").click()
            browser.find_element_by_class_name("month-year").click()
            browser.find_element_by_id("{}".format(sd[1].upper())).click()
            browser.find_element_by_class_name("year-dropdown").click()
            browser.find_element_by_id("{}".format(int(sd[2]))).click()
            browser.find_element_by_xpath('//span[text()="{}"]'.format(int(sd[0]))).click()
            #browser.find_element_by_class_name("ok").click()
            browser.find_elements_by_class_name("wc-date-container")[1].click()
            browser.find_elements_by_class_name("month-year")[1].click()
            browser.find_elements_by_id("{}".format(ed[1].upper()))[1].click()
            browser.find_elements_by_class_name("year-dropdown")[1].click()
            browser.find_element_by_id("{}".format(int(ed[2]))).click()
            browser.find_elements_by_xpath('//span[text()="{}"]'.format(int(ed[0])))[1].click()
            #browser.find_elements_by_class_name("ok")[1].click()
            browser.find_elements_by_tag_name("button")[-1].click()
            try:
                WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.ID,"DataTables_Table_0_wrapper")))
            except TimeoutException:
                print("Timed out waiting for page to load")
                break
            browser.find_element_by_tag_name("select").send_keys("100")
            time.sleep(5)
            maxpage = int(browser.find_elements(By.XPATH,"//*[@id='DataTables_Table_0_paginate']/span/a")[-1].text)
            
            i = 1
            while i < maxpage + 1:
                print(i)
                browser.find_element(By.XPATH,"//*[@id='DataTables_Table_0_paginate']/span/a[contains(text(),'{}')]".format(i)).click()
                time.sleep(8)
                res = browser.page_source
                soup = BeautifulSoup(res, 'html.parser')
                soup = soup.find(id = 'DataTables_Table_0')
                if i == 1:
                    data = getValsHtml(soup)
                else:
                    data = data.append(getValsHtml(soup))
                i = i + 1
                browser.find_element(By.XPATH,"//*[@id='DataTables_Table_0_paginate']/span/a[contains(text(),'{}')]".format(i)).click()
                time.sleep(30)
                
            soups.append([(stateName, cityName, station), data])
            browser.quit()
            print("Finished Crawling for {}, {}, {}".format(stateName, cityName, station))
        except:
            print("Exception raised for {}, {}, {}".format(stateName, cityName, station))
            time.sleep(5)
    return soups
    

def getValsHtml(table):
    data = []
    heads = table.find_all('th')
    data.append([ele.text.strip() for ele in heads])
    rows = table.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols]) # Get rid of empty values
    data.pop()
    data = pd.DataFrame(data[1:],columns = data[0])
    return data

def main():
    global option,browser,url,param,startdate,enddate,duration,directory,chdriverpath
    param = ['PM2.5','Ozone','SO2','PM10','NO2','CO']
    chdriverpath = 'bin/chromedriver'
    directory = '/home/prnv/MLP/Data'
    startdate = '01-03-2019'
    enddate = '01-04-2019'
    duration = ' '.join('24 Hour')
    cdir='/'
    """You can create an instance of ChromeOptions , which has convenient methods for setting ChromeDriver-specific 
    capabilities. You can then pass the ChromeOptions object into the ChromeDriver constructor: 
    ChromeOptions options = new ChromeOptions options."""
    option = webdriver.ChromeOptions()
    os.chdir(cdir)
    prefs = {'download.default_directory' : '{}'.format(cdir)}

    option.add_experimental_option('prefs', prefs)
    url = 'https://app.cpcbccr.com/ccr/#/caaqm-dashboard-all/caaqm-landing/data'
    cities = getCities()
    if not os.path.exists(directory):
        os.makedirs(directory)
    for elem in range(cities.shape[0]):
        stateName, cityName = cities["StateName"][elem],cities["CityName"][elem]
    	try:
        	soups = getData(stateName, cityName, param,startdate,enddate,duration)
        	print(soups)
        	for s in soups:
        	    state, city, station = s[0]
        	    s[1].to_csv("{}/{}_{}_{}.csv".format(directory,state, city, station),index = False)
        	print("---")
        	print("Finished Crawling city {}, {}".format(stateName, cityName))
        	time.sleep(1)
    	except:
        	print("Error occurred at {}, {}".format(stateName, cityName))
        

if __name__ == '__main__':
	main()
