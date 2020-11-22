import json
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer

with open("movies.json", "r") as data_file:
    movies = json.load(data_file)

def getIndex(key):
    index = dict()
    stop_words = set(stopwords.words('english'))
    
    for movie in movies:
        word_tokens = word_tokenize(movie[key].lower())
        filtered_tokens = [token for token in word_tokens if not token in stop_words]
        for token in filtered_tokens:
            if token not in index:
                index[token] = [movie['id']]
            else:
                index[token].append(movie['id'])
    return index

def groupIndex(key):
    index = dict()
    for movie in movies:
        for i in movie[key]:
            if i.lower() not in index:
                index[i.lower()] = [movie['id']]
            else:
                index[i.lower()].append(movie['id'])
    return index
    
    

title_index = getIndex('title')
description_index = getIndex('description')
genre_index = groupIndex('genre')    
stars_index = groupIndex('stars')

year_index = dict()
for movie in movies:
    if movie['year'] not in year_index:
        year_index[movie['year']] =  [movie['id']]
    else:
         year_index[movie['year']].append(movie['id'])


# query = input("Provide description: ")
# movie_description = []
# for movie in movies:
#     movie_description.append(movie['description'])

# vectorizer = TfidfVectorizer()
# X = vectorizer.fit_transform(movie_description)
