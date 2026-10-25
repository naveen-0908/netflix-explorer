import pandas as pd
import sys
from netflix_explorer.sql_connection import get_connection
from mysql.connector import Error
import unicodedata

pd.set_option('display.max_columns', None)

df = pd.read_csv('netflix_titles_nov_2019.csv')

def normalize_name(name):
    replacements = {
        'ø': 'o',
        'Ø': 'O',
        'æ': 'ae',
        'Æ': 'AE',
        'å': 'a',
        'Å': 'A'
    }
    name = ''.join(replacements.get(c,c) for c in name)
    name = ''.join(c for c in unicodedata.normalize('NFKD', name)
                   if not unicodedata.combining(c))
    return ''.join(name.casefold().split())

# print(normalize_name("Sørensen"))
# print(normalize_name("Sorensen"))
# sys.exit(0)
# print(df.head())
# print(df.shape)
# print(df.columns)
# print(df.isnull().sum())
# print(df['type'].value_counts())
# print(df['rating'].value_counts())
# print(df['duration'].value_counts().head(20))
# print(df['director'].dropna().head(10).to_list())
# print(df['cast'].dropna().head(10).to_list())
# print(df['listed_in'].head(10).to_list())

# print(df.loc[1,'director'])
# print(df.loc[1,'director'].split(','))
# print([name.strip() for name in df.loc[1,'director'].split(',')])

# print(df.loc[0,'cast'])
# print(type(df.loc[0,'cast']))
# print(df['cast'].unique)

def clean_director(value):
    if pd.isna(value):
        return[]

    return [name.strip() for name in value.split(',')]

def clean_actor(value):
    if pd.isna(value):
        return []

    return [name.strip() for name in value.split(',')]
# print(clean_director(df.loc[1, 'director']))
# print(clean_director(df.loc[0, 'director']))
# directors = df['director'].dropna().str.split(',').explode()
# directors = directors.str.strip()
# directors = directors.drop_duplicates()

title_directors = df[['show_id', 'director']].dropna(subset=['director'])
title_directors['director'] = title_directors['director'].str.split(',')
title_directors = title_directors.explode('director')
title_directors['director'] = title_directors['director'].str.strip()
title_directors = title_directors.rename(columns={'director':'name'})
# title_directors = title_directors[['name']]
title_directors = title_directors.reset_index(drop=True)

directors = title_directors[['name']].drop_duplicates()
# title_directors = title_directors.drop_duplicates(subset=['name'], keep='first')
# print(title_directors[title_directors.duplicated(keep=False)].sort_values('name').head(50))
# print('Total:', len(directors))
# print('Unique:', title_directors.nunique())
# print(title_directors[title_directors['name'].str.lower().duplicated(keep=False)].sort_values('name').head(50))
directors['name'] = directors['name'].str.strip()
directors['name_key'] = directors['name'].str.casefold()
directors = directors.drop_duplicates(subset='name_key')
directors = directors.drop(columns='name_key')
# print(len(directors))
# print(directors[directors['name'].str.casefold()=='felix van groeningen'])
# sys.exit(0)

title_actors = df[['show_id', 'cast']].dropna(subset=['cast'])
title_actors['cast'] = title_actors['cast'].str.split(',')
title_actors = title_actors.explode('cast')
title_actors['cast'] = title_actors['cast'].str.strip()
title_actors = title_actors.reset_index(drop=True)
actors = title_actors[['cast']]
actors = actors.rename(columns={'cast':'name'})

actors['name'] = actors['name'].str.strip()
actors['name_key'] = actors['name'].str.casefold()
actors['name_key2'] = actors['name'].apply(normalize_name)

# duplicates = actors[
#     actors['name_key2'].duplicated(keep=False)
# ].sort_values('name_key2')
# print(duplicates[['name', 'name_key2']].head(50))
# sys.exit(0)
actors = actors.drop_duplicates(subset='name_key2')
actors = actors.drop(columns=['name_key','name_key2'])
# check = title_actors[
#     title_actors['cast'].str.contains(
#         'Birgitte Hjort',
#         case=False,
#         na=False
#     )
# ]
# print(check['cast'].to_string(index=False))
# print(actors[actors['name'].str.contains('Luis Guzman', case=False, na=False)]
# print(actors.columns)
# print('Unique names:', actors['name'].nunique())
# print('Unique Keys:', actors['name_key2'].nunique())
# print('Duplicate normalized:',actors['name_key2'].duplicated().sum())
# sys.exit(0)
# print(title_actors.head())
# print(title_actors.shape)
# print(df.loc[1,'cast'].split(','))
# print(title_actors['cast'].nunique())

title_genre = df[['show_id','listed_in']].dropna(subset=['listed_in'])
title_genre['listed_in'] = title_genre['listed_in'].str.split(',')
title_genre = title_genre.explode('listed_in')
title_genre['listed_in'] = title_genre['listed_in'].str.strip()
title_genre = title_genre.reset_index(drop=True)
title_genre = title_genre.rename(columns={'listed_in':'name'})
genres = title_genre[['name']].drop_duplicates()
# print(genres[
#     genres['name'].duplicated(keep=False)
# ].sort_values('name'))
# print(genres.columns)
# print(genres.nunique())
# print("count:",len(genres))
genres = genres.reset_index(drop=True)
# print("after reset:", len(genres))
# sys.exit(0)

titles = df[['show_id', 'title', 'country','date_added','release_year','rating','duration','description','type']]

print(titles['show_id'].is_unique)
print(titles['show_id'].duplicated().sum())

def load_data(df, table_name):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cols = ", ".join(df.columns)
        placeholder = ", ".join(["%s"] * len(df.columns))
        rows_to_insert = [
            tuple(
                None if pd.isna(value)
                else value.item() if hasattr(value, 'item')
                else value
                for value in row
            )
            for row in df.to_numpy()
        ]
        sql_stat = f'''insert into {table_name} ({cols})
        values ({placeholder})'''
        cursor.executemany(sql_stat, rows_to_insert)
        connection.commit()
        connection.close()
        print('load completed')
    except Error as e:
        print(f"Execution failed with error: {e}")

# print(load_sample(directors, 'directors'))
# load_data(genres, 'genres')

connection = get_connection()
actors_db = pd.read_sql("select id, name from actors", connection)
titles_db = pd.read_sql("select id as title_id, show_id from titles", connection)
# connection.close()


title_actors = title_actors.rename(columns={'cast':'name'})
actors_db = actors_db.rename(columns={'id':'actor_id'})
title_actors['name_key'] = title_actors['name'].apply(normalize_name)
actors_db['name_key'] = actors_db['name'].apply(normalize_name)

# print(title_actors[['name','name_key']].head(10))
# print(actors_db[['name', 'name_key']].head(20))
# sys.exit(0)
title_actors_mapped = title_actors.merge(
    actors_db[['actor_id','name_key']],
    on='name_key',
    how='inner'
)
title_actors_mapped = title_actors_mapped.merge(titles_db, on='show_id', how='inner')
title_actors_final = title_actors_mapped[['title_id','actor_id']].drop_duplicates()

# print("original relationships:",len(title_actors))
# print("Final unique relationships:",len(title_actors_final))
# print("Duplicate pairs removed:",len(title_actors)-len(title_actors_final))
# load_data(title_actors_final, "title_actors")
genre_db = pd.read_sql("select id, name from genres", connection)
# connection.close()
# print(title_genre.columns)
genre_db = genre_db.rename(columns={'id':'genre_id'})
title_genre_mapped = title_genre.merge(
    genre_db,
    on='name',
    how='inner'
    )
title_genre_mapped = title_genre_mapped.merge(
    titles_db,
    on='show_id',
    how='inner'
)
title_genre_final = title_genre_mapped[['title_id','genre_id']].drop_duplicates()
# duplicates = title_genre_final[title_genre_final.duplicated(subset=['title_id','genre_id'],keep=False)]
# print(duplicates)
# print("Duplicated rows:",duplicates.shape[0])
# load_data(title_genre_final,"title_genres")
directors_db = pd.read_sql("select id, name from directors", connection)
connection.close()

title_directors['name_key'] = title_directors['name'].apply(normalize_name)

directors_db['name_key'] = directors_db['name'].apply(normalize_name)

title_directors_mapped = title_directors.merge(
    directors_db[['id','name_key']],
    on='name_key',
    how='inner'
)
title_directors_mapped = title_directors_mapped.rename(columns={'id':'director_id'})

title_directors_mapped = title_directors_mapped.merge(
    titles_db,
    on='show_id',
    how='inner'
)

title_directors_final = title_directors_mapped[['title_id','director_id']].drop_duplicates()

# duplicates = title_directors_mapped[title_directors_mapped.duplicated(subset=['title_id','director_id'],keep=False)]
# print(duplicates)
# print("Duplicated rows:",duplicates.shape[0])
# print(directors_db.shape)
# load_data(title_directors_final,"title_directors")