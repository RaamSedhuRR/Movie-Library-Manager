"""Tests for the Movie Library Manager. Run with:  python tests.py"""

import json
import os

from Movie import Movie
from Series import Series
from MovieLibrary import MovieLibrary, from_dict


results = {"passed": 0, "failed": 0}


def check(label, actual, expected):
    """Compare actual with expected and print PASS or FAIL with the difference."""
    if actual == expected:
        results["passed"] += 1
        print(f"PASS  {label}")
    else:
        results["failed"] += 1
        print(f"FAIL  {label}")
        print(f"      expected: {expected!r}")
        print(f"      got:      {actual!r}")


def titles(items):
    return [item.title for item in items]


def round_trip(item):
    """object -> dict -> JSON text -> dict -> object, as saving and loading do."""
    return from_dict(json.loads(json.dumps(item.to_dict())))


# ---------------- Milestone 1: Movie ----------------

def test_movie():
    print("\n--- Movie ---")
    check("genres are cleaned", Movie("T", 2000, " Sci-Fi , thriller,, ").genres, {"sci-fi", "thriller"})

    m = Movie("Inception", 2010, "sci-fi, thriller")
    check("__str__ when new", str(m), "Inception (2010) [sci-fi, thriller] not rated unwatched")
    check("rate(11) rejected", m.rate(11), False)
    check("rate(0) rejected", m.rate(0), False)
    check("nothing changed after rejections", (m.rating, m.watched), (None, False))
    check("rate(8) accepted", m.rate(8), True)
    check("rating also marks watched", (m.rating, m.watched), (8, True))
    check("re-rating allowed", m.rate(9), True)
    check("__str__ when rated", str(m), "Inception (2010) [sci-fi, thriller] 9/10 watched")
    check("mark_watched when already watched", m.mark_watched(), False)
    check("mark_watched on a fresh movie", Movie("F", 2020, "drama").mark_watched(), True)
    check("genres are a set, not text", "fi" in m.genres, False)


# ---------------- Milestone 2: Series ----------------

def test_series():
    print("\n--- Series ---")
    dark = Series("Dark", 2017, " Mystery, Sci-Fi ", 2)
    check("inherited genre cleaning", dark.genres, {"mystery", "sci-fi"})
    check("starts with no episodes", dark.episodes_watched, [])
    check("progress starts at 0", dark.progress(), 0)
    check("__str__", str(dark), "Dark (2017) [mystery, sci-fi] not rated unwatched, 2 seasons, 0 episodes watched")

    check("season too high", dark.watch_episode(3, 1), False)
    check("episode 0", dark.watch_episode(1, 0), False)
    check("season 0", dark.watch_episode(0, 1), False)
    check("valid episode", dark.watch_episode(1, 1), True)
    check("duplicate episode", dark.watch_episode(1, 1), False)
    check("last season is valid", dark.watch_episode(2, 1), True)
    check("episodes are tuples", dark.episodes_watched, [(1, 1), (2, 1)])
    check("progress counts episodes", dark.progress(), 2)

    solo = Series("Solo", 2020, "drama", 1)
    check("1 season (singular)", str(solo), "Solo (2020) [drama] not rated unwatched, 1 season, 0 episodes watched")
    check("each series has its own list", solo.episodes_watched, [])

    s = Series("S", 2020, "drama", 1)
    s.watch_episode(1, 1)
    s.watch_episode(1, 2)
    s.watch_episode(1, 3)
    check("progress with many episodes in one season", s.progress(), 3)


# ---------------- Milestone 3: library basics ----------------

def test_library_basics():
    print("\n--- Library basics ---")
    lib = MovieLibrary()
    inception = Movie("Inception", 2010, "sci-fi, thriller")
    interstellar = Movie("Interstellar", 2014, "sci-fi, drama")
    dark = Series("Dark", 2017, "mystery", 3)

    check("add", lib.add(inception), True)
    check("add", lib.add(interstellar), True)
    check("add series", lib.add(dark), True)
    check("duplicate in another case", lib.add(Movie("inception", 1999, "drama")), False)
    check("duplicate with spaces", lib.add(Movie("  Interstellar ", 2014, "sci-fi")), False)
    check("non-movie rejected", lib.add("not a movie"), False)
    check("count", len(lib.movies), 3)

    check("get ignores case", lib.get("INCEPTION") is inception, True)
    check("get ignores spaces", lib.get("  dark  ") is dark, True)
    check("get unknown", lib.get("Avatar"), None)

    check("search sorted by title", titles(lib.search("IN")), ["Inception", "Interstellar"])
    check("search sorted by title", titles(lib.search("ar")), ["Dark", "Interstellar"])
    check("search no match", lib.search("zzz"), [])

    check("remove", lib.remove("DARK"), True)
    check("remove again", lib.remove("dark"), False)
    check("count after remove", len(lib.movies), 2)


# ---------------- Milestone 4: queries and stats ----------------

def make_query_library():
    lib = MovieLibrary()
    lib.add(Movie("Inception", 2010, "sci-fi, thriller"))
    lib.add(Movie("Interstellar", 2014, "sci-fi, drama"))
    lib.add(Movie("Arrival", 2016, "sci-fi, drama"))
    lib.add(Series("Dark", 2017, "mystery, sci-fi", 3))
    lib.add(Movie("Parasite", 2019, "thriller, drama"))
    lib.add(Movie("Memento", 2000, "thriller, mystery"))
    return lib


def test_queries_and_stats():
    print("\n--- Queries and stats ---")
    lib = make_query_library()

    check("by_genre", titles(lib.by_genre("SCI-FI")), ["Arrival", "Dark", "Inception", "Interstellar"])
    check("by_genre strips", titles(lib.by_genre(" drama ")), ["Arrival", "Interstellar", "Parasite"])
    check("by_genre no match", lib.by_genre("comedy"), [])
    check("watchlist oldest first",
          titles(lib.watchlist()),
          ["Memento", "Inception", "Interstellar", "Arrival", "Dark", "Parasite"])

    lib.get("inception").rate(9)
    lib.get("interstellar").rate(7)
    lib.get("arrival").rate(9)
    lib.get("memento").mark_watched()

    check("watchlist after watching", titles(lib.watchlist()), ["Dark", "Parasite"])
    check("top_rated tie A to Z", titles(lib.top_rated(2)), ["Arrival", "Inception"])
    check("top_rated skips unrated", titles(lib.top_rated(10)), ["Arrival", "Inception", "Interstellar"])
    check("top_rated(0)", lib.top_rated(0), [])
    check("top_rated(-1)", lib.top_rated(-1), [])

    s = lib.stats()
    check("stats total", s["total"], 6)
    check("stats watched", s["watched"], 4)
    check("stats average (rounded)", s["average_rating"], 8.3)
    check("stats genre counts", s["genre_counts"], {"sci-fi": 4, "thriller": 3, "drama": 3, "mystery": 2})
    check("stats most common", s["most_common_genre"], "sci-fi")
    check("stats genres", s["genres"], {"drama", "mystery", "sci-fi", "thriller"})

    lib.get("parasite").rate(5)
    s = lib.stats()
    check("average updates by itself", s["average_rating"], 7.5)
    check("watched updates by itself", s["watched"], 5)

    e = MovieLibrary().stats()
    check("empty library: no crash",
          (e["total"], e["watched"], e["average_rating"], e["most_common_genre"], e["genre_counts"], e["genres"]),
          (0, 0, None, None, {}, set()))

    tie = MovieLibrary()
    tie.add(Movie("A", 2000, "drama"))
    tie.add(Movie("B", 2001, "comedy"))
    check("genre tie is alphabetical", tie.stats()["most_common_genre"], "comedy")


# ---------------- Milestone 5: save and load ----------------

def test_persistence():
    print("\n--- Save and load ---")
    m = Movie("Inception", 2010, " Thriller, Sci-Fi ")
    m.rate(9)
    check("movie to_dict", m.to_dict(),
          {"type": "movie", "title": "Inception", "year": 2010,
           "genres": ["sci-fi", "thriller"], "rating": 9, "watched": True})

    d = Series("Dark", 2017, "Mystery, Sci-Fi", 3)
    d.watch_episode(1, 1)
    d.watch_episode(1, 2)
    d.rate(8)
    check("series to_dict type", d.to_dict()["type"], "series")

    copy = round_trip(d)
    check("round trip keeps the class", type(copy).__name__, "Series")
    check("round trip restores tuples", copy.episodes_watched, [(1, 1), (1, 2)])
    check("round trip loses nothing", copy.to_dict(), d.to_dict())
    check("round trip makes a new object", copy is d, False)

    fresh = Movie("Memento", 2000, "thriller")
    check("unrated movie survives", round_trip(fresh).to_dict(), fresh.to_dict())
    check("unknown type skipped", from_dict({"type": "podcast", "title": "X"}), None)

    lib = MovieLibrary("test_library.json")
    lib.add(m)
    lib.add(d)
    check("save returns count", lib.save(), 2)

    loaded = MovieLibrary("test_library.json")
    check("load normal file", loaded.load(), "loaded")
    check("everything came back",
          [x.to_dict() for x in loaded.movies.values()],
          [x.to_dict() for x in lib.movies.values()])

    if os.path.exists("does_not_exist.json"):
        os.remove("does_not_exist.json")
    missing = MovieLibrary("does_not_exist.json")
    check("missing file", missing.load(), "new")
    check("missing file leaves library empty", len(missing.movies), 0)

    with open("broken.json", "w") as f:
        f.write("{ this is not json")
    broken = MovieLibrary("broken.json")
    check("corrupted file", broken.load(), "corrupted")
    check("saves are redirected", broken.path, "library_recovered.json")
    broken.add(Movie("New", 2020, "drama"))
    check("save to recovery file", broken.save(), 1)
    with open("broken.json") as f:
        check("damaged file untouched", f.read(), "{ this is not json")

    for name in ("test_library.json", "broken.json"):
        os.remove(name)


if __name__ == "__main__":
    test_movie()
    test_series()
    test_library_basics()
    test_queries_and_stats()
    test_persistence()
    print(f"\n{results['passed']} passed, {results['failed']} failed")