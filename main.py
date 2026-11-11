from Movie import Movie
from Series import Series
from MovieLibrary import MovieLibrary


MENU = """
--- Movie Library ---
1. Add movie
2. Add series
3. Rate a title
4. Mark watched / watch an episode
5. Search by title
6. Filter (genre, watchlist, top rated)
7. Statistics
8. Remove a title
9. Save and quit"""


# ---------- input helpers ----------

def get_int(prompt, low, high):
    """Ask for a whole number between low and high. Return it, or None if invalid."""
    try:
        value = int(input(prompt))
    except ValueError:
        return None
    if value < low or value > high:
        return None
    return value


def get_title(prompt="Title: "):
    """Ask for a non-empty title. Return it stripped, or None if empty."""
    title = input(prompt).strip()
    return title if title else None


def find_title(library):
    """Ask for a title and return the matching object, or None (with a message)."""
    title = get_title()
    if title is None:
        print("Title can't be empty.")
        return None
    item = library.get(title)
    if item is None:
        print(f"'{title}' is not in your library.")
    return item


def print_titles(items, empty_message="Nothing to show."):
    """Print each item on its own line using its __str__."""
    if not items:
        print(empty_message)
        return
    for item in items:
        print(f"  {item}")


# ---------- menu options ----------

def ask_title_year_genres():
    """Shared questions for options 1 and 2. Returns (title, year, genres_text) or None."""
    title = get_title()
    if title is None:
        print("Title can't be empty.")
        return None

    year = get_int("Year (1888-2030): ", 1888, 2030)
    if year is None:
        print("Invalid year.")
        return None

    genres_text = input("Genres (comma-separated): ")
    return title, year, genres_text


def add_movie(library):
    answers = ask_title_year_genres()
    if answers is None:
        return
    title, year, genres_text = answers

    if library.add(Movie(title, year, genres_text)):
        print(f"Added {title}.")
    else:
        print(f"{title} is already in your library.")


def add_series(library):
    answers = ask_title_year_genres()
    if answers is None:
        return
    title, year, genres_text = answers

    seasons = get_int("Seasons (1-100): ", 1, 100)
    if seasons is None:
        print("Invalid number of seasons.")
        return

    if library.add(Series(title, year, genres_text, seasons)):
        print(f"Added {title}.")
    else:
        print(f"{title} is already in your library.")


def rate_title(library):
    item = find_title(library)
    if item is None:
        return

    score = get_int("Rating (1-10): ", 1, 10)
    if score is None:
        print("Rating must be a whole number from 1 to 10.")
        return

    item.rate(score)
    print(f"Rated: {item}")


def mark_watched(library):
    item = find_title(library)
    if item is None:
        return

    if isinstance(item, Series):
        season = get_int(f"Season (1-{item.seasons}): ", 1, item.seasons)
        if season is None:
            print("Invalid season.")
            return
        episode = get_int("Episode: ", 1, 1000)
        if episode is None:
            print("Invalid episode.")
            return
        if item.watch_episode(season, episode):
            print(f"Watched S{season}E{episode}. {item.progress()} episodes watched so far.")
        else:
            print(f"S{season}E{episode} was already marked as watched.")
    else:
        if item.mark_watched():
            print(f"Marked {item.title} as watched.")
        else:
            print(f"{item.title} was already watched.")


def search_titles(library):
    text = input("Search for: ")
    print_titles(library.search(text), "No matches.")


def filter_titles(library):
    print("1. By genre\n2. Watchlist (unwatched)\n3. Top rated")
    choice = get_int("Filter: ", 1, 3)

    if choice is None:
        print("Invalid choice. Pick 1-3.")
    elif choice == 1:
        genre = input("Genre: ")
        print_titles(library.by_genre(genre), "No titles in that genre.")
    elif choice == 2:
        print_titles(library.watchlist(), "Nothing on your watchlist.")
    else:
        n = get_int("How many (1-100): ", 1, 100)
        if n is None:
            print("Invalid number.")
            return
        print_titles(library.top_rated(n), "Nothing rated yet.")


def show_stats(library):
    stats = library.stats()
    average = stats["average_rating"]

    print(f"Titles: {stats['total']}")
    print(f"Watched: {stats['watched']}")
    print(f"Average rating: {average if average is not None else 'no ratings yet'}")

    if not stats["genre_counts"]:
        print("Genres: none yet")
        return

    print(f"Most common genre: {stats['most_common_genre']}")
    print("Titles per genre:")
    by_count = sorted(stats["genre_counts"].items(), key=lambda pair: (-pair[1], pair[0]))
    for genre, count in by_count:
        print(f"  {genre}: {count}")


def remove_title(library):
    item = find_title(library)
    if item is None:
        return

    answer = input(f"Remove {item.title}? Are you sure? (y/n): ").strip().lower()
    if answer != "y":
        print("Nothing removed.")
        return

    library.remove(item.title)
    print(f"Removed {item.title}.")


# ---------- startup and main loop ----------

STARTUP_MESSAGES = {
    "new": "Starting a new library.",
    "corrupted": "Warning: library.json is damaged. Starting empty; saves will go to library_recovered.json.",
}

ACTIONS = {
    1: add_movie,
    2: add_series,
    3: rate_title,
    4: mark_watched,
    5: search_titles,
    6: filter_titles,
    7: show_stats,
    8: remove_title,
}


def main():
    library = MovieLibrary()
    status = library.load()

    if status == "loaded":
        print(f"Loaded {len(library.movies)} titles.")
    else:
        print(STARTUP_MESSAGES[status])

    while True:
        print(MENU)
        choice = get_int("Choose: ", 1, 9)

        if choice is None:
            print("Invalid choice. Pick 1-9.")
        elif choice == 9:
            count = library.save()
            print(f"Saved {count} titles to {library.path}. Goodbye!")
            break
        else:
            ACTIONS[choice](library)


if __name__ == "__main__":
    main()