import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx


def make_scenario(matriz_peso, dict_estado_inicial, T, lamb=3):
    n_var = len(dict_estado_inicial)
    colunas = []
    for var in dict_estado_inicial.keys():
        colunas.append([dict_estado_inicial[var]])
    for t in range(1, T):
        estado_anterior = []
        for var in range(n_var):
            estado_anterior.append(colunas[var][-1])
        for var in range(n_var):
            peso_coluna = matriz_peso[:, var]
            colunas[var].append(sigmoid(lamb, estado_anterior, peso_coluna))
    colunas = np.array(colunas)
    colunas = colunas.T
    df_colunas = pd.DataFrame(colunas, columns=dict_estado_inicial.keys())
    return df_colunas


def sigmoid(lamb, estado_anterior, pesos_coluna):
    return 1 / (1 + np.exp(-lamb * (np.array(estado_anterior) @ pesos_coluna)))


def plot_scenario(df_cenario):
    fig = px.line(df_cenario)
    fig.show()


def plot_matriz_pesos(matriz_peso):

    pass
