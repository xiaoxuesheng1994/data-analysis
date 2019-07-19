import pandas as pd
import pyecharts as pec

kw_counts_list_by_score = [[] for i in range(10)]
for i in range(4,10):
	kw_counts_list_by_score[i] = pd.read_csv('movie_keywords_by_score/{}_movie_keywords.csv'.format(i))

# print(kw_counts_list_by_score)

kw_percentage_df = pd.DataFrame([],
	columns=list(range(4,10)),
	index = kw_counts_list_by_score[9]['kw'][:10]
	)
#print(kw_percentage_df)
for i in range(4,10):
	kw=kw_counts_list_by_score[i]
	kw = kw[kw['kw'].isin(kw_percentage_df.index)] # 筛选出kw中的kw同时也存在于9分电影的数据
	kw_percentage_df[i]= pd.Series(list(kw['percentage']),index=kw['kw'])
	#a = list(kw['percentage'])
kw_percentage_df.fillna(0,inplace=True)

print(kw_percentage_df)

data = []
i = 0
for index in kw_percentage_df.index:
	j=0
	for column in kw_percentage_df.columns:
		data.append([j,i,kw_percentage_df[column][index]*100])
		j += 1
	i+=1
# print(data)

heatmap = pec.HeatMap()
heatmap.add('电影关键词热力图',
	kw_percentage_df.columns,
	kw_percentage_df.index,
	data,
	is_visualmap=True,
	visual_text_color='#000',
	visual_range = [0,10],
	visual_orient = 'horizontal'
	)
heatmap.render()