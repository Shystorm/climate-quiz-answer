import requests
import datetime
import os

# 1. API 설정 (발견하신 최소한의 헤더 적용)
API_URL = "https://appapi.ggaction.or.kr/api/v1/app/activity/quiz-question"
HEADERS = {
    "Host": "appapi.ggaction.or.kr",
    "Content-Type": "application/json",
    "Accept": "application/json",
    "User-Agent": "ghg-ios/1.5.1 (iPhone12,8; iOS 26.2; 2026-01-22 00:56:13)",
}
DATA = {"memInfoId": 832149}

def fetch_quiz():
    try:
        # data-binary 대신 json 파라미터 사용 (requests가 알아서 변환해줌)
        response = requests.post(API_URL, headers=HEADERS, json=DATA, timeout=10)
        response.raise_for_status()
        return response.json().get('resultData')
    except Exception as e:
        print(f"Error fetching quiz: {e}")
        return None

def generate_html(quiz_data):
    today_date = datetime.datetime.now().strftime("%Y년 %m월 %d일")
    today_weekday = datetime.datetime.now().strftime("%A") # 요일 (영어) -> 한글 변환 필요 시 로직 추가
    
    # 요일 한글 변환
    weekday_map = {"Monday": "월요일", "Tuesday": "화요일", "Wednesday": "수요일", "Thursday": "목요일", "Friday": "금요일", "Saturday": "토요일", "Sunday": "일요일"}
    weekday_kor = weekday_map.get(today_weekday, "오늘의")

    # 정답 로직 (1=O, 0=X)
    is_correct_o = (quiz_data['answer'] == "1")
    
    # 정답에 따른 디자인 요소 설정
    if is_correct_o:
        main_symbol = "O"
        main_color = "#4A90E2" # 앱과 유사한 파란색
        sub_text = "그렇다"
    else:
        main_symbol = "X"
        main_color = "#E94E58" # 앱과 유사한 빨간색
        sub_text = "아니다"

    # HTML 템플릿
    html = f"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        
        <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8376160575017122"
     crossorigin="anonymous"></script>
        <meta name="google-adsense-account" content="ca-pub-8376160575017122">

        <title>{today_date} 퀴즈 정답</title>        
        <!-- OG 태그 추가 -->
        <meta property="og:title" content="{today_date} 퀴즈 정답" />
        <meta property="og:description" content="오늘의 기후 퀴즈 정답을 확인해보세요!" />
        <meta property="og:image" content="http://dailywisdom.kr/og_image_quiz_dailywisdom.png" />
        <meta property="og:url" content="http://dailywisdom.kr" />
        <meta property="og:type" content="website" />
        <meta property="og:site_name" content="Daily Wisdom" />
        <style>
            /* 기본 설정 */
            body {{
                font-family: 'Apple SD Gothic Neo', 'Noto Sans KR', sans-serif;
                background-color: #F2F4F6; /* 연한 회색 배경 */
                margin: 0;
                padding: 20px;
                display: flex;
                flex-direction: column;
                align-items: center;
                min-height: 100vh;
            }}
            
            .container {{
                background: white;
                max-width: 500px;
                width: 100%;
                border-radius: 25px;
                box-shadow: 0 10px 25px rgba(0,0,0,0.05);
                padding: 40px 20px;
                text-align: center;
                box-sizing: border-box;
            }}

            /* 날짜 및 제목 */
            .date {{
                color: #8B95A1;
                font-size: 1.1rem;
                margin-bottom: 5px;
            }}
            .title {{
                color: #191F28;
                font-size: 1.8rem;
                font-weight: 800;
                margin-bottom: 40px;
            }}

            /* 정답 표시 영역 (가장 크게) */
            .answer-card {{
                background-color: {main_color}10; /* 투명도 10% 배경 */
                border: 3px solid {main_color};
                border-radius: 20px;
                padding: 30px 0;
                margin-bottom: 30px;
            }}
            .answer-symbol {{
                font-size: 8rem; /* 엄청 큰 O, X */
                font-weight: 900;
                color: {main_color};
                line-height: 1;
            }}
            .answer-text {{
                font-size: 2rem;
                font-weight: bold;
                color: {main_color};
                margin-top: 10px;
            }}

            /* 문제 영역 */
            .question-box {{
                background-color: #F9FAFB;
                padding: 20px;
                border-radius: 15px;
                margin-bottom: 30px;
                text-align: left;
            }}
            .q-label {{
                color: #4A90E2;
                font-weight: 900;
                font-size: 1.2rem;
                margin-right: 5px;
            }}
            .question-text {{
                font-size: 1.3rem; /* 폰트 키움 */
                line-height: 1.6;
                color: #333;
                font-weight: 600;
                word-break: keep-all;
            }}

            /* 해설 보기 (접었다 펴기) */
            details {{
                margin-bottom: 40px;
                width: 100%;
            }}
            summary {{
                cursor: pointer;
                padding: 15px;
                background-color: #eee;
                border-radius: 10px;
                font-size: 1.1rem;
                font-weight: bold;
                color: #555;
                list-style: none; /* 화살표 없애기 */
            }}
            summary:after {{
                content: " 👇"; 
            }}
            .desc-content {{
                padding: 20px;
                background-color: #fafafa;
                border-radius: 0 0 10px 10px;
                text-align: left;
                font-size: 1.1rem;
                line-height: 1.6;
                color: #666;
                border-top: 1px solid #eee;
            }}

            /* 하단 광고 */
            .ad-container {{
                margin-top: auto;
                width: 100%;
                padding-top: 20px;
                border-top: 1px dashed #ddd;
                color: #999;
                font-size: 0.9rem;
            }}

        </style>
        </head>
    <body>

        <div class="container">
            <div class="date">{today_date}</div>
            <div class="title">{weekday_kor} 퀴즈 정답</div>

            <div class="answer-card">
                <div class="answer-symbol">{main_symbol}</div>
                <div class="answer-text">{sub_text}</div>
            </div>

            <div class="question-box">
                <span class="q-label">Q.</span>
                <span class="question-text">{quiz_data['question']}</span>
            </div>

            <details>
                <summary>💡 정답 해설 보기 </summary>
                <div class="desc-content">
                    {quiz_data['desc']}
                </div>
            </details>

            <div class="ad-container">
                광고가 표시되는 영역입니다
                </div>
        </div>

    </body>
    </html>
    """
    return html

if __name__ == "__main__":
    data = fetch_quiz()
    if data:
        html_content = generate_html(data)
        
        # 파일 저장
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        print("index.html 생성 완료")
    else:
        print("퀴즈 데이터 가져오기 실패")
