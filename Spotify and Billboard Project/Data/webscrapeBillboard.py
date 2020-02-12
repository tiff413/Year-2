#===============================================================================
# SCRAPE BILLBOARD WEBSITE FOR WEEKLY HOT 100 SONGS
#===============================================================================
#   INPUTS:
#       * çhoose start date
#       * choose end date
#   OUTPUTS (written into CSV file):
#       * data for weekly Hot 100 songs:
#           rank, date, song name, artist names, previous week rank,
#           peak rank, total weeks on chart
#===============================================================================
# 1.IMPORT MODULES

from bs4 import BeautifulSoup
import requests
import re
import numpy as np
import datetime as dt
import time
import csv
import os

#===============================================================================
# 2.CHOOSE INPUTS AND OUTPUTS

# CHOOSE TIME FRAME FOR BILLBOARD DATA
startDate = "2019-12-03"
endDate = "2020-01-01"
# endDate = str((dt.datetime.now()).date())

# CHOOSE CSV FILE TO SAVE DATA IN
fileName = "billboardData.csv"

#===============================================================================
# 3.DEFINE TIME FUNCTIONS

# CONVERTS TIME STR INTO DATETIME
def readTime(ti):
    read = (dt.datetime.strptime(ti, "%Y-%m-%d")).date()
    return read

# READS IN A DATETIME AND REFORMATS IT
def rereadTime(ti):
    reread = str(ti)
    read = (dt.datetime.strptime(reread, "%Y-%m-%d")).date()
    return read

# INCREMENTS TIME BY A WEEK
def incrementTime(ti):
    return (rereadTime(ti) + dt.timedelta(weeks=1))

#===============================================================================
# 4.DEFINE FUNCTION TO SCRAPE A BILLBOARD WEBPAGE

def scrape(date, fileName):
    # APPLY DATE TO URL
    url = ("https://www.billboard.com/charts/hot-100/"+str(date)).rstrip()
    # SCRAPE
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html,features="lxml")

    # FIND CHART DATA
    allData = soup.findAll("span", {"class": "chart-element__information"})

    # SET UP THE STRINGS FOR FINDING CLASSES
    songClass = "chart-element__information__song text--truncate color--primary"
    artistClass = "chart-element__information__artist text--truncate color--secondary"
    lastWeekRankClass = "chart-element__information__delta__text text--last"
    peakRankClass = "chart-element__information__delta__text text--peak"
    weeksOnChartClass = "chart-element__information__delta__text text--week"

    dateStr = str(date)

    # IF THERE IS VALID DATA FOR THE DATE
    if len(allData) > 0:
        # FOR ALL SONGS
        for i in range(0, len(allData)):
            # FIND SONG NAME AND ARTIST NAME
            songName = allData[i].find("span", {"class": songClass}).text
            artistName = allData[i].find("span", {"class": artistClass}).text

            # FIND LAST WEEK RANK AS AN INTEGER (TAKE AWAY LABELS)
            lastWeekRankStr = allData[i].find("span", {"class": lastWeekRankClass}).text
            lastWeekRankLi = re.findall('\d+', lastWeekRankStr)
            if len(lastWeekRankLi) > 0: lastWeekRank = int(lastWeekRankLi[0])
            else: lastWeekRank = np.nan # if last week rank doesn't exist, take np.nan

            # FIND PEAK RANK AS AN INTEGER (TAKE AWAY LABELS)
            peakRankStr = allData[i].find("span", {"class": peakRankClass}).text
            peakRank = int(re.findall('\d+', peakRankStr)[0])

            # FIND WEEKS ON CHART AS AN INTEGER(TAKE AWAY LABELS)
            weeksOnChartStr = allData[i].find("span", {"class": weeksOnChartClass}).text
            weeksOnChart = int(re.findall('\d+', weeksOnChartStr)[0])

            # APPEND SCRAPED DATA TO A ROW
            row = [
                i+1,                # rank
                dateStr,            # date
                songName,
                artistName,
                lastWeekRank,
                peakRank,
                weeksOnChart
                ]

            # WRITE ROW INTO CSV FILE
            with open(fileName, 'a') as writeFile:
                writer = csv.writer(writeFile)
                writer.writerow(row)

    # IF THERE IS NO VALID DATA, EXIT LOOP
    else:
        exit()

#===============================================================================
# 5.EXECUTE FUNCTIONS

# IF OUTPUT CSV FILE DOESN'T EXIST OR IS EMPTY, WRITE COLUMN NAMES INTO FILE
if not(os.path.exists(fileName)) or os.stat(fileName).st_size == 0:
    with open(fileName, 'a') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerow(["rank","date","songName","artistName","lastWeekRank",
                         "peakRank","weeksOnChart"])

# APPLY CONDITIONS FOR SCRAPING
scrapeFrom = readTime(startDate)
scrapeUntil = readTime(endDate)

# INITIALISE VARIABLE CALLED DATE
date = scrapeFrom
# WHILE DATE < END DATE, SCRAPE
while date < scrapeUntil:
    scrape(date, fileName)

    # WAIT FOR A WHILE
    time.sleep(abs(np.random.normal(5)))

    # INCREMENT DATE
    date = incrementTime(date)
