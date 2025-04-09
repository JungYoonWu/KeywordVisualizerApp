import streamlit as st
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from matplotlib import font_manager, rc

def visualize_barchart_st(counter, title, xlabel, ylabel, top_n=20):
    # 상위 빈도수 top_n 개
    most_common = counter.most_common(top_n)
    word_list = [word for word, _ in most_common]
    count_list = [count for _, count in most_common]

    # 한글 폰트 설정 (Windows 기준)
    font_path = "C:/Windows/Fonts/malgun.ttf"
    font_name = font_manager.FontProperties(fname=font_path).get_name()
    rc('font', family=font_name)

    fig, ax = plt.subplots()
    ax.barh(word_list[::-1], count_list[::-1])
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    st.pyplot(fig)

def visualize_wordcloud_st(counter, max_words=50):
    # 한글 폰트 설정
    font_path = "C:/Windows/Fonts/malgun.ttf"

    wordcloud = WordCloud(
        font_path=font_path,
        background_color='white',
        width=600,
        height=400,
        max_words=max_words
    )

    wordcloud = wordcloud.generate_from_frequencies(counter)

    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')

    st.pyplot(fig)
