from urllib.parse import _NetlocResultMixinBytes
import requests
from bs4 import BeautifulSoup
import re
import save


# re_exp = re.compile('[^/\\:?*"><|.%]')
nre_exp_str = '[/\\:?*"><|.%]'


# item -> {company, title, link} 정보 dict 를 반환한다.
def div_to_inf(item)->dir:
    company = item.find("a").string.strip()
    if company:
        company = re.sub(nre_exp_str,'_', company)
    else:
        return None

    extract =item.find('a', {'class': 'title'}) 
    title = extract['title']
    
    if not title:
        return None
    
    link= extract['href']
    if link:
        link ="https://www.jobkorea.co.kr" + link 
    else:
        return None
    
    return {'company':company, 'title': title, 'link' : link}


def extract_jobkor_jobs(search) ->list:
    URL= f"https://www.jobkorea.co.kr/Search/?stext={search}"
    jobs = []
    data = requests.get(URL)
    
    soup = BeautifulSoup( data.text , 'html.parser')   
    
    divs_lists_cnt = soup.find('div', {'class': 'lists-cnt'})
    li_list_post = divs_lists_cnt.find_all('li', {'class': 'list-post'})
    
    for item in li_list_post:
        x= div_to_inf(item.find('div', {'class': 'post'}))
        print(x)
        jobs.append(x)    
    

    return jobs



# # 모든 브랜드 사이트에서 모든 jobs 을 저장하기.
# def scraping_all_jobs(brands):
    
#     for brand in brands:
#         save.save_to_jobs_file(brand)