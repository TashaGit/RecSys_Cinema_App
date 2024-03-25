from typing import List

import pandas as pd
from .utils import parse


class ContentBaseRecSys:

    def __init__(self, movies_dataset_filepath: str, distance_filepath: str):
        self.distance = pd.read_csv(distance_filepath, index_col='movie_id')
        self.distance.index = self.distance.index.astype(int)
        self.distance.columns = self.distance.columns.astype(int)
        self._init_movies(movies_dataset_filepath)

    def _init_movies(self, movies_dataset_filepath) -> None:
        self.movies = pd.read_csv(movies_dataset_filepath, index_col='movie_id')
        self.movies.index = self.movies.index.astype(int)
        self.movies['genres'] = self.movies['genres'].apply(parse)

    def get_title(self) -> List[str]:
        return self.movies['title'].values

    def get_genres(self) -> List[str]:
        genres = [item for sublist in self.movies['genres'].values.tolist() for item in sublist]
        return list(genres)

    #def get_production(self) ->List[str]:
        #companies_list = []
        #for companies in self.movies['production_companies']:
            #companies = ast.literal_eval(companies)
            #for company in companies:
                #companies_list.append(company['name'])
        #return list(companies_list)

    def get_rating(self, x, rate) -> bool:
        res = x >= rate[0] and x <= rate[1]
        return res

    def find_similar_genres(self, descrs, genre):
        res = genre in descrs
        return res

    def recommendation(self, title: str, genre: str = None, rate: tuple = None, top_k: int = 5) -> List[str]:
        """
        Returns the names of the top_k most similar movies with the movie "title"
        """

        if genre is not None:
            self.movies['contains_genre'] = self.movies['genres'].apply(lambda x: self.find_similar_genres(x, genre))
            movies = self.movies.loc[(self.movies['contains_genre'] == True) | (self.movies['title'] == title)]
        else:
            movies = self.movies

        if rate is not None:
            self.movies['contains_rate'] = self.movies['vote_average'].apply(lambda x: self.get_rating(x, rate))
            movies = self.movies.loc[(self.movies['contains_rate'] == True) | (self.movies['title'] == title)]
        else:
            movies = self.movies

        indices = movies.index
        if not movies.empty and len(movies[movies['title'] == title]) > 0:
            idx = movies[movies['title'] == title].index[0]
            sim_scores = self.distance[idx].sort_values(ascending=False)

            if genre != None:
                new_sim_scores = {}
                for i in sim_scores.keys():
                    if i in indices:
                        new_sim_scores[i] = sim_scores[i]
                sim_scores = pd.Series(data=new_sim_scores, index=new_sim_scores.keys())

            if rate != None:
                new_sim_scores = {}
                for i in sim_scores.keys():
                    if i in indices:
                        new_sim_scores[i] = sim_scores[i]
                sim_scores = pd.Series(data=new_sim_scores, index=new_sim_scores.keys())

            sim_scores = sim_scores[1:(top_k + 1)]
            movie_indices = [i for i in sim_scores.keys()]
            return movies.loc[movie_indices]['title'].values
        else:
            return []

