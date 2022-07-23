from wwr import extract_wwr_jobs
from jobkor import extract_jobkor_jobs
from remote import extract_remote_jobs
from exporter import save_to_file

from flask import Flask, render_template, request, redirect, send_file


def get_jobs(word):
    jobs =[]
    jobs += extract_wwr_jobs(word)
    jobs += extract_jobkor_jobs(word)
    jobs += extract_remote_jobs(word)

    return jobs


# flask 사용하기
app = Flask(__name__)
#fake DB 만들기
db ={}

#누가 /를 요청하면 다음 함수를 실행해라
@app.route("/")
def home():
    # flask 는 템플릿을 어디서 찾아야 할지 안다.
    return render_template('potato.html')

#dynamic URL 사용하기. username이라는 플레이스 홀더
@app.route("/<username>")
# username을 받았으니 함수에서 사용해야만 한다
def potato(username):
    return redirect('/')

@app.route('/report')
def report():
    # request.args.get 함수를 이용하면 단어를 뽑을 수 있다.
    word = request.args.get('word')
    # word가 None이 아니면 소문자로 바꾸고, 아니면 home으로 리다이렉트
    if word:
        word = word.lower()

        # db 에 word가 있으면 그거 쓰고 없으면 스크래핑하기
        jobsFromDb = db.get(word)
        if jobsFromDb:
            jobs = jobsFromDb
        else:
            jobs = get_jobs(word)
            db[word] = jobs
    else:
        return redirect('/')
    # word 변수를 넘겨주자
    return render_template(
        'report.html', 
        searchingBy=word,
        resultsNumber=len(jobs),
        jobs=jobs)

@app.route('/export')
def export():
    # 예외가 발생하면 /으로 리다이렉트 시키기
    try:
        word = request.args.get('word')
        if not word:
            raise Exception()
        word = word.lower()
        jobs = db.get(word)
        if not jobs:
            raise Exception()
        save_to_file(jobs)
        return send_file("jobs.csv")
    except:
        return redirect('/')
    
if __name__ == "__main__":
    app.run()