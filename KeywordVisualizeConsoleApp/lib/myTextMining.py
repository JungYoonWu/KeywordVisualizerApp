from collections import Counter

def load_corpus_from_csv(corpus_file, col_name):
    import pandas as pd
    data_df = pd.read_csv(corpus_file)
    result_list = list(data_df[col_name])
    return result_list

def tokenize_korean_corpus(corpus_list, tokenizer, tags, stopwords):
  text_pos_list = []
  for text in corpus_list:
    text_str = str(text)  # 텍스트를 문자열로 변환
    text_pos = tokenizer(text_str)
    text_pos_list.extend(text_pos)
  token_list = [token for token, tag in text_pos_list if tag in tags and token not in stopwords]
  return token_list

def analyze_word_freq(corpus_list, tokenizer ,tags, stopwords):
    token_list = tokenize_korean_corpus(corpus_list, tokenizer, tags, stopwords)
    counter = Counter(token_list)
    return counter

def visualize_barchar(counter, title, xlabel, ylabel):
    #데이터 준비
    most_common = counter.most_common(20)
    word_list = [word for word, _ in most_common]
    count_list = [count for _, count in most_common]

    #한글폰트 설정하기
    from matplotlib import font_manager, rc
    font_path = "c:/Windows/Fonts/malgun.ttf"
    font_name = font_manager.FontProperties(fname=font_path).get_name()
    rc('font', family=font_name)
    #barh
    import matplotlib.pyplot as plt
    plt.barh(word_list[::-1], count_list[::-1])
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    # 화면에 출력
    plt.show()

def visualize_wordcloud(counter):
    from wordcloud import WordCloud
    import matplotlib.pyplot as plt

    # 한글 폰트 path 지정
    font_path = "C:/Windows/fonts/malgun.ttf"

    # WordCloud 객체 생성
    wordcloud = WordCloud(font_path, background_color='ivory', width=600, height=400, max_words=50)

    wordcloud = wordcloud.generate_from_frequencies(counter)
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.show()