import sqlite3
import pandas as pd
import jieba
import pyecharts as pec
import math


def get_movie_id_list(min_comments_count):
	#统计各个电影的评论数
	movie_list = comment_data['MOVIEID'].value_counts()
	# print(movie_list)
	# 筛选评论数大于100的电影
	movie_list=movie_list[movie_list.values>min_comments_count]
	return(movie_list.index)

# 得到一部电影的前count 个关键词
def get_comment_keywords_count(movie_id, count):
	comment_list = comment_data[comment_data['MOVIEID']==movie_id]['CONTENT'] 
	#print(comment_list)
	comment_str_all=''
	for comment in comment_list:
		comment_str_all += comment+'\n'
	#print(comment_str_all)

	# 获取分词后的列表
	seg_list = list(jieba.cut(comment_str_all))
	#print(seg_list)
	# 转换成pandas的series类型数据
	keywords_counts = pd.Series(seg_list)       # 把列表转换成series数据，有了索引
	#print(keywords_counts)
	# 统计各个关键词的出现次数
	keywords_counts = keywords_counts[keywords_counts.str.len()>1]
	# print(keywords_counts)
	# keywords_counts = keywords_counts.value_counts()
	FILTER_WORDS = ['知道','影评','电影','这么','那么','怎么','如果','这个','一个','这种','时候','什么','\n','一部','这部','没有','还有','觉得','of','is','the','看过','thing']
	# 利用str.contains()筛选数据
	FILTER_WORDS = '|'.join(FILTER_WORDS)
	keywords_counts = keywords_counts[~keywords_counts.str.contains(FILTER_WORDS)].value_counts()[:count]
	return keywords_counts

def get_movie_name_and_score(movie_id):
	movie_link='https://movie.douban.com/subject/{}/'.format(movie_id)
	search_result = movie_data[movie_data['链接']==movie_link].iloc[0]
	movie_name = search_result['电影名']
	movie_score = search_result['评分']
	return (movie_name, movie_score)

def gen_word_cloud(word_list,path_name):
	wordcloud = pec.WordCloud(width=1280,height=720)
	wordcloud.add('keywords',word_list.index,word_list.values,word_size_range=[20,100],shape = 'diamond')
	wordcloud.render(path=path_name)
	print('done')

# 连接数据库并读取表格
conn = sqlite3.connect('douban_comment_data.db')
comment_data = pd.read_sql_query('select * from comment;', conn)
movie_data = pd.read_excel('douban_movie_data.xlsx')
#print(comment_data)

# movie_id = '1292052'
# get_comment_keywords_count(movie_id, 30)
# keywords_counts = get_comment_keywords_count(movieid,100)
# movie_name, movie_score = get_movie_name_and_score(movieid)
# path_name = 'wordcloud/{}_{}.html'.format(movie_name,movie_score)
# gen_word_cloud(keywords_counts,path_name)

kw_list_by_score = [[] for i in range(10)]          # [[], [], [], [], [], [], [], [], [], []]
kw_counts_list_by_score = [[] for i in range(10)]   #
# print(kw_list_by_score)
# 筛选出评论数是300以上的电影的id
movie_id_list = get_movie_id_list(300)

for movie_id in movie_id_list:
	word_list = get_comment_keywords_count(movie_id,30)
	movie_name, movie_score = get_movie_name_and_score(movie_id)
	try:
		kw_list_by_score[math.floor(movie_score)].extend(word_list.index) # 把当前movie_id的关键词添加到这个列表对应的分数那一栏
		kw_counts_list_by_score[math.floor(movie_score)].extend(word_list.values) # 添加关键词的数量
	except:
		print(movie_id)

# print(kw_list_by_score,kw_counts_list_by_score)

for i in range(10):
	if kw_list_by_score[i]:
		kw30_with_counts = pd.DataFrame({
			'kw':kw_list_by_score[i],
			'counts':kw_counts_list_by_score[i]
			})
		kw30_with_counts = kw30_with_counts.groupby('kw').sum().sort_values(by='counts', ascending=False)[:30]
		counts_sum = kw30_with_counts['counts'].sum()
		kw30_with_counts['percentage'] = kw30_with_counts['counts']/counts_sum
		kw30_with_counts.to_csv('{}_movie_keywords.csv'.format(i))
# print(kw30_with_counts)

# print(get_movie_id_list(100))

# seg_list = list(jieba.cut('我想过过过儿过过的生活'))

# print(seg_list)