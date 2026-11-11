from Movie import Movie
from Series import Series
import json

def from_dict(data):
     if data['type'] not in ('movie','series'):
        return None
     
     genres_text = ", ".join(data['genres'])
     if data['type'] == 'movie':
        item = Movie(data['title'],data['year'],genres_text)
     else:
        item = Series(data['title'],data['year'],genres_text,data['seasons'])
        item.episodes_watched = [tuple(ep) for ep in data['episodes_watched']]
     item.rating = data['rating']
     item.watched = data['watched']

     return item
class MovieLibrary:

  def __init__(self, path= 'library.json'):
    self.path = path
    self.movies = {}
  
  def add(self, item):
     if not isinstance(item, (Movie, Series)):
        return False

     title = self._key(item.title)
     if title in self.movies:
        return False
     
     self.movies[title] = item

     return True

  def get(self,title):
     return self.movies.get(self._key(title))
  
  def remove(self,title):
     title = self._key(title=title)
     if title in self.movies:
        del self.movies[title]
        return True

     return False
  
  def search(self, title):
     sorted_movies = sorted(self.movies.items())
     title = self._key(title)
     return [movie for movie_title, movie in sorted_movies if title in movie_title]
  
  def _key(self,title):
      return title.strip().lower()
  
  def by_genre(self, genre):
     sorted_movies = sorted(self.movies.items())
     return [movie[1] for movie in sorted_movies if self._key(genre) in movie[1].genres]
  
  def watchlist(self):
     sorted_movies = sorted(self.movies.values(), key=lambda m: m.year)
     return [movie for movie in sorted_movies if not movie.watched]
  
  def top_rated(self, n):
     if n <= 0:
        n = 0
     rated_movies = [m for m in self.movies.values() if m.rating is not None]

     sorted_movies = sorted(rated_movies, key=lambda m: (-m.rating,m.title.lower()))
     
     return sorted_movies[:n]
     
  def stats(self):
     total_title_count = len(self.movies)
     watched_count = 0
     average_rating = None
     ratings = []
     genre_counts = {}
     most_common_genre = None
     genres = set()
     
     for movie in self.movies.values():
        if movie.watched:
           watched_count += 1
        if movie.rating is not None:
           ratings.append(movie.rating)
        for g in movie.genres:
           genre_counts[g] = genre_counts.get(g,0) + 1
           genres.add(g)

     if len(ratings):           
        average_rating = round(sum(ratings) / len(ratings),1)
      
     if genre_counts:
        
        max_count = max(genre_counts.values())

        most_common_genre = sorted(
           genre for genre, count in genre_counts.items()
            if count == max_count)[0]
        
     return {
        "total": total_title_count,
        "watched": watched_count,
        "average_rating":average_rating,
        "genre_counts":genre_counts,
        "genres":genres,
        "most_common_genre":most_common_genre}
  def save(self):
     data = [movie.to_dict() for movie in self.movies.values()]     
     with open(self.path, "w") as f:
        json.dump(data,f,indent=2)  

     return len(data)
  
  def load(self):
     try:
        with open(self.path) as f:
            data = json.load(f)
     except FileNotFoundError:
        return "new"
     except json.JSONDecodeError:
        self.path = "library_recovered.json"
        return "corrupted"
      
     for item in data:
        new_item = from_dict(item)
        if new_item is not None:
           self.add(new_item)
           
     return "loaded"
