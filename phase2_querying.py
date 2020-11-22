import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from operator import itemgetter

def get_relevant_documents(index):
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform(index)
    cosine_similarities = linear_kernel(tfidf[-1], tfidf).flatten()
    # cosine_similarities = np.array([x for x in cosine_similarities if x!=0.0])
    
    #fetch top 5 results excluding the query
    relevant_docs_index = cosine_similarities.argsort()[-6:-1][::-1]
    # relevant_doc_scores  = cosine_similarities[relevant_doc_indices]
    # relevant_doc_params  = zip(relevant_doc_indices, relevant_doc_scores)
    relevant_docs_index = [index for index in relevant_docs_index if cosine_similarities[index] != 0.0]
    # print(relevant_docs_index, itemgetter(*relevant_docs_index)(cosine_similarities))
    return relevant_docs_index
    
def get_movies(query):
    with open("movies.json", "r") as data_file:
        movies = json.load(data_file)

    movie_description = []
    stars = []
    genre = []
    directors = []
    title = []
    year = []
    rating = []


    for movie in movies:
        movie_description.append(movie['description'])
        stars.append(' '.join(movie['stars']))
        genre.append(' '.join(movie['genre']))
        directors.append(' '.join(movie['directors']))
        title.append(movie['title'])

        year.append(movie['year'])
        rating.append(movie['rating'])
    
    is_rating_query = all([char.isdigit() or char=='.' for char in query])
    is_year_query   = all([char.isdigit() for char in query])
    indices = []
    
    if is_year_query:
        indices = [i for i, x in enumerate(year) if x == query]

    if is_rating_query:
        indices = [i for i, x in enumerate(rating) if x == query]
        
    if len(indices):
        relevant_movies = itemgetter(*indices)(movies)
        return relevant_movies
    

    title.append(query)
    genre.append(query)
    stars.append(query)
    directors.append(query)
    movie_description.append(query)
    
    relevant_movies_index = set()
    print(relevant_movies_index)
    relevant_movies_index.update(get_relevant_documents(title))
    relevant_movies_index.update(get_relevant_documents(genre))
    relevant_movies_index.update(get_relevant_documents(stars))
    relevant_movies_index.update(get_relevant_documents(directors))
    relevant_movies_index.update(get_relevant_documents(movie_description))
    
    
    relevant_movies_index = list(relevant_movies_index)
    print(relevant_movies_index)
    
    if(relevant_movies_index):
        relevant_movies = itemgetter(*relevant_movies_index)(movies)
    else:
        relevant_movies = []
    
    if(type(relevant_movies) == dict):
        return [relevant_movies]

    return list(relevant_movies)

    
if __name__ == '__main__':
    print("hello world")
    print(get_movies("vikram"))
    # print(get_relevant_documents(stars))
    # print(related_docs_indices)
    # print(cosine_similarities[related_docs_indices])