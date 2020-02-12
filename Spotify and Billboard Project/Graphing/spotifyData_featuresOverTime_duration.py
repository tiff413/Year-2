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

import datetime as dt

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

df_mean2 = df_mean[["year", "duration_ms"]]

# CREATE FIGURE
fig = go.FigureWidget()

# CREATE A LIST FOR R VALUES
rValues = []
pValues = []
stdErrors = []

# ADD SCATTER PLOT
x = df_mean2['year']
y = df_mean2['duration_ms']/(1000*60)
fig.add_trace(go.Scatter(
                    x = x,
                    y = y,
                    name = "duration",
                    mode = 'lines+markers',
                    opacity = 0.5,
                    marker=dict(
                        color = "#cc338b",
                        size = 4),
                    line = dict(
                        color = "#cc338b",
                        dash = 'dot',
                        width = 1.5)
                    ))

# FIND INDEX FOR YEAR 2010
ind = list(x).index(1990)

# SPLIT DATA INTO TWO SETS, BEFORE AND AFTER 2010
x1 = x.iloc[:ind]
y1 = y.iloc[:ind]

x2 = x.iloc[ind:]
y2 = y.iloc[ind:]

# CALCULATE REGRESSION LINE FOR DATA BEFORE 2010
mask1 = ~np.isnan(x1) & ~np.isnan(y1)
slope1, intercept1, r_value1, p_value1, std_err1 = \
    sc.stats.linregress(x1[mask1],y1[mask1])
line1 = slope1*x1+intercept1

# APPEND VALUES TO LISTS
rValues.append(r_value1) # APPEND R VALUE
pValues.append(p_value1)
stdErrors.append(std_err1)

# CALCULATE REGRESSION LINE FOR DATA AFTER 2010
mask2 = ~np.isnan(x2) & ~np.isnan(y2)
slope2, intercept2, r_value2, p_value2, std_err2 = \
    sc.stats.linregress(x2[mask2],y2[mask2])
line2 = slope2*x2+intercept2

# APPEND VALUES TO LISTS
rValues.append(r_value2)
pValues.append(p_value2)
stdErrors.append(std_err2)

# PLOT REGRESSION LINE FOR DATA BEFORE 2010
fig.add_trace(go.Scatter(
                    x = x1,
                    y = line1,
                    mode ='lines',
                    marker = go.Marker(),
                    line = dict(
                        color = "#cc338b",
                        width = 3),
                    name = "LR1"
                    ))

# PLOT REGRESSION LINE FOR DATA ATER 2010
fig.add_trace(go.Scatter(
                    x = x2,
                    y = line2,
                    mode ='lines',
                    marker = go.Marker(),
                    line = dict(
                        color = "#cc338b",
                        width = 3),
                    name = "LR2"
                    ))

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
            'text': "Average duration of Billboard Year End Hot 100 songs (1980-2019)",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
            },
    xaxis_title = "Year",
    yaxis_title = "Duration (min)",
    # font=dict(
    #     family="Courier New, monospace",
    #     size=18,
    #     color="#7f7f7f"
    # )
)

py.iplot(fig, filename='spotifyData_durationOverTime_2LRs')
fig.show()
