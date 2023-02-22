import numpy as np
import pandas as pd
import plotly.graph_objects as go

anos = [
    2023,
    2024,
    2025,
    2026,
    2027,
    2028,
    2029,
    2030,
    2031,
    2032,
    2033,
    2034,
    2035,
    2036,
    2037
]

geracao_hidro = np.array([
    59.65,
    59.65,
    59.65,
    59.65,
    59.65,
    59.65,
    64.07,
    64.07,
    64.07,
    102.47,
    102.47,
    102.47,
    102.47,
    124.45,
    124.45
])


geracao_solar = np.array([
    4,
    4,
    4,
    4,
    4,
    4,
    4,
    4,
    4,
    4,
    4,
    4,
    4,
    4,
    4
])

carga_atual = np.array([
    219.01,
    219.01,
    219.01,
    219.01,
    219.01,
    219.01,
    219.01,
    219.01,
    219.01,
    219.01,
    219.01,
    219.01,
    219.01,
    219.01,
    219.01
])

carga_expansao = np.array([
    0.00,
    0.00,
    0.00,
    15.00,
    15.00,
    15.00,
    15.00,
    15.00,
    21.00,
    21.00,
    21.00,
    21.00,
    21.00,
    21.00,
    21.00
])

compras = np.array([
    250.20,
    176.75,
    156.75,
    156.75,
    156.75,
    156.75,
    113.89,
    113.89,
    113.89,
    109.35,
    96.58,
    96.58,
    96.58,
    92.08,
    92.08
])

vendas = np.array([
    104.00,
    42.00,
    42.00,
    0.00,
    0.00,
    0.00,
    0.00,
    0.00,
    0.00,
    0.00,
    0.00,
    0.00,
    0.00,
    0.00,
    0.00
])

preco_compras = np.array([
    199.36,
    196.54,
    191.49,
    191.49,
    191.49,
    191.49,
    164.63,
    164.63,
    164.63,
    162.75,
    160.24,
    160.24,
    160.24,
    155.30,
    155.30
])

preco_vendas = np.array([
    213.39,
    210.41,
    210.41,
    0.00,
    0.00,
    0.00,
    0.00,
    0.00,
    0.00,
    0.00,
    0.00,
    0.00,
    0.00,
    0.00,
    0.00
])

geracao_total = geracao_hidro + geracao_solar
carga_total = carga_atual + carga_expansao
recursos = geracao_total + compras
requisitos = carga_total + vendas
exposicao = geracao_total + compras - carga_total - vendas

fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=anos,
        y=geracao_total,
        mode='lines',
        name='Geração total'
    ))
fig.add_trace(
    go.Scatter(
        x=anos,
        y=compras,
        mode='lines',
        name='Compras'
    ))
fig.add_trace(
    go.Scatter(
        x=anos,
        y=carga_total,
        mode='lines',
        name='Carga total'
    ))
fig.add_trace(
    go.Scatter(
        x=anos,
        y=vendas,
        mode='lines',
        name='Vendas'
    ))
fig.add_trace(
    go.Bar(
        x=anos,
        y=exposicao,
        name='Exposição'
    ))
fig.show()




fig2 = go.Figure()
fig2.add_trace(
    go.Scatter(
        x=anos,
        y=recursos,
        mode='lines',
        name='Recursos'
    ))
fig2.add_trace(
    go.Scatter(
        x=anos,
        y=requisitos,
        mode='lines',
        name='Requisitos'
    ))
fig2.add_trace(
    go.Bar(
        x=anos,
        y=exposicao,
        name='Exposição'
    ))
fig2.show()
