from .secrets import API_KEY
import tmdbsimple as tmdb
from requests.exceptions import HTTPError

tmdb.API_KEY = API_KEY

def get_search_results(search_query):
    search = tmdb.Search()
    response = search.movie(query=search_query)
    return_list = []
    for movie in response['results']:
        result_dict = {
            "title": movie['title'],
            "tmdb_id": movie['id'],
            "popularity": movie['popularity'],
            "release_date": movie['release_date'],
            "overview": movie['overview']
        }
        return_list.append(result_dict)
    return sorted(return_list, key=lambda d: d['popularity'], reverse=True)

def get_movie_info(tmdb_id):
    movie = tmdb.Movies(tmdb_id)
    try:
        info = movie.info()
        return info
    except HTTPError:
        return None
