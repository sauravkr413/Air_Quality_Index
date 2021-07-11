import numpy as np # linear algebra
import pandas as pd
import matplotlib.pyplot as plt
import os

#Function to calculate so2 individual pollutant index(si)
def calculate_si(so2):
    si=0
    if (so2<=40):
     si= so2*(50/40)
    if (so2>40 and so2<=80):
     si= 50+(so2-40)*(50/40)
    if (so2>80 and so2<=380):
     si= 100+(so2-80)*(100/300)
    if (so2>380 and so2<=800):
     si= 200+(so2-380)*(100/800)
    if (so2>800 and so2<=1600):
     si= 300+(so2-800)*(100/800)
    if (so2>1600):
     si= 400+(so2-1600)*(100/800)
    return si
    
#Function to calculate no2 individual pollutant index(ni)
def calculate_ni(no2):
    ni=0
    if(no2<=40):
     ni= no2*50/40
    elif(no2>40 and no2<=80):
     ni= 50+(no2-14)*(50/40)
    elif(no2>80 and no2<=180):
     ni= 100+(no2-80)*(100/100)
    elif(no2>180 and no2<=280):
     ni= 200+(no2-180)*(100/100)
    elif(no2>280 and no2<=400):
     ni= 300+(no2-280)*(100/120)
    else:
     ni= 400+(no2-400)*(100/120)
    return ni
    
def calculate_p25i(PM25):
    p25=0
    if(PM25<=12):
        p25i=PM25*50/12.0
    elif(PM25>12.1 and PM25<=35.4):
        p25i=51+(PM25-12.1)*49/23.3
    elif(PM25>35.5 and PM25<=55.4):
        p25i=101+(PM25-35.5)*49/19.9
    elif(PM25>55.5 and PM25<=150.4):
        p25i=151+(PM25-55.5)*49/94.9
    elif(PM25>150.5 and PM25<=250.4):
        p25i=201+(PM25-150.5)*99/99.9
    elif(PM25>250.5 and PM25<=350.4):
        p25i=301+(PM25-250.5)*99/99.9
    else:
        p25i=401+(PM25-250.5)*99/149.9    
    return p25i
    
def calculate_oi(o3):
    oi=0
    if(o3>54):
        oi=o3*50/108
    elif(o3>54 and o3<=70):
        oi=55+(o3/2-55)*49/15    
    elif(o3>70 and o3<=85):
        oi=101+(o3/2-71)*49/14 
    elif(o3>85 and o3<=105):
        oi=151+(o3/2-86)*49/19
    elif(o3>105 and o3<=200):
        oi=201+(o3/2-105)*99/94
    elif(o3>200 and o3<=504):  
        oi=301+(o3/2-201)*99/99
    else:
        oi=401+(o3/2-505)*99/99
    return oi
    
def calculate_p10i(PM10):
    p10i=0
    if(PM10<=54):
        p10i=PM10*50/54
    elif(PM10>54 and PM10<=154):
        p10i=51+(PM10-55)*49/99
    elif(PM10>154 and PM10<=254):
        p10i=101+(PM10-155)*49/99
    elif(PM10>254 and PM10<=354):
        p10i=151+(PM10-255)*49/99
    elif(PM10>354 and PM10<=424):
        p10i=201+(PM10-355)*99/69
    elif(PM10>424 and PM10<=504):
        p10i=301+(PM10-425)*99/79
    else:
        p10i=401+(PM10-505)*99/99
    return p10i
    
    
def calculate_coi(co):
    coi=0
    if(co<=4.4):
        coi=co/1.145*50/4.4
    elif(co>4.4 and co<=9.4):
        coi=51+(co/1.145-4.5)*49/4.9
    elif(co>9.4 and co<=12.4):
        coi=101+(co/1.145-9.5)*49/2.9
    elif(co>12.4 and co<=15.4):
        coi=151+(co/1.145-12.5)*49/2.9
    elif(co>15.4 and co<=30.4):
        coi=201+(co/1.145-15.5)*99/14.9
    elif(co>30.4 and co<=40.4):
        coi=301+(co/1.145-30.5)*99/9.9
    else:
        coi=401+(co/1.145-40.5)*99/9.9
    return coi
   
#function to calculate the air quality index (AQI) of every data value
#its is calculated as per indian govt standards
def calculate_aqi(si,ni,p25i,p10i,oi,coi):
    aqi=max(si,ni,p25i,p10i,oi,coi)    
    return aqi 
    
    
data=pd.read_csv('kol.csv')
print(data)
data['si']=data['SO2 (ug/m3)'].apply(calculate_si)
data['ni']=data['NO2 (ug/m3)'].apply(calculate_ni)
data['p25i']=data['PM2.5 (ug/m3)'].apply(calculate_p25i)
data['oi']=data['Ozone (ug/m3)'].apply(calculate_oi)
data['p10i']=data['PM10 (ug/m3)'].apply(calculate_p10i)
data['coi']=data['CO (mg/m3)'].apply(calculate_coi)
data['AQI']=data.apply(lambda x:calculate_aqi(x['si'],x['ni'],x['p25i'],x['p10i'],x['oi'],x['coi']),axis=1)
df= data[['From Date','AQI']]
plt.plot(df['From Date'],df['AQI'])
plt.show()
