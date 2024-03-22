
import pandas as pd
import numpy as np
movies_df = pd.read_csv('/content/kaggle-movie-data-/tmdb_5000_movies.csv')
credits_df = pd.read_csv('/content/kaggle-movie-data-/tmdb_5000_credits.csv')

credits_df.rename(columns = {'movie_id' : 'id'} , inplace = True)

movies_df.info()

credits_df.info()

common_df = pd.merge(movies_df , credits_df , on = 'id')

common_df.drop(['homepage', 'title_x', 'title_y', 'production_companies'] , axis = 1 , inplace = True)
common_df.dropna(inplace = True)
common_df.info()

# calculating weighted_rating
R = common_df['vote_average']
v = common_df['vote_count']
C = common_df['vote_average'].mean()
print(C)
m = common_df['vote_count'].quantile(0.9)
print(m)
common_df['weighted_rating'] = (R*v + C*m) / (v + m)

from ast import literal_eval

features = ['cast' , 'crew', 'keywords', 'genres']
for feature in features:
  common_df[feature] = common_df[feature].apply(literal_eval)

def get_director(crew):
  for crew_member in crew:
    if crew_member['job']  ==  'Director':
      return crew_member['name']

  return np.nan

common_df['director'] = common_df['crew'].apply(get_director)

def get_name_list(column_value):
  names_list = []
  if isinstance(column_value , list):
    for element in column_value:
      names_list.append(element['name'])

  return names_list

features = ['cast' , 'keywords' , 'genres']
for feature in features:
  common_df[feature] = common_df[feature].apply(get_name_list)

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

def create_soup(x):
   return ' '.join(x['keywords']) + ' ' + ' '.join(x['cast']) + ' ' + x['director'] + ' ' + ' '.join(x['genres'])
common_df['soup'] = common_df.apply(create_soup, axis=1)

# resetting index
common_df = common_df.reset_index()
indices = pd.Series(common_df.index, index=common_df['original_title'])

# converting dataframe to csv
common_df.to_csv('movies.csv')

# downloading file
from google.colab import files
files.download('movies.csv')
