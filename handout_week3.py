import json
import csv
import urllib.request as req
#網路連線
import ssl 
import bs4 

ssl._create_default_https_context = ssl._create_unverified_context
#StationName,AttractionTitle1,AttractionTitle2,AttractionTitle3,


with open('spot1.csv',mode='w',newline='') as newfile:
    writer= csv.writer(newfile)
#SpotTitle,District,Longitude,Latitude,ImageURL

URL1='https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1'
URL2='https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-2'

#-----------------------建立spot1.csv------------------
#建立一個編號對站名的字典
with req.urlopen(URL2) as file2:
    data2=json.load(file2)
    station_loca＿num=dict()
    for i in data2['data']:
        StationName = i['MRT']
        station_number= i['SERIAL_NO']
        station_loca_num[StationName]=station_number
    print(station_loca_num)
#建立一個編號對地區的字典
with req.urlopen(URL2) as file3:
    data3=json.load(file3)
    MRTnumber=dict()
    for i  in data3['data']:
        StationName = i['MRT']
        station_number= i['SERIAL_NO']
        address = i['address']
        District =address[5:8]
        MRTnumber[station_number]= District
    #print(MRTnumber)

with req.urlopen(URL1) as file:
    data=json.load(file)
#SpotTitle,District,Longitude,Latitude,ImageURL
with open('spot1.csv',mode='a',newline='') as file:
    writer = csv.writer(file)
    for i  in data['data']['results']:
        spottitle= i['stitle']
        MRTnumber2= i['SERIAL_NO']
        #從info裡面找ststion_loca的車站在對上地名
        #一堆字包含站名
        District2='unknow'
        for station_num,district_name in  MRTnumber.items():
            if station_num in  MRTnumber2:
                District2= district_name
                
        longitude= i['longitude']
        latitude= i['latitude']
        filelist= i['filelist']
        image= filelist
        image= filelist.split('https')[1]
        writer.writerow([spottitle,District2,longitude,latitude,'https'+image])



#-----------------------建立mrt1.csv------------------
with open('mrt1.csv',mode='w',newline='') as newfile:
    writer= csv.writer(newfile)


attra=dict()
with req.urlopen(URL1) as file:
    data=json.load(file)
    #建一個字典來記錄

    for i  in data['data']['results']:
        spottitle= i['stitle']
        MRTnumber2= i['SERIAL_NO']
        with req.urlopen(URL2) as file2:
            data2=json.load(file2)
            for i in data2['data']:
                if i['SERIAL_NO'] == MRTnumber2:
                    if i['MRT'] in attra:
                        attra[i['MRT']].append(spottitle)
                    else:
                        attra[i['MRT']]=[spottitle]
                
            #從info裡面找ststion_loca的車站在對上地名
print(attra)        
            
with open('mrt1.csv',mode='a',newline='') as file:
    writer = csv.writer(file)
    for station_name, spottitle in attra.items():
        writer.writerow([station_name]+spottitle)        


# --------------------Task2------------------ 
#建一個csv檔
with open('ptt_lottery.csv',mode='w',newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['標題','推文次數','日期'])

def Getdata(url):
    
    request =req.Request(url, headers={
        'cookie':'over18=1',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    })


    with req.urlopen(request) as response:
        data = response.read().decode('utf-8')

    root=bs4.BeautifulSoup(data, 'html.parser')

    # 喜歡次數
    likes = root.find_all('div', class_='nrec')
    # 標題
    titles = root.find_all('div', class_='title')
    # 日期
    dates = root.find_all('div', class_='date')
    #利用修改的方式寫入csv檔中
    with open('ptt_lottery.csv',mode='a',newline='') as file:
        writer = csv.writer(file)
        for i in range(len(titles)):
            title_row = titles[i].text.strip()
            # 檢查是否找到喜歡次數，如果沒有就設定為 0
            if likes[i].span != None:
                like_row = likes[i].text.strip() 
            else:
                like_row = '0'
            date_row = dates[i].text.strip()
            writer.writerow([title_row, like_row, date_row])
    #抓取上一頁的網址
    nextLink=root.find('a',string='‹ 上頁') 
    return nextLink['href']   
 
pageURL='https://www.ptt.cc/bbs/Lottery/index.html'
count=0
while count<3:
    pageURL='https://www.ptt.cc'+Getdata(pageURL)
    count+=1