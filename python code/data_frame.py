# creating dataframe
import pandas as pd
import numpy as np

credits_df = pd.read_csv('/content/kaggle-movie-data-/tmdb_5000_credits.csv')
movies_df = pd.read_csv('/content/kaggle-movie-data-/tmdb_5000_movies.csv')

# info of credits dataframe
credits_df.info()

# changing col name to merge dataframes
credits_df.rename(columns = {'movie_id' : 'id'} , inplace = True)
credits_df.info()

# merging dataframes
common_df = pd.merge(movies_df , credits_df , on = 'id')
common_df.info()

# dropping columns : cleaning dataset
common_df.drop(['homepage', 'title_x', 'title_y', 'production_companies'] , axis = 1 , inplace = True)
common_df.info()

common_df.dropna(inplace = True)
common_df.info()

# calculating weighted average
R = common_df['vote_average']
v = common_df['vote_count']
C = common_df['vote_average'].mean()
m = common_df['vote_count'].quantile(0.9)
print(C , m)
common_df['weighted_rating'] = (R*v + C*m) / (v + m)

# sorting dataframe
common_df.sort_values('weighted_rating' , ascending = False , inplace = True)

common_df.head()

# looking at columns : cast, crew, keywords, original title, genres
common_df[['original_title' , 'cast' , 'crew' , 'keywords' , 'genres']].head(3)

# check the datatype of elements
type(common_df.loc[0].at['cast'])

# changing datatype of list
from ast import literal_eval

features = ['cast' , 'crew', 'keywords', 'genres']

for feature in features:
  common_df[feature] = common_df[feature].apply(literal_eval)

# testing the datatype again
type(common_df.loc[0].at['cast'])

# printing one element from crew column
common_df.loc[6].at['crew']

# adding director column in dataframe
def get_director(crew):
  for crew_member in crew:
    if crew_member['job']  ==  'Director':
      return crew_member['name']

  return np.nan

common_df['director'] = common_df['crew'].apply(get_director)

# print the title and director column
common_df[['original_title' , 'director']].head()

# printing first element in cast column
common_df.loc[0].at['cast']

# printing first element in keywords column
common_df.loc[0].at['keywords']

# printing first element in genres column
common_df.loc[0].at['genres']

# extracting names
def get_name_list(column_value):
  names_list = []
  if isinstance(column_value , list):
    for element in column_value:
      names_list.append(element['name'])

  return names_list

features = ['cast' , 'keywords' , 'genres']
for feature in features:
  common_df[feature] = common_df[feature].apply(get_name_list)

# verify the changes
common_df[['cast' , 'keywords' , 'genres' , 'director']].head(3)

# cleaning data
def clean_data(column_value):
  modified_list = []
  modified_string = ""
  if isinstance(column_value , list):
    for element in column_value:
      modified_string = element.replace(" " , "")
      modified_list.append(modified_string.lower())

    return modified_list

  elif isinstance(column_value , str):
    modified_string = column_value.replace(" " , "")
    return modified_string.lower()

  else:
    return ''

features = ['cast' , 'keywords' , 'genres' , 'director']
for feature in features:
  common_df[feature] = common_df[feature].apply(clean_data)

# verify the changes
common_df[['cast' , 'keywords' , 'genres' , 'director']].head(3)

# try out the .join method
b = ['hello,' , 'how' , 'are' , 'you' , '?']
c = " ".join(b)
print(c)

# creating soup
def create_soup(x):
   return ' '.join(x['keywords']) + ' ' + ' '.join(x['cast']) + ' ' + x['director'] + ' ' + ' '.join(x['genres'])
common_df['soup'] = common_df.apply(create_soup, axis=1)

# verifying the output
common_df[['original_title' , 'soup']].head()

# creating vectors or matrix
from sklearn.feature_extraction.text import CountVectorizer
count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(common_df['soup'])

from sklearn.metrics.pairwise import cosine_similarity
cosine_sim2 = cosine_similarity(count_matrix, count_matrix)

print(cosine_sim2.shape)

common_df = common_df.reset_index()
indices = pd.Series(common_df.index, index=common_df['original_title'])

def get_recommendations(title, cosine_sim):
   idx = indices[title]
   sim_scores = list(enumerate(cosine_sim[idx]))
   sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
   sim_scores = sim_scores[1:11]
   movie_indices = [i[0] for i in sim_scores]
   return common_df['original_title'].iloc[movie_indices]

get_recommendations('Fight Club', cosine_sim2)

# converting df to csv
common_df.to_csv('movies.csv')

# downloading file
from google.colab import files
files.download('movies.csv')
