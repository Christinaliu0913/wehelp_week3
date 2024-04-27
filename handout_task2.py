#網路連線
import ssl 
#相關資源
from urllib import request
import csv
import bs4 


#略過驗證
ssl._create_default_https_context = ssl._create_unverified_context
import urllib.request as req

# 建立 CSV 文件
with open('ptt_lottery.csv',mode='w',newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['ArticleTitle', 'Like/DislikeCount', 'PublishTime'])

# 定義函數獲取資料
def Getdata(url):
    #連線至Lottery網站首頁
    request = req.Request(url, headers={
        'cookie':'over18=1',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    })

    with req.urlopen(request) as response:
        data = response.read().decode('utf-8')
    root = bs4.BeautifulSoup(data, 'html.parser')
    
        

    #獲取相關資料
    likes = root.find_all('div', class_='nrec')
    titles = root.find_all('div', class_='title')
    dates = root.find_all('div', class_='date')
    
    
    # 利用修改的方式寫入csv檔中
    with open('ptt_lottery.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        
        for i in range(len(titles)):
            
            #抓取標題  
            title_row = titles[i].text.strip()    
            # 抓取推文次數資料，檢查是否找到喜歡次數，如果沒有就設定為 0
            if likes[i].span != None:
                like_row = likes[i].text.strip() 
            else:
                like_row = '0'
            
            #連線標題點入的頁面
            upload_date_page=titles[i].find('a')
            if upload_date_page != None:
                page=upload_date_page.get('href')
                upload_url = 'https://www.ptt.cc' + page
            else:
                title_row = '未知'
                upload_url = '未知'
            print(upload_url)
            #通過驗證
            #連線至點入標題的頁面
            request2 = req.Request(upload_url, headers={
                            'cookie':'over18=1',
                            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
                        })
            with req.urlopen(request2) as uploadpage:
                datedata = uploadpage.read().decode('utf-8')
            root2 = bs4.BeautifulSoup(datedata, 'html.parser')
            #尋找發布日期
            upload_daterenew=root2.find_all('span',class_='article-meta-value')
            print(upload_daterenew)
            if upload_daterenew:
                upload_daterenew_row = upload_daterenew[-1].text.strip() 
            else:
                upload_daterenew_row = 'Unknown'
            #寫入資料
            writer.writerow([title_row, like_row, upload_daterenew_row])
        

    # 抓取上一頁的網址
    nextLink = root.find('a', string='‹ 上頁') 
    return nextLink['href']   

# 初始頁面並尋找上一頁
pageURL = 'https://www.ptt.cc/bbs/Lottery/index.html'
count = 0
while count < 3:
    pageURL = 'https://www.ptt.cc' + Getdata(pageURL)
    count += 1

