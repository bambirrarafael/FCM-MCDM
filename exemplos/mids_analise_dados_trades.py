import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_excel('D:/Programas/Doutorado/FCM-MCDM/dados/avaliacao.xlsx')
df_win = df[df['Ativo'] == 'WINJ23']
df_ind = df[df['Ativo'] == 'INDJ23']

#
serie_resultados = df['Lucro'].cumsum()
serie_resultados_win = df_win['Lucro'].cumsum()
#
fig = px.line(serie_resultados)
fig.update_layout(title='resultados dos ultimos 2 dias')
fig.show()
fig = px.line(serie_resultados_win)
fig.update_layout(title='resultados no mini índice')
fig.show()
#
fig = go.Figure()
fig.add_trace(go.Histogram(x=df_win['Lucro'][df_win['alvo'] == 20], name='alvo_20_pts'))
fig.add_trace(go.Histogram(x=df_win['Lucro'][df_win['alvo'] == 25], name='alvo_25_pts'))
fig.update_layout(barmode='overlay')
fig.update_traces(opacity=0.6)
fig.update_layout(title='WINJ23')
fig.show()
#
fig = go.Figure()
fig.add_trace(go.Scatter(x=df_win['Volume'][df_win['alvo']==20], y=df_win['Lucro'][df_win['alvo']==20], name='alvo_20', mode='markers'))
fig.add_trace(go.Scatter(x=df_win['Volume'][df_win['alvo']==25], y=df_win['Lucro'][df_win['alvo']==25], name='alvo_25', mode='markers'))
fig.show()

n_amostras = df_win.count()['Lucro']
n_gain = df_win[df_win['Lucro'] > 0].count()['Lucro']
metrica_taxa_acerto = n_gain/n_amostras

df_win['Lucro'].replace(0, np.nan, inplace=True)
df_win = df_win[df_win['Lucro'].notna()]

n_amostras_nao_nulas = df_win.notnull().count()['Lucro']
metrica_porcentagem_operacoes_nulas = 1 - n_amostras_nao_nulas/n_amostras
metrica_taxa_acerto_sem_null = n_gain/n_amostras_nao_nulas

serie_alvo_20 = df_win['Lucro'][df_win['alvo'] == 20]
serie_alvo_25 = df_win['Lucro'][df_win['alvo'] == 25]
media_20 = serie_alvo_20.mean()
media_25 = serie_alvo_25.mean()

fig = go.Figure()
fig.add_trace(go.Histogram(x=df_win['Lucro'][df_win['alvo'] == 20], name='alvo_20_pts'))
fig.add_trace(go.Histogram(x=df_win['Lucro'][df_win['alvo'] == 25], name='alvo_25_pts'))
fig.add_vline(x=media_20, line_dash="dash", line_color="blue", annotation_text='20pts')
fig.add_vline(x=media_25, line_dash="dash", line_color="red", annotation=dict(text='25pts', yshift=-40))
fig.update_layout(barmode='overlay')
fig.update_traces(opacity=0.6)
fig.update_layout(title='WINJ23')
fig.show()

fig = go.Figure()
fig.add_trace(go.Scatter(x=df_win['Volume'][df_win['alvo']==20], y=df_win['Lucro'][df_win['alvo']==20], name='alvo_20', mode='markers'))
fig.add_trace(go.Scatter(x=df_win['Volume'][df_win['alvo']==25], y=df_win['Lucro'][df_win['alvo']==25], name='alvo_25', mode='markers'))
fig.show()

print("fim!")
