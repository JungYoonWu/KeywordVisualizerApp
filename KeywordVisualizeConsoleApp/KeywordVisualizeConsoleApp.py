import mylib.myTextMining as tm
from konlpy.tag import Okt, Komoran
#코퍼스 로딩
#input_filename = "daum_movie_review.csv"
input_filename = "젤렌스키_naver_news.csv"
corpus_list = tm.load_corpus_from_csv("./data/"+input_filename, "description")
print(corpus_list[:10])

#빈도수 추출 Okt
#my_tokenizer = Okt().pos
#my_tags = ['Noun', 'Adjective', 'Verb']
#my_stopwords = ['하며', '입', '하고', '로써', '하여', '애','한다', '받', '하', '있', '그', '제', '영화', '보']

my_tokenizer = Komoran().pos
my_tags = ['NNG', 'NNP', 'VV', 'VA']
my_stopwords = ['하며', '입', '하고', '로써', '하여', '애','한다', '받', '하', '있', '그', '제', '영화', '보']


counter = tm.analyze_word_freq(corpus_list, my_tokenizer, my_tags, my_stopwords)
#print(list(counter.items())[:20])
#tm.visualize_barchar(counter, "젤렌스키 네이버 뉴스 키워드 분석", "빈도수", "키워드")
tm.visualize_wordcloud(counter)