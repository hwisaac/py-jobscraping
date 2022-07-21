import requests
from bs4 import BeautifulSoup
import re
import csv
import save

# re_exp = re.compile('[^/\\:?*"><|.%]')
nre_exp_str = '[/\\:?*"><|.%]'
URL = 'https://weworkremotely.com/remote-jobs/search?utf8=%E2%9C%93&term='

brand_test_url='http://footlockerkr.alba.co.kr/'

# li -> {company, title, link} 정보 dict 를 반환한다.
def li_to_info(li)->dir:
    company = li.find("span", {'class': 'company'})
    if company:
        company = company.string
        #파일명으로 쓰이기 때문에 특수문자는 대체시킨다.
        company = re.sub(nre_exp_str,'_', company)
    else:
        return None

    
    title = li.find('span', {'class': 'title'})
    if title:
        title = title.string
    else:
        return None
    link = li.find_all('a')[1]['href']
    
    if not link:
        return None

    return {'company':company, 'title': title, 'link' : link}

# (검색어)-> brands 메인페이징에서 jobs 뽑아내기
def extract_wwr_brands(search) ->list:
    
    data = requests.get(URL+search)
    # 데이터 추출해서 html 알려주기
    soup = BeautifulSoup( data.text , 'html.parser')
    jobs = []

    # section 태그의 클래스명 class:jobs 찾아 행렬로 반환 
    sections_jobs = soup.find_all("section" , {'class' : 'jobs'})

    li_tags = []
    # jobs 에서 li 태그를 뽑아서 li_jobs 에 저장
    for section in sections_jobs:
        li_tags += section.find_all('li')
        

    for li_tag in li_tags:
        # li_to_info 함수로 정보를 꺼내고 None 타입이 아닌경우만 jobs 리스트에 넣는다
        x = li_to_info(li_tag)
        if x:
            jobs.append(x)

    return jobs

extract_wwr_brands('java')


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


# 모든 브랜드 사이트에서 모든 jobs 을 저장하기.
def scraping_all_jobs(brands):
    
    for brand in brands:
        save.save_to_jobs_file(brand)