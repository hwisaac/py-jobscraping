import requests
from bs4 import BeautifulSoup
import re



# re_exp = re.compile('[^/\\:?*"><|.%]')
nre_exp_str = '[/\\:?*"><|.%]'

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
            link = 'https://remoteok.com'+ link['href']
        else:
            return None
    else:
        return None
    

    return {'company':company, 'title': title, 'link' : link}

# (검색어)-> jobs 검색 페이지에서 jobs 뽑아내기
def extract_remote_jobs(search) ->list:
    URL= f"https://remoteok.com/remote-{search}-jobs"
    jobs = []

    # 이래처럼 해줘야 data에 503 에러가 안남
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
    print(len(jobs), 'remote jobs')
    return jobs
