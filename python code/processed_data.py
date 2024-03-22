
# creating dataframes
import pandas as pd

credits_df = pd.read_csv('/content/kaggle-movie-data-/tmdb_5000_credits.csv')
movies_df = pd.read_csv('/content/kaggle-movie-data-/tmdb_5000_movies.csv')

# printing first 5 rows
credits_df.head()

# printing first 5 rows
movies_df.head()

# renaming column
credits_df.rename(columns = {'movie_id' : 'id'} , inplace = True)
credits_df.head()

# merging dataset
result_df = pd.merge(movies_df , credits_df , on = 'id')

# printing shape
result_df.shape

#  printing info about dataset
result_df.info()

# dropping columns : cleaning dataset
result_df.drop(['homepage', 'title_x', 'title_y', 'production_companies'] , axis = 1 , inplace = True)

# printing info again to verify
result_df.info()

# dropping cols with na
result_df.dropna(inplace = True)
result_df.info()

# Calculating weighted average
R = result_df['vote_average']

v = result_df['vote_count']

C = result_df['vote_average'].mean()
print(C)

m = result_df['vote_count'].quantile(0.9)
print(m)

result_df['weighted_rating'] = (R*v + C*m) / (v + m)

result_df[['original_title' , 'weighted_rating']].head()

result_df.sort_values('weighted_rating' , ascending = False , inplace = True)

result_df[['original_title' , 'vote_average' , 'vote_count' , 'weighted_rating' , 'popularity']].head(10)

import plotly.express as px
bar_plot = px.bar(result_df.head(10).sort_values('weighted_rating') , x = 'weighted_rating' , y = 'original_title' , orientation = 'h')
bar_plot.show()
