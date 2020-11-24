# movie-search-engine

Primitive form of search engine is built from scratch to filter movies based on user query on varied fields based on data scraped from [IMDb](https://www.imdb.com/search/title/?count=100&groups=top_1000&sort=user_rating)

This project is implemented in 3 phases:
 
 * Phase 1 - Scraping Data using crawler & Index Creation
 * Phase 2 - Querying & Ranking + UI Intergration
 * Phase 3 - Integration with elasticsearch to add some cool features

## Phase 1 - Scraping Data + Index Creation

* **Data Collection**: 
Data is scraped from IMDb website using BeautifulSoup/Selenium in Python.

* **Index Creation**:
Each movie data is considered as a document. Index Creation can be divided into 2 fundamental steps:
  * **Dictionary Implementatio**n:
    Dictionary is implemented using Hash Tables containing all unique terms from the corpus along with its frequency.
  * **Posting List Implementation**:
    As of now, Linked List appears to be a best bet for posting lists. If performance is affected severely, Skip List will be leveraged to improve.
    Posting List will also include position so that querying can be designed in a sophisticated fashion facilitating best match searches. 

## **Phase 2 - Querying & Ranking + UI Integration**

* Ranking documents can be divided into 2 fundamental steps:
  * **Modelling documents**:
  Vector Space Model(VSM) is leveraged to model documents & queries as vectors.
  Documents and queries are represented as vectors.
  Normalised tf-idf weighting scheme is used to compute term weights
  * **Ranking documents**:
  Cosine similarity is used to compute similarity scores between documents & query.
  Relevant documents in non-increasing order of similarity score are retieved & displayed

## **Phase 3 - Elasticsearch Integration**

To further spice up search engine features, elasticsearch is used to match queries involving dynamic indexing, spelling errors and synonym matching
* As soon as data is populated in elasticsearch shards, indexing is performed in ad-hoc fashion. Also, indexing modified id as & when new data is added.
* Spelling errors can be modelled as Fuzzy String Matching problem, which can be resolved using [Levenshtein edit distance score](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-fuzzy-query.html).
  * How is it used in Movie Search Engine?
    Consider a scenario, where an user intends to search for the movie named “avenger” but misspelt as “svenge”. “svenge” can be converted to “avenger” in 2 edit distance:
      * svenge → avenge (replace ‘s’ by ‘a’)
      * avenge → avenger (insert ‘r’ to the end of string). 
* Synonym matching - Elasticsearch has a predefined set of synonyms for words in english language, which is used to retrieve movies for users searching based on movie description.

## References:
[1] Amanpreet Singh, Karthik Venkatesan and Simranjyot Singh Gill. _Building a Structured Query Engine_. https://arxiv.org/abs/1710.00454. \
[2] Justin Zobel and Alistair Moffat. _Inverted Files for Text Search Engines_. (July 2006). https://doi.org/10.1145/1132956.1132959
