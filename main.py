import requests
import datetime
import os
import random

# 1. API 설정
API_URL = "https://appapi.ggaction.or.kr/api/v1/app/activity/quiz-question"
HEADERS = {
    "Host": "appapi.ggaction.or.kr",
    "Content-Type": "application/json",
    "Accept": "application/json",
    "User-Agent": "ghg-ios/1.5.1 (iPhone12,8; iOS 26.2; 2026-01-22 00:56:13)",
}
DATA = {"memInfoId": int(os.environ.get("MEM_INFO_ID"))}

ENV_KNOWLEDGE_BASE = [
    {"title": "텀블러 사용의 진실", "content": "텀블러를 하나 사서 최소 15~40번 이상 사용해야 일회용 컵보다 환경 보호 효과가 나타납니다. 하나를 오래 쓰는 습관이 탄소 중립의 시작입니다."},
    {"title": "이메일 삭제와 탄소 배출", "content": "불필요한 이메일을 보관하는 데이터 센터 운영에도 막대한 전기가 소모됩니다. 이메일 1통당 약 4g의 탄소가 배출되니 스팸 메일함을 정기적으로 비워주세요."},
    {"title": "분리배출의 핵심: 비우고 헹구기", "content": "플라스틱 용기에 음식물이 묻어 있으면 재활용이 불가능합니다. 내용물을 비우고 라벨을 제거한 뒤 깨끗이 헹궈서 배출해야 자원이 순환됩니다."},
    {"title": "대기 전력 차단하기", "content": "사용하지 않는 가전제품의 플러그를 뽑는 것만으로도 가정 내 소비 전력의 10%를 절감할 수 있습니다. 외출 시 멀티탭 스위치를 꺼주세요."},
    {"title": "채식 한 끼의 가치", "content": "소고기 1kg을 생산하는 데는 약 15,000리터의 물이 필요합니다. 일주일에 단 한 번만 채식을 해도 1년에 나무 수십 그루를 심는 효과를 냅니다."},
    {"title": "패스트 패션과 환경 오염", "content": "옷 한 벌을 만드는 데 수천 리터의 물이 쓰이고 막대한 폐수가 발생합니다. 유행을 따르기보다 좋은 옷을 오래 입는 '슬로우 패션'을 실천해 보세요."},
    {"title": "LED 조명 교체 효과", "content": "일반 전구를 LED로 교체하면 수명은 50배 길어지고 전력 소비는 80% 이상 줄어듭니다. 작은 실천으로 에너지 위기를 극복할 수 있습니다."},
    {"title": "양치컵 사용하기", "content": "양치할 때 물을 틀어놓으면 약 6리터의 물이 낭비되지만, 양치컵을 사용하면 0.6리터로 충분합니다. 물 부족 문제를 해결하는 첫걸음입니다."}
]

def fetch_quiz():
    try:
        response = requests.post(API_URL, headers=HEADERS, json=DATA, timeout=10)
        response.raise_for_status()
        return response.json().get('resultData')
    except Exception as e:
        print(f"Error fetching quiz: {e}")
        return None

def generate_html(quiz_data):
    quiz_date_raw = quiz_data.get('quizDt')
    dt = datetime.datetime.strptime(quiz_date_raw, "%Y-%m-%d")
    today_date = dt.strftime("%Y년 %m월 %d일")
    weekday_map = {0: "월요일", 1: "화요일", 2: "수요일", 3: "목요일", 4: "금요일", 5: "토요일", 6: "일요일"}
    weekday_kor = weekday_map.get(dt.weekday(), "오늘의")

    # 정답 로직
    is_correct_o = (quiz_data['answer'] == "1")
    main_symbol = "O" if is_correct_o else "X"
    main_color = "#4A90E2" if is_correct_o else "#E94E58"
    sub_text = "그렇다" if is_correct_o else "아니다"

    # [상식 노출] 랜덤 3개 추출
    selected_info = random.sample(ENV_KNOWLEDGE_BASE, 3)
    info_html = ""
    for info in selected_info:
        info_html += f"""
        <div class="info-item">
            <h4>💡 {info['title']}</h4>
            <p>{info['content']}</p>
        </div>
        """

    # [히스토리] 최근 7일 링크 생성
    history_links = ""
    if os.path.exists("history"):
        files = sorted([f for f in os.listdir("history") if f.endswith(".html")], reverse=True)[:7]
        for f in files:
            date_str = f.replace(".html", "")
            history_links += f'<li><a href="/history/{f}">{date_str} 퀴즈 정답 보기</a></li>'

    html = f"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8376160575017122" crossorigin="anonymous"></script>
        <meta name="google-adsense-account" content="ca-pub-8376160575017122">
        <title>{today_date} 퀴즈 정답</title>
        <style>
            body {{ font-family: 'Apple SD Gothic Neo', sans-serif; background-color: #F2F4F6; margin: 0; padding: 20px; display: flex; flex-direction: column; align-items: center; min-height: 100vh; }}
            .container {{ background: white; max-width: 500px; width: 100%; border-radius: 25px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); padding: 40px 20px; text-align: center; box-sizing: border-box; }}
            .date {{ color: #8B95A1; font-size: 1.1rem; margin-bottom: 5px; }}
            .title {{ color: #191F28; font-size: 1.8rem; font-weight: 800; margin-bottom: 40px; }}
            .answer-card {{ background-color: {main_color}10; border: 3px solid {main_color}; border-radius: 20px; padding: 30px 0; margin-bottom: 30px; }}
            .answer-symbol {{ font-size: 8rem; font-weight: 900; color: {main_color}; line-height: 1; }}
            .answer-text {{ font-size: 2rem; font-weight: bold; color: {main_color}; margin-top: 10px; }}
            .question-box {{ background-color: #F9FAFB; padding: 20px; border-radius: 15px; margin-bottom: 30px; text-align: left; }}
            .q-label {{ color: #4A90E2; font-weight: 900; font-size: 1.2rem; margin-right: 5px; }}
            .question-text {{ font-size: 1.3rem; line-height: 1.6; color: #333; font-weight: 600; word-break: keep-all; }}
            
            /* 추가 구성 요소 스타일 */
            .ad-section {{ margin: 20px 0; width: 100%; min-height: 100px; background: #fafafa; border: 1px dashed #ccc; display: flex; align-items: center; justify-content: center; color: #999; font-size: 0.8rem; }}
            .info-section {{ text-align: left; margin-top: 30px; padding-top: 20px; border-top: 2px solid #eee; }}
            .info-item {{ margin-bottom: 20px; }}
            .info-item h4 {{ margin: 0 0 5px 0; color: #2c3e50; font-size: 1.1rem; }}
            .info-item p {{ margin: 0; color: #666; font-size: 0.95rem; line-height: 1.5; }}
            .history-section {{ text-align: left; margin-top: 30px; background: #f8f9fa; padding: 20px; border-radius: 15px; }}
            .history-section h4 {{ margin: 0 0 10px 0; font-size: 1rem; color: #333; }}
            .history-section ul {{ padding-left: 20px; margin: 0; }}
            .history-section li {{ margin-bottom: 5px; font-size: 0.9rem; }}
            .history-section a {{ color: #4A90E2; text-decoration: none; }}
            .footer {{ margin-top: 40px; font-size: 0.8rem; color: #ADB5BD; text-align: center; width: 100%; max-width: 500px; }}
            .policy-text {{ display: none; background: #f1f1f1; padding: 15px; border-radius: 10px; margin-top: 10px; text-align: left; line-height: 1.4; }}
        </style>
    </head>
    <body>
        <div class="container">
            <!-- [유지] 기존 상단 영역 -->
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

            <!-- [추가] 광고 노출 영역 -->
            <div class="ad-section">
                <!-- 애드센스 자동 광고가 이 근처에 배치됩니다 -->
                ADVERTISEMENT
            </div>

            <!-- [추가] 상세 해설 및 랜덤 지식 상식 -->
            <div class="info-section">
                <div class="info-item">
                    <h4>💡 정답 해설</h4>
                    <p>{quiz_data['desc']}</p>
                </div>
                <hr style="border: 0; border-top: 1px solid #eee; margin: 20px 0;">
                <h3 style="font-size: 1.2rem; color: #191F28; margin-bottom: 15px;">🌍 오늘의 환경 상식</h3>
                {info_html}
            </div>

            <!-- [추가] 최근 7일 히스토리 -->
            <div class="history-section">
                <h4>📅 지난 퀴즈 보기 (최근 7일)</h4>
                <ul>{history_links if history_links else "<li>이전 기록을 쌓는 중입니다.</li>"}</ul>
            </div>
        </div>

        <!-- [추가] 필수 정책 및 격식 푸터 -->
        <div class="footer">
            <p>© 2026 Daily Wisdom. All rights reserved.</p>
            <p>
                <a href="#" onclick="document.getElementById('policy').style.display='block'; return false;" style="color:#ADB5BD;">개인정보처리방침</a> | 
                <a href="mailto:admin@dailywisdom.kr" style="color:#ADB5BD;">문의하기</a>
            </p>
            <div id="policy" class="policy-text">
                <strong>개인정보처리방침:</strong> 본 사이트는 사용자의 어떠한 개인정보도 직접 수집하거나 저장하지 않습니다. 다만, 구글 애드센스 광고 서빙을 위해 구글이 쿠키를 사용할 수 있으며, 이에 대한 통제권은 구글에 있습니다.
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
        
        # history 폴더 생성 및 저장
        if not os.path.exists("history"):
            os.makedirs("history")
        
        date_filename = f"history/{data.get('quizDt')}.html"
        with open(date_filename, "w", encoding="utf-8") as f:
            f.write(html_content)
            
        # 메인 index.html 저장
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        print("Update Success")
