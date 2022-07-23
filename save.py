import csv
import jobkor
import remote
import wwr


def save_to_jobs_file(jobs:list, site:str, search:str):
    # open 함수는 파일을 열어준다. 없으면 생성해준다. 쓰기모드 사용.
    file = open(f'jobs/{site}_{search}.csv', mode='w')
    writer = csv.writer(file)

    writer.writerow(["company", "title", "link"])
    for job in jobs:
        # company 의 value 들을 리스트로 만들기
        writer.writerow(list(job.values()))

    return
