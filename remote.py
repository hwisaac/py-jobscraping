from urllib.parse import _NetlocResultMixinBytes
import requests
from bs4 import BeautifulSoup
import re
import save
import time



# re_exp = re.compile('[^/\\:?*"><|.%]')
nre_exp_str = '[/\\:?*"><|.%]'


brand_test_url='http://footlockerkr.alba.co.kr/'

# li -> {company, title, link} 정보 dict 를 반환한다.
def tr_to_info(tr)->dir:
    company = tr.find("h3", {'itemprop': 'name'}).string.strip()
    
    if company:
        company = re.sub(nre_exp_str,'_', company)
    else:
        return None

    
    title = tr.find('h2', {'itemprop': 'title'}).string.strip()
    if not title:
        return None
    
    # 링크를 못찾으면 None 반환
    link = tr.find('td',{'class': 'source'})
    if link:
        link = link.find('a')
        if link:
            link = link['href']
        else:
            return None
    else:
        return None
    
    print(link)

    return {'company':company, 'title': title, 'link' : link}

# (검색어)-> jobs 검색 페이지에서 jobs 뽑아내기
def extract_remote_jobs(search) ->list:
    URL= f"https://remoteok.com/remote-{search}-jobs"
    jobs = []

    # 이래처럼 해줘야 data에 503 에러가 안남
    print('Connecting to remoteok')
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
    data = requests.get(URL, headers = headers)
    
    # 데이터 추출해서 html 알려주기
    soup = BeautifulSoup( data.text , 'html.parser')    
    
    # # tr 태그의 클래스명 class:job 찾아 행렬로 반환 
    trs_jobs = soup.find_all("tr" , {'class' : 'job'})

    

    for tr in trs_jobs:
        # tr_to_info(tr) ->{company, title, link} 함수로 정보를 꺼내고 None 타입이 아닌경우만 jobs 리스트에 넣는다
        x = tr_to_info(tr)
        if x:
            jobs.append(x)
            print('remoteok searching: ',x )

    return jobs

extract_remote_jobs('java')


# brand_link -> jobs={local,title,company,pay}각각의 brand 사이트 마다 jobs 정보 뽑기 
def extract_alba_jobs(brand_link) -> dir:
    jobs=[]
    result = requests.get(brand_link)

    # 자료를 뽑자
    soup = BeautifulSoup( result.text , 'html.parser')
    data = soup.find_all("tr", {'style': ""})
    data = data[1:]
    for da in data:
        local  = da.find("td", {'class': 'local'})
        if local == None:
            local = "None"
        else:
            local = local.text

        title = da.find("span", {'class': 'title'})
        if title == None:
            title = "None"
        else:
            title = title.text

        company = da.find("span", {'class': 'company'})
        if company == None:
            company = "None"
        else:
            company = company.text
            # company = re_exp.match(company).group()
            company = re.sub(nre_exp_str,'_', company)

        pay = da.find("span", {'class': 'number'})
        if pay == None:
            pay = "None"
        else:
            pay = pay.text
            
        reg_date = da.find("td", {'class': 'regDate'})
        if reg_date == None:
            reg_date = "None"
        else:
            reg_date = reg_date.text

        time = da.find("span" , {'class': 'time'})
        if time == None:
            time = "None"
        else:
            time = time.text

        jobs.append( {'local':local, 'title':title, 'company':company, 'pay':pay, 'reg_date':reg_date} )
    
    return jobs


# # 모든 브랜드 사이트에서 모든 jobs 을 저장하기.
# def scraping_all_jobs(brands):
    
#     for brand in brands:
#         save.save_to_jobs_file(brand)