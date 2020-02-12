#===============================================================================
# PLOTTING THE LIFETIME OF SONGS ON THE BILLBOARD HOT 100 WITHIN A GIVEN PERIOD
#===============================================================================
#NOTE:  CHANGE PLOT DATES ON LINE 210 - 211
#       CHANGE PLOT X-AXIS RANGE ON LINE 291

import pandas as pd
import datetime as dt
import time
import cufflinks as cf
# import plotly as py
import plotly.graph_objs as go
import numpy as np
from itertools import repeat
from plotly.offline import init_notebook_mode, iplot
import plotly.io as pio
import dash_core_components as dcc
init_notebook_mode()
import chart_studio
import chart_studio.plotly as py
#===============================================================================
# CHOOSE RANKINGS
rankLow = 1
rankHigh = 1

#===============================================================================
# SET UP CHART STUDIO
chart_studio.tools.set_credentials_file(username='thisistiff', api_key='yVDN4aKh02TaxSpm7o0L')

#===============================================================================
# CREATE FUNCTION TO PLOT DATA FOR GIVEN YEAR
def plotbbdata(rankLow,rankHigh,startPeriod,endPeriod):

    # FUNCTION FOR CONVERTING TIME FROM STRING TO DATETIME
    def readTime(ti):
        read = (dt.datetime.strptime(ti, "%Y-%m-%d")).date()
        return read

    # READ DATA FROM CSV FILE
    allData = pd.read_csv("billboardData.csv")
    rankData = allData[(allData["rank"]>=rankLow) & (allData["rank"]<=rankHigh)]
    rankData = rankData.drop_duplicates(subset=["songName","artistName"])
    rankData = rankData.reset_index(drop=True)

    # SELECT DATA WITHIN THE GIVEN PERIOD
    for ind in range(0, int(len(rankData))):
        i = rankData.index.get_loc(ind)
        dateSearch = readTime(rankData.iloc[i]["date"])
        if readTime(startPeriod) <= dateSearch < readTime(endPeriod):
            continue
        else:
            rankData.drop(rankData.index[i], inplace=True)
    rankData = rankData.reset_index(drop=True)

    # PLOT ALL SONGS IN RANK DATA
    allycols=list(range(len(rankData)))
    ally=pd.DataFrame()
    allx=[]
    aglastx=[]
    traces=[]
    meanx=0
    for j in range(len(rankData)):
        chooseSong = rankData["songName"][j]
        chooseArtist = rankData["artistName"][j]

        # SEARCH DATA FOR SONG
        song = allData.loc[(allData["songName"]==chooseSong)
                            & (allData["artistName"]==chooseArtist)]

        # GET Y VALUES (SONG RANK)
        y = song["rank"].tolist()

        # GET X VALUES (DATE IN DATETIME FORMAT)
        songDate = song["date"].tolist()

        # FOR EVERY DATE, READ AS DATE TIME AND APPEND TO LIST
        x = []

        for i in range(len(songDate)):
            dateT = readTime(songDate[i])
            x.append(dateT)

        # NORMALIZE ALL DATA BY DATE RANKED
        xabs = [0]

        for i in range(len(songDate)-1):
            div=int((x[i+1]-x[i]).days/7)
            if div != 1:
                #print(x[i+1]-[i],x[i]-[i-1])
                xabs1=list(range(int(div)))
                a=int((x[i]-x[0]).days/7)
                xabs1=[str(z+a+1) for z in xabs1]
                xabs=xabs+xabs1
                for n in range(div-1):
                    y.insert(i+1,'Nan')

            else:
                xabs1 = str(int((x[i+1]-x[0]).days/7))
                xabs.append(xabs1)

        lastx=xabs[-1]
        aglastx.append(lastx)


        # AGGREGATE X
        allx.append(xabs)


        # CREATE ARRAY WITH ALL SONG RANKINGS (ally)
        colours = ["","","","",""]
        ydf=pd.DataFrame(y)
        ally=pd.concat([ally,ydf],axis=1)
        songtrace=(go.Scatter(
                            visible=False,
                            x= xabs,
                            y= y,
                            mode = 'lines',
                            name = chooseSong,
                            opacity=0.8,
                            line = dict(
                                color = "#f1b6da"
                                )
                            ))
        traces.append(songtrace)



    #GET SD AND MEAN OF EACH WEEK
    meany=[]
    ysd=[]
    for k in range(len(ally)):
        row=np.array(list(ally.iloc[k,:])).astype(np.float)
        mean=np.nanmean(row)
        sd=np.nanstd(row)
        meany.append(mean)
        ysd.append(sd)

    #FIND MAXIMUM AMOUNT OF WEEKS A SONG HAS BEEN ON THE CHARTS
    maxx=max(allx)

    #GET 1SD PLUS MEAN AND 1SD MINUS MEAN
    p1sd=np.add(meany,ysd)
    m1sd=np.subtract(meany,ysd)

    #LIMIT p1sd AND m1sd VALUES WITHIN 0 TO 100
    for m in range(len(m1sd)):
        if m1sd[m]<0:
            m1sd[m]=0

    for n in range(len(m1sd)):
        if p1sd[n]>100:
            p1sd[n]=100

    # IF EXISTS SPLICE AVERAGE AND SD PLOTS WHERE SD=0 (AFTER THIS POINT ONLY ONE SONG IS RANKED)
    if 0 in ysd:
        stop=ysd.index(0)
    else:
        stop=len(ysd)+1

    maxx1=maxx[:stop]
    m1sd1=m1sd[:stop]
    p1sd1=p1sd[:stop]
    meany1=meany[:stop]

    # PLOT AVERAGE AND SD
    avgtrace=(go.Scatter(
                            visible=False,
                            x= maxx1,
                            y= meany1,
                            mode = 'lines+markers',
                            name = 'Average per Week',
                            marker=dict(
                                color = "#276419",
                                size = 6),
                            line = dict(
                                color = "#276419",
                                width = 2.5)
                            ))
    traces.append(avgtrace)
    topsd=(go.Scatter(
                            visible=False,
                            x=maxx1,
                            y=m1sd1,
                            fill='tonexty',
                            fillcolor='rgba(184,225,134,0.4)',
                            line=dict(color='rgba(184,225,134,0.4)'),
                            showlegend=False,
                            name='1 Sd',))
    traces.append(topsd)
    botsd=(go.Scatter(
                            visible=False,
                            x=maxx1,
                            y=p1sd1,
                            fill='tonexty',
                            fillcolor='rgba(184,225,134,0.4)',
                            line=dict(color='rgba(184,225,134,0.4)'),
                            showlegend=False,
                            name='1 Sd',))
    traces.append(botsd)

    xabs2=np.array(aglastx).astype(np.float)
    meanx=np.nanmean(xabs2)
    meanxtrace=(go.Scatter(
                            visible=False,
                            x=[meanx,meanx],
                            y=[0,100],
                            mode = 'lines',
                            name ='Average Number of Weeks on Charts',
                            line = dict(
                                color = "#8e0152",
                                width = 2.5
                                )
                            ))
    traces.append(meanxtrace)

    #OUTPUT OF FUNCTION ARE TRACES ALL TURNED OFF
    return traces

#===============================================================================
# FUNCTION FOR CONVERTING TIME FROM STRING TO DATETIME
def readTime(ti):
        read = (dt.datetime.strptime(ti, "%Y-%m-%d")).date()
        return read
# FUNCTION FOR REREADING DATETIME
def rereadTime(ti):
    reread = str(ti)
    read = (dt.datetime.strptime(reread, "%Y-%m-%d")).date()
    return read

# INCREMENTS TIME BY A Year
def incrementTime(ti):
    return rereadTime(ti) + dt.timedelta(days=730)

#===============================================================================
# CHOOSE DATES TO GET PLOTS
startdate="1980-01-01"
enddate="2019-01-01"

#TURN DATES INTO DATE TIME
date=startdate
readenddate=readTime(enddate)

#PLOT FOR EACH YEAR
plots=[]
plotnum=[]
years=[str(readTime(date).year)]
while readTime(date)<readenddate:
    datep1=incrementTime(readTime(date))
    plot1=plotbbdata(1,1,str(date),str(datep1))
    plotnum1=len(plot1)
    plots=plots+plot1
    plotnum.append(plotnum1)
    date=str(incrementTime(readTime(date)))
    years.append(str(int(datep1.year)+1))
fig = go.Figure(plots)
nyears=len(plotnum)
steps=[]
count=0
#TURN ON PLOTS FOR SINGLE SLIDER
for i in range(nyears):
    # HIDE ALL TRACES (RESET EVERY YEAR)
    step = dict(
        method = 'restyle',
        args = ['visible', [False] * len(plots)],
        label=years[i],
    )
    #PROGRESSIVELY TURN ON EACH TRACE FOR SINGLE SLIDER
    if i>0:
        count=plotnum[i-1]+count
    for j in range(plotnum[i]):
        step['args'][1][j+count] = True

    # ADD STEP TO STEP LIST
    steps.append(step)

# MAKE FIRST SET VISIBLE
for traces in range(plotnum[0]):
    fig.data[traces].visible = True

#SETUP SLIDER AND PLOT LAYOUTS
sliders = [dict(
                x=0,
                y=-0.05,
                currentvalue= {
                'font': {'size': 20},
                'prefix': 'Year:',
                'visible': True,
                'xanchor': 'left'},
                steps = steps,
                ),]
fig.layout.sliders=sliders
fig.update_layout(
    autosize=False,
    width=1000,
    height=700,
    margin=go.layout.Margin(
        l=50,
        r=50,
        b=100,
        t=100,
        pad=4
        ),
    legend_orientation="h",
    legend=dict(x=0, y=-0.35),
    title = {
           'text': "<b>Lifetime of a Billboard no.1 song (1980-2019) (all plots, 2 yr increments ver.)</b>",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
            },
    xaxis_title = "Weeks on chart",
    yaxis_title = "Rank on Billboard Hot 100",
    xaxis_tickformat = '',
    # font=dict(
    #     family="Courier New, monospace",
    #     size=12,
    #     color="#7f7f7f"
    #  )
    )
#SET RANGES FOR PLOTS
fig.update_xaxes(range=[0, 70])
fig.update_yaxes(range=[0, 100])
fig.update_yaxes(autorange="reversed")
fig.update_layout(showlegend=False)
fig.show()

#PLOT ONTO BROWSER
pio.renderers.default = 'browser'
pio.show(fig)
py.iplot(fig, filename='spotifyData_lifeTimeOfNo1Songs')
