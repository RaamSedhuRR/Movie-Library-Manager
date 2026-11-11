from Movie import Movie


class Series(Movie):
  def __init__(self, title, year, genres, seasons):
    super().__init__(title, year, genres)
    self.seasons = seasons
    self.episodes_watched = []
  
  def watch_episode(self,season, episode):
    if season <= 0 or episode <= 0 or season > self.seasons or (season, episode) in self.episodes_watched:
      return False
    self.episodes_watched.append((season,episode))
    return True

  def progress(self):
    return len(self.episodes_watched)
  
  def __str__(self):
    return super().__str__() + (
        f", {self.seasons} season" if self.seasons == 1
        else f", {self.seasons} seasons"
    ) + f", {self.progress()} episodes watched"
  
  def to_dict(self):
     data = super().to_dict()
     data["type"] = 'series'
     data["seasons"] = self.seasons
     data["episodes_watched"] = self.episodes_watched
     return data