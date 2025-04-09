import streamlit as st
import pandas as pd
import os

# 형태소 분석기
from konlpy.tag import Okt, Komoran

# 사용자설정 lib
import lib.myTextMining as tm
import lib.NaverNewsCrawler as crawler
import lib.STVisualizer as sv

def main():
    st.title("키워드 분석(빈도수, 워드클라우드) Streamlit App")

    # ─────────────────────────────────────────────────────────
    # 사이드바 - 데이터 입력 구역 (CSV 업로드 vs. 검색어 입력으로 크롤링)
    # ─────────────────────────────────────────────────────────
    st.sidebar.header("데이터 파일 확인")
    data_mode = st.sidebar.radio("데이터 소스 선택", ("CSV 파일 업로드", "검색어 입력으로 크롤링")) #data_mode radio버튼

    data_df = None  # 데이터프레임 초기화
    col_name = "review"  # CSV 업로드 시 기본 컬럼명

    if data_mode == "CSV 파일 업로드": #data_mode radio버튼을 눌렀을때 그 버튼에 등록된 값이 "CSV파일 업로드"인 경우
        uploaded_file = st.sidebar.file_uploader("CSV 파일 업로드", type=["csv"])
        col_name = st.sidebar.text_input("분석할 텍스트 컬럼명", value="미리보기를 확인하고 입력하세요.")

        if uploaded_file is not None:
            try:
                data_df = pd.read_csv(uploaded_file)
                st.write("업로드된 CSV 미리보기")
                st.dataframe(data_df.head())
            except Exception as e:
                st.error("CSV 파일을 불러오는 중 오류가 발생했습니다.")
                st.exception(e)

    else: #data_mode radio버튼을 눌렀을때 그 버튼에 등록된 값이 "CSV파일 업로드"가 아닌경우. 지금 등록된 radio값은 "검색어 입력으로 크롤링"
        # 검색어 입력으로 크롤링 (네이버 뉴스)
        keyword = st.sidebar.text_input("검색어를 입력하세요", value="기본검색어")
        start_num = st.sidebar.number_input("start (페이지 시작)", min_value=1, max_value=1000, value=1)
        display_num = st.sidebar.number_input("display (개수)", min_value=10, max_value=100, value=20)
        if st.sidebar.button("크롤링 시작"):
            result_all = []
            resultJSON = crawler.searchNaverNews(keyword, start_num, display_num)
            if resultJSON:
                crawler.setNewsSearchResult(result_all, resultJSON)
                data_df = pd.DataFrame(result_all)
                st.write("크롤링 결과 미리보기")
                st.dataframe(data_df.head())

                # data 폴더에 저장 (폴더가 없으면 생성)
                data_folder = "data"
                os.makedirs(data_folder, exist_ok=True)
                filename = f"{keyword}_naver_news.csv"
                filepath = os.path.join(data_folder, filename)
                data_df.to_csv(filepath, index=False, encoding="utf-8-sig")
                st.success(f"크롤링 결과가 {filepath} 에 저장되었습니다.")
            else:
                st.error("크롤링에 실패했습니다. API 설정 또는 네트워크 상태를 확인하세요.")

    # ─────────────────────────────────────────────────────────
    # 사이드바 - 분석 설정 구역 (빈도수 그래프, 워드클라우드)
    # ─────────────────────────────────────────────────────────
    st.sidebar.header("분석 설정")
    
    # 체크박스를 통해 각각의 시각화 여부 결정
    show_barchart = st.sidebar.checkbox("빈도수 Bar 차트 표시", value=True)
    show_wordcloud = st.sidebar.checkbox("워드클라우드 표시", value=True)
    
    top_n = st.sidebar.slider("Bar 차트 단어 수", min_value=10, max_value=50, value=20, step=5)
    max_words_wc = st.sidebar.slider("워드클라우드 단어 수", min_value=30, max_value=100, value=50, step=10)
    
    # 형태소 분석기 선택
    tokenizer_option = st.sidebar.selectbox("형태소 분석기 선택", ["Okt", "Komoran"])
    if tokenizer_option == "Okt":
        my_tokenizer = Okt().pos
        default_tags = ['Noun', 'Adjective', 'Verb']
    else:
        my_tokenizer = Komoran().pos
        default_tags = ['NNG', 'NNP', 'VV', 'VA']

    # 불용어 목록 (필요 시 수정)
    default_stopwords = ['하며', '입', '하고', '로써', '하여', '애', '한다', '받', '하', '있', '그', '제', '영화', '보','어','션','방','진행','위','굿','기반','주','직','명','톱','의','탕','서','했던','확대','가','꽉','찬','다시',
                         '힘','파면','됐다','봄','생','민주주의','과','효','당했었다','캐나다','팀홀튼','영화인','김장','육상','하다','를','중']

    # ─────────────────────────────────────────────────────────
    # 분석 실행: CSV 업로드 혹은 크롤링 후 데이터가 준비되었을 때 실행
    # ─────────────────────────────────────────────────────────
    if st.sidebar.button("분석 시작"):
        if data_df is not None and not data_df.empty:
            # CSV 업로드 모드인 경우 지정된 컬럼명을 사용하여 텍스트 추출
            if data_mode == "CSV 파일 업로드":
                if col_name not in data_df.columns:
                    st.error(f"'{col_name}' 컬럼이 CSV 파일에 없습니다.")
                    return
                corpus_list = list(data_df[col_name].astype(str))
            else:
                # 크롤링 모드인 경우, 'description' 컬럼이 있다면 사용
                if 'description' in data_df.columns:
                    corpus_list = list(data_df['description'].astype(str))
                else:
                    st.error("크롤링된 데이터에 'description' 컬럼이 없습니다.")
                    return

            # 빈도수 분석 수행
            counter = tm.analyze_word_freq(
                corpus_list,
                tokenizer=my_tokenizer,
                tags=default_tags,
                stopwords=default_stopwords
            )

            # 선택한 시각화만 표시
            if show_barchart:
                st.subheader("상위 단어 Bar 차트")
                sv.visualize_barchart_st(
                    counter,
                    title="키워드 분석 결과",
                    xlabel="빈도수",
                    ylabel="단어",
                    top_n=top_n
                )

            if show_wordcloud:
                st.subheader("워드클라우드")
                sv.visualize_wordcloud_st(counter, max_words=max_words_wc)

            if not show_barchart and not show_wordcloud:
                st.info("하나 이상의 시각화 옵션을 선택하세요.")
        else:
            st.warning("먼저 CSV 파일을 업로드하거나, 검색어 크롤링을 통해 데이터를 준비하세요.")

if __name__ == "__main__":
    main()
