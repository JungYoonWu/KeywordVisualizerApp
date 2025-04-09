#  키워드 시각화 Streamlit 앱

네이버 뉴스 또는 CSV 파일을 기반으로 키워드를 분석하고, 빈도수 그래프 및 워드클라우드 형태로 시각화하는 Streamlit 기반 웹 애플리케이션입니다.

---

##  주요 기능

-  검색어 입력 시 네이버 뉴스에서 기사 크롤링 (자동 저장: `검색어_naver_news.csv`)
-  CSV 파일 업로드하여 분석 가능 (컬럼명 지정)
-  형태소 분석기 선택 지원 (Okt / Komoran)
-  불용어 처리 및 품사 필터링
-  빈도수 그래프 / ☁️ 워드클라우드 체크박스로 선택 가능

---

## /lib/NaverNewsCrawler.py 의 client_id, client_secret부분에 사용자의 API KEY값을 적용 후 사용하세요.

---

##  필수 패키지
streamlit, pandas, konlpy, matplotlib, wordcloud, requests, beautifulsoup4

## 실행방법
streamlit run KeywordVisualizeSTApp.py

