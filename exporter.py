import csv

def save_to_file(jobs):
    # open 함수는 파일을 열어준다. 없으면 생성해준다. 쓰기모드 사용.
    file = open('jobs.csv', mode='w')
    writer = csv.writer(file)

    writer.writerow(["company", "title", "link"])
    for job in jobs:
        # job 의 value 들을 리스트로 만들기
        writer.writerow(list(job.values()))