<h2>Retrieving Billboard Hot 100 Data (webscrapeBillboard.py)</h2>

This program scrapes the Billboard music chart website and records the Hot 100 songs every week within a certain period.

The program uses Beautiful Soup for webscraping. The datetime module is also used to compare and iterate time, while the time module is used to delay the looping so that the IP address won’t be blocked.

Inputs | Outputs
-------| -------
* The date you want to start scraping from (start date)|For the 100 top Billboard songs per week: rank, date, song name, artist names, previous week rank, peak rank, total weeks on chart (written into CSV file)
The date you want to scrape until (end date) | 


<h2>Retrieving Spotify Data (scrapeSpotify.py)</h2>

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
  
*More details about data (morale, summarised method, explanation of Spotify audio features): https://musicandstreamingservices.github.io/data.html*
