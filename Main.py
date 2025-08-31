import re
from plexapi.server import PlexServer
from flask import Flask, Response, redirect, url_for

# ---- Plex setup ----
baseurl = '*******'
token = '*******'
plex = PlexServer(baseurl, token)

# Library Information
movies = plex.library.section('Movies')
tv = plex.library.section('TV Shows')

allMovies = movies.all()
allTVShows = tv.all()

# return all movies using plex native api - UGLY
def returnAllMovies():
    return allMovies

# returns all tv shows using plex native api - UGLY
def returnAllTvShows():
    return allTVShows

# Parses movies into a more appealing list
def returnParsedMovieTitles():
    parsed = [t.replace('-', ' ') for t in re.findall(r'<Movie:\d+:([^>]+)>', str(allMovies))]
    return parsed

# parses TV Titles into a more appealing list
def returnParsedTVTitles():
    parsed = [t.replace('-', ' ') for t in re.findall(r'<Show:\d+:([^>]+)>', str(allTVShows))]
    return parsed

# Media Statistics
def totalMovies():
    countMovies = len(allMovies)
    return countMovies

def totalTVShows():
    countTVShows = len(allTVShows)
    return countTVShows

# ---- Flask app ----
app = Flask(__name__)

@app.get("/")
def index():
    return redirect(url_for("widget"))

# The widget page
@app.get("/widget")
def widget():
    movies_count = totalMovies()
    tv_count     = totalTVShows()
    movies       = returnParsedMovieTitles()[:20]
    shows        = returnParsedTVTitles()[:20]

    html = (
        "<!doctype html><html><head>"
        "<meta charset='utf-8'/>"
        "<meta name='viewport' content='width=device-width, initial-scale=1'/>"
        "<meta http-equiv='refresh' content='300'/>"
        "<title>Plex Snapshot</title>"
        "</head>"
        "<body style='font:13px system-ui;margin:6px;background:#0b0e12;color:#e7eef7;'>"
          "<div style='width:100%;max-width:420px'>"
            "<div style='display:flex;justify-content:space-between;align-items:center;margin:0 0 6px'>"
              "<strong>Plex Snapshot</strong>"
              "<span style='font-size:11px;opacity:.7'>auto-refresh 5m</span>"
            "</div>"
            f"<div style='margin:0 0 10px'>Movies: <b>{movies_count}</b> &nbsp;•&nbsp; TV Shows: <b>{tv_count}</b></div>"

            "<div style='background:rgba(255,255,255,.06);padding:10px;border-radius:10px;margin-bottom:10px;'>"
              "<div style='font-weight:600;margin:0 0 6px'>Movies (top 20)</div>"
              "<ul style='margin:0;padding-left:16px;max-height:150px;overflow:auto'>"
                + "".join(f"<li>{t}</li>" for t in movies) +
              "</ul>"
            "</div>"

            "<div style='background:rgba(255,255,255,.06);padding:10px;border-radius:10px;'>"
              "<div style='font-weight:600;margin:0 0 6px'>TV Shows (top 20)</div>"
              "<ul style='margin:0;padding-left:16px;max-height:150px;overflow:auto'>"
                + "".join(f"<li>{t}</li>" for t in shows) +
              "</ul>"
            "</div>"
          "</div>"
        "</body></html>"
    )
    return Response(html, mimetype="text/html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=999)
