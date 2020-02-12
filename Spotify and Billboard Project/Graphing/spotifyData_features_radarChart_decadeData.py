import pandas as pd
# from plotly.offline import iplot
import cufflinks as cf
# import plotly as py
import plotly.graph_objs as go
import chart_studio
import chart_studio.plotly as py

# import numpy as np
# import scipy as sc
# import plotly.graph_objs as go

# py.offline.init_notebook_mode(connected=True)
# cf.go_offline()

# tls.set_credentials_file(username='pwLLzE4yloKrAseHMWeP')

df_all = pd.read_csv("spotifyData_billboardDecadeData_final.csv")

# IF INSTRUMENTALNESS < 0.5, INSTRUMENTALNESS == 0, ELSE INSTRUMENTALNESS == 1
df_all.loc[df_all["instrumentalness"]<0.5, "instrumentalness"] = 0
df_all.loc[df_all["instrumentalness"]>=0.5, "instrumentalness"] = 1

df_mean = df_all.groupby('decade').mean()
df_mean = df_mean.reset_index(drop=False)
df_mean2 = df_mean[[
            "acousticness", "danceability", "energy", "instrumentalness",
            "speechiness", "valence"
            ]]

#==========================================================================
# SET UP CHART STUDIO
chart_studio.tools.set_credentials_file(username='thisistiff', api_key='yVDN4aKh02TaxSpm7o0L')

#==========================================================================
cols = list(df_mean2.columns)

fig = go.FigureWidget()

for i in range(len(df_mean2)):
    vals = list(df_mean2.iloc[i,:].values)

    fig.add_trace(go.Scatterpolar(
                        visible = False,
                        r = vals,
                        theta = cols,
                        fill = 'toself',
                        name = str(df_mean["decade"][i])
                        ))

fig.data[0].visible = True

# CREATE AND ADD SLIDERS
steps = []
for i in range(len(fig.data)):
    step = dict(
        method="restyle",
        args=["visible", [False] * len(fig.data)],
        label=str(df_mean["decade"][i])+"'s"
    )
    step["args"][1][i] = True  # Toggle i'th trace to "visible"
    steps.append(step)

sliders = [dict(
    active=0,
    currentvalue={"prefix": "Decade: "},
    pad={"t": 40},
    steps=steps
)]

fig.update_layout(
    title = {
           'text': "Spotify audio features of Billboard Hot 100 songs (per decade)",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
            },
    sliders=sliders,
    polar=dict(
        radialaxis=dict(
          visible=True,
          range=[0, 0.8]
        )),
    showlegend=False
)

py.iplot(fig, filename='spotifyData_features_radarChart_decadeData')
fig.show()
