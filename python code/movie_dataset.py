
# installing kaggle module
!pip install kaggle

# uploading kaggle.json file
from google.colab import files
files.upload()

# creating a new hidden directory named 'kaggle'
!mkdir -p ~/.kaggle
!cp kaggle.json ~/.kaggle
!chmod 600 ~/.kaggle/kaggle.json

# downloading dataset
!kaggle datasets download -d tmdb/tmdb-movie-metadata

# listing all the files in working directory
!ls

# unzipping
!unzip tmdb-movie-metadata.zip


# creating dataframe
import pandas as pd
credits_df = pd.read_csv('tmdb_5000_credits.csv')
movies_df = pd.read_csv('tmdb_5000_movies.csv')

# printing first 5 rows
credits_df.head()

# printing first 5 rows
movies_df.head()

# printing shape of datasets
print("Credits dataframe : " , credits_df.shape)
print("Movies dataframe : " , movies_df.shape)

# renaming a column
credits_df.rename(columns = {'movie_id' : 'id'} , inplace = True)
credits_df.head()

# merging 2 datasets
result_df = pd.merge(movies_df , credits_df , on = 'id')

# printing shape of dataset
result_df.shape
