"""Movies Extension: Get's movie ratings and info from omdb api"""

from albertv0 import *

import urllib3
import json
import os

__iid__ = "PythonInterface/v0.1"
__prettyname__ = "Movie"
__version__ = "0.1"
__trigger__ = "m "
__author__ = "Bharat Kalluri"
__dependencies__ = []

http = urllib3.PoolManager()


def _get_icon(icon_name):
    return os.path.dirname(__file__) + "/icons/{}.svg".format(icon_name)


def handleQuery(query):
    if query.isTriggered:
        if len(query.string.strip()) >= 3:
            if query.string.strip().startswith("id:"):
                mid = query.string.strip().replace("id: ", "")
                return movieInfo(mid)
            return searchMovies(query)
        else:
            return Item(
                id=__prettyname__,
                icon=_get_icon("movie"),
                text=__prettyname__,
                subtext="Type in the movie name",
                completion=query.rawString,
            )


def searchMovies(query):
    qurl = "http://www.omdbapi.com/?s={}&apikey=e389610c".format(query.string.strip())
    try:
        res = http.request("GET", qurl)
        data = json.loads(res.data)
    except:
        critical("No Internet!")
        return [
            Item(
                id=__prettyname__,
                icon=iconLookup("dialog-warning"),
                text="Is internet working?",
                subtext="We could not query, check your internet connection",
                completion=query.rawString,
            )
        ]

    itemArr = []
    if data["Response"] == "True":
        for movieItem in data["Search"]:
            temp_item = Item(
                id=__prettyname__,
                icon=_get_icon("movie"),
                text="{}".format(movieItem["Title"]),
                subtext="{}".format(movieItem["Type"]),
                completion=__trigger__ + "id: " + movieItem["imdbID"],
            )
            itemArr.append(temp_item)

        return itemArr
    else:
        return Item(
            id=__prettyname__,
            icon=iconLookup("dialog-warning"),
            text="Too many results",
            subtext="Too many results returned, Please be specifics",
            completion=query.rawString,
        )


def movieInfo(mid):
    qurl = "http://www.omdbapi.com/?i={}&apikey=e389610c".format(mid)
    try:
        res = http.request("GET", qurl)
        data = json.loads(res.data)
    except:
        critical("No Internet!")
        return [
            Item(
                id=__prettyname__,
                icon=iconLookup("dialog-warning"),
                text="Is internet working?",
                subtext="We could not query, check your internet connection",
            )
        ]

    itemArr = []

    if data["Response"] == "True":
        # Append movie name
        itemArr.append(
            Item(
                id=__prettyname__,
                icon=_get_icon("movie"),
                text=data["Title"],
                subtext="Title",
            )
        )
        # Append movie genre
        itemArr.append(
            Item(
                id=__prettyname__,
                icon=_get_icon("genre"),
                text=data["Genre"],
                subtext="Genre",
            )
        )
        # Append director
        itemArr.append(
            Item(
                id=__prettyname__,
                icon=_get_icon("director"),
                text=data["Director"],
                subtext="Director",
            )
        )
        # Append Actors
        itemArr.append(
            Item(
                id=__prettyname__,
                icon=_get_icon("actors"),
                text=data["Actors"],
                subtext="Actors",
            )
        )
        # Append Plot
        itemArr.append(
            Item(
                id=__prettyname__,
                icon=_get_icon("plot"),
                text=data["Plot"],
                subtext="Plot",
            )
        )
        # Append Awards
        itemArr.append(
            Item(
                id=__prettyname__,
                icon=_get_icon("awards"),
                text=data["Awards"],
                subtext="Awards",
            )
        )
        # Append Metascore
        itemArr.append(
            Item(
                id=__prettyname__,
                icon=_get_icon("metacritic"),
                text=data["Metascore"],
                subtext="Metascore",
            )
        )
        # Append imdbRating
        imdb_url = "https://www.imdb.com/title/" + mid
        itemArr.append(
            Item(
                id=__prettyname__,
                icon=_get_icon("imdb"),
                text=data["imdbRating"],
                subtext="IMDB Rating, Click to open on IMDB",
                actions=[UrlAction("Open article on Wikipedia", imdb_url)],
            )
        )
        # TODO : Append Rotten tomatoes rating
        # Open on IMDB
        return itemArr
    else:
        critical("No Internet!")
        return [
            Item(
                id=__prettyname__,
                icon=iconLookup("dialog-warning"),
                text="Movie Not found",
                subtext="Movie does not exist in database",
            )
        ]

    return Item(id=__prettyname__, icon=iconLookup("dialog-warning"), text=str(mid))

