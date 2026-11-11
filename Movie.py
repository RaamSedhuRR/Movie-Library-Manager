class Movie:
  def __init__(self, title, year, genres):
    self.title = title
    self.year = year
    self.genres = self.clean_genres(genres)
    self.rating = None
    self.watched = False
  
  def rate(self, score):
    if score > 0 and score <= 10:
      self.rating = score
      self.mark_watched()
      return True
    else:
      return False
     
  def mark_watched(self):
    if self.watched:
      return False
    else:
      self.watched = True
      return True
  
  def clean_genres(self, text):
    genres = set()

    for genre in text.split(","):
        genre = genre.strip().lower()
        if genre:
            genres.add(genre)
    return genres
  
  def __str__(self):
    genres_text = ", ".join(sorted(self.genres))          
    rating_status = f"{self.rating}/10" if self.rating is not None else "not rated"
    watch_status = "watched" if self.watched else "unwatched" 
    return f"{self.title} ({self.year}) [{genres_text}] {rating_status} {watch_status}"
  
  def to_dict(self):
    return {
     "type": 'movie',
     "title": self.title,
     "year" : self.year,
     "genres" : sorted(self.genres),
     "rating" : self.rating,
     "watched": self.watched
    }
  
