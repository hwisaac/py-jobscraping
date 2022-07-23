import requests
from bs4 import BeautifulSoup
import re


nre_exp_str = '[/\\:?*"><|.%]'
URL = 'https://weworkremotely.com/remote-jobs/search?utf8=%E2%9C%93&term='


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
    
    try:
        link = 'https://weworkremotely.com/' + li.find_all('a')[1]['href']
    
        if not link:
            return None
    except:
        return None

    return {'company':company, 'title': title, 'link' : link}

# (검색어)-> brands 메인페이징에서 jobs 뽑아내기
def extract_wwr_jobs(search) ->list:
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
    print(len(jobs), 'wwr jobs')
    return jobs
