df_most

def top_article(df):




 = df_most_pop.groupby(['naslov', 'link','medij','foto', 'uvod']).count()\
.sort_values('keywo', ascending=False).reset_index().copy()

top_list = df_most_pop[df_most_pop.naslov==df_most.loc[0].naslov].keywo.tolist()

no_top = df_most_pop[df_most_pop.naslov != df_most.loc[0].naslov]

top_kw = str(top_list).replace('[','').replace(']','')\
.replace(',','|').replace("'","").replace(' ','').lower()

df_connected = no_top[no_top.uvod.str.lower().str.contains(top_kw)]\
.groupby(['naslov', 'medij','link']).count().reset_index()\
.sort_values('keywo', ascending=False)[:4]
