import streamlit as st
import requests
from bs4 import BeautifulSoup

# 페이지 설정
st.set_page_config(page_title="VIP 비서", page_icon="🤵")

# 세련된 다크 디자인 입히기
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .report-card { background-color: #161b22; padding: 20px; border-radius: 15px; border: 1px solid #30363d; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🤵 VIP 인텔리전스 비서")

# 분석 점수 엔진
SCORE_DICT = {'상승': 15, '급등': 20, '최고': 15, '실적': 10, '호재': 15, '하락': -15, '급락': -25, '위기': -20}

# 종목 입력
keyword = st.text_input("분석할 종목명을 입력하세요", placeholder="예: 테슬라, 삼성전자")

if st.button("🎯 정밀 분석 시작"):
    if keyword:
        with st.spinner("데이터 분석 중..."):
            url = f"https://news.google.com/rss/search?q={keyword}+when:1d&hl=ko&gl=KR&ceid=KR:ko"
            res = requests.get(url)
            soup = BeautifulSoup(res.content, 'xml')
            items = soup.find_all('item')[:4]
            
            if items:
                total_score = 0
                for item in items:
                    title = item.title.text.split(' - ')[0]
                    link = item.link.text
                    news_score = 60
                    for word, point in SCORE_DICT.items():
                        if word in title: news_score += point
                    news_score = max(0, min(100, news_score))
                    total_score += news_score
                    
                    st.markdown(f"""
                    <div class="report-card">
                        <div style="font-weight:bold; font-size:1.1em;">{title}</div>
                        <div style="color:#f1c40f;">분석 점수: {news_score}점</div>
                        <a href="{link}" target="_blank" style="color:#58a6ff; text-decoration:none;">원문 보기 ↗</a>
                    </div>
                    """, unsafe_allow_html=True)
                
                avg = total_score / len(items)
                st.metric("🤵 비서의 최종 판단", f"{avg:.1f}점")
            else:
                st.error("뉴스를 찾을 수 없습니다.")
