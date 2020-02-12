import pandas as pd
# from plotly.offline import iplot
import cufflinks as cf
# import plotly as py
import plotly.express as px
import plotly.graph_objs as go
import numpy as np
import scipy as sc
import chart_studio
import chart_studio.plotly as py

# ACCESS PLOTLY AND CUFFLINKS OFFLINE
# py.offline.init_notebook_mode(connected=True)
# cf.go_offline()

# SET UP CHART STUDIO (FOR SAVING INTO PLOTLY ACCOUNT)
chart_studio.tools.set_credentials_file(username='thisistiff', api_key='yVDN4aKh02TaxSpm7o0L')

# READ SPOTIFY DATA
df_all = pd.read_csv("spotifyData_100perYr_final.csv")

# IF INSTRUMENTALNESS < 0.5, INSTRUMENTALNESS == 0, ELSE INSTRUMENTALNESS == 1
df_all.loc[df_all["instrumentalness"]<0.5, "instrumentalness"] = 0
df_all.loc[df_all["instrumentalness"]>=0.5, "instrumentalness"] = 1

# TAKE AVERAGES OF FEATURES FOR EVERY YEAR
df_mean = df_all.groupby('year').mean()
df_mean = df_mean.reset_index(drop=False)

# %% #==========================================================================
# PLOT FEATURES WITH VALUES BETWEEN 0 AND 1

df_mean2 = df_mean[[
        "year", "acousticness", "danceability", "energy", "instrumentalness",
        "speechiness", "valence"
        ]]

coloursBlock = ["#e6194B", "#f58231", "#808000", "#3cb44b",
                    "#469990", "#000075", "#911eb4"]

# CREATE FIGURE
fig = go.FigureWidget()

# CREATE A LIST FOR R VALUES
rValues = []
pValues = []
stdErrors = []

# ADD A TRACE FOR EVERY
for i in range(len(df_mean2.columns)-1):
# for i in range(1):
    x = df_mean2['year']
    y = df_mean2.iloc[:,i+1]

    # ADD SCATTER PLOT
    fig.add_trace(go.Scatter(
                        x = x,
                        y = y,
                        name = df_mean2.columns[i+1],
                        mode = 'lines+markers',
                        opacity = 0.5,
                        marker=dict(
                            color = coloursBlock[i],
                            size = 4),
                        line = dict(
                            color = coloursBlock[i],
                            dash = 'dot',
                            width = 1.5)
                        ))

    # ADD REGRESSION LINE
    mask = ~np.isnan(x) & ~np.isnan(y)
    slope, intercept, r_value, p_value, std_err = \
        sc.stats.linregress(x[mask],y[mask])
    line = slope*x+intercept

    # APPEND VALUES TO LISTs
    rValues.append(r_value)
    pValues.append(p_value)
    stdErrors.append(std_err)

    fig.add_trace(go.Scatter(
                        x = x,
                        y = line,
                        mode ='lines',
                        marker = go.Marker(),
                        line = dict(
                            color = coloursBlock[i],
                            width = 3),
                        name = df_mean2.columns[i+1]+" LR"
                        ))

fig.update_layout(
    updatemenus=[
        go.layout.Updatemenu(
            # type="buttons",
            direction="down",
            active=0,
            x=1.2,
            y=1.1,

            buttons=list([
                dict(label="all",
                    method="update",
                    args=[{"visible": [True,True,True,True,True,True,
                                        True,True,True,True,True,True,
                                        True,True]}]),
                dict(label="acousticness",
                    method="update",
                    args=[{"visible": [True,True,False,False,False,False,
                                        False,False,False,False,False,False,
                                        False,False]}]),
                dict(label="danceability",
                     method="update",
                     args=[{"visible": [False,False,True,True,False,False,
                                        False,False,False,False,False,False,
                                        False,False]}]),
                dict(label="energy",
                    method="update",
                    args=[{"visible": [False,False,False,False,True,True,
                                        False,False,False,False,False,False,
                                        False,False]}]),
                dict(label="instrumentalness",
                    method="update",
                    args=[{"visible": [False,False,False,False,False,False,
                                        True,True,False,False,False,False,
                                        False,False]}]),
                dict(label="speechiness",
                    method="update",
                    args=[{"visible": [False,False,False,False,False,False,
                                        False,False,True,True,False,False,
                                        False,False]}]),
                dict(label="valence",
                    method="update",
                    args=[{"visible": [False,False,False,False,False,False,
                                        False,False,False,False,True,True,
                                        False,False]}])
            ]),
        )
    ])

# FORMAT GRAPH
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
    title = {
            'text': "Spotify audio features of Billboard Year End Hot 100 songs (1980-2019)",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
            },
    xaxis_title = "Year",
    yaxis_title = "Intensity (min=0, max=1)",
    # font=dict(
    #     family="Courier New, monospace",
    #     size=18,
    #     color="#7f7f7f"
    # )
)

py.iplot(fig, filename='spotifyData_featuresOverTime')
fig.show()
