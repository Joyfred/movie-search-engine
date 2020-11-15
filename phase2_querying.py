import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


query = input("Search movie based on any field: ")

with open("movies.json", "r") as data_file:
    movies = json.load(data_file)

movie_description = []
for movie in movies:
    movie_description.append(movie['description'])

movie_description.append(query)

vectorizer = TfidfVectorizer()
tfidf = vectorizer.fit_transform(movie_description)
cosine_similarities = linear_kernel(tfidf[-1], tfidf).flatten()
#top 5 results excluding the query
related_docs_indices = cosine_similarities.argsort()[-7:-2][::-1] 
print(related_docs_indices)
print(cosine_similarities[related_docs_indices])

    