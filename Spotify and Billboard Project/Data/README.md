<h2>Retrieving Billboard Hot 100 Data</h2>
[webscrapeBillboard.py](webscrapeBillboard.py)


This program scrapes the Billboard music chart website and records the Hot 100 songs every week within a certain period.

**Inputs** 
* The date you want to start scraping from (start date)
* The date you want to scrape until (end date)

**Outputs**
* For the 100 top Billboard songs per week: 
  * rank, date, song name, artist names, previous week rank, peak rank, total weeks on chart (written into CSV file)

<h2>Retrieving Spotify Data</h2>
[scrapeSpotify.py](scrapeSpotify.py)

Two datasets were obtained from the program:
1. Spotify audio features of the Year End Hot 100 Billboard songs (per year)
2. Spotify audio features of every Hot 100 Billboard song (per decade)

**Inputs**
* Spotify user URI
* Key phrase (if the key is in the playlist name, the playlist will be scraped)

**Outputs**
* Song name and song URI
* Artist name and artist URI
* Song features:
  * acousticness, danceability, energy, instrumentalness, liveness, loudness, speechiness, tempo, valence, duration_ms, mode, key, time_signature, popularity
  
*For more details about data (morale, summarised method, explanation of Spotify audio features): https://musicandstreamingservices.github.io/data.html*
