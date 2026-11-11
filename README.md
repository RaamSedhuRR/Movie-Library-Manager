# Movie Library Manager

A command-line app for managing a personal library of movies and series: add titles, rate them, track what you've watched (down to individual episodes), search and filter, see statistics, and keep everything saved between runs in a JSON file.

Built in plain Python with no external packages, as the capstone project for the Python fundamentals phase of my AI/ML engineering roadmap.

## Features

- Add movies and series; titles are case-insensitive, so `Inception` and `inception` are the same title
- Rate titles from 1 to 10 (rating a title marks it as watched)
- Mark movies as watched, or track individual episodes of a series
- Search by title, filter by genre, see your watchlist (oldest first) and your top-rated titles
- Statistics: totals, average rating, titles per genre and the most common genre
- Saves to `library.json` on exit and loads it on start
- A damaged save file is never overwritten: the app warns you and saves to `library_recovered.json` instead
- Invalid input never crashes the app

## Running it

Requires Python 3.10 or newer.

```bash
python main.py
```

## Running the tests

```bash
python tests.py
```

The test suite covers all five layers of the project, from the `Movie` class to saving and loading, and ends with a summary line such as `79 passed, 0 failed`.

## Project structure

| File | Contents |
| --- | --- |
| `Movie.py` | `Movie` class: genres, rating, watched status, conversion to a dict |
| `Series.py` | `Series(Movie)`: seasons and watched episodes |
| `MovieLibrary.py` | `MovieLibrary` class (add, search, filters, stats, save, load) and `from_dict` |
| `main.py` | The interactive menu; the only file that reads input or prints |
| `tests.py` | Automated tests with PASS/FAIL output |

## Design notes

- **Data and display are separate.** Classes return values; only `main.py` prints.
- **Nothing derived is stored.** Averages, counts and episode progress are calculated on demand, so they can never go stale.
- **Inheritance over duplication.** `Series` reuses `Movie` through `super()`, and the library treats both through one interface.
- **Validate before changing anything.** Every method rejects bad input before modifying data.
