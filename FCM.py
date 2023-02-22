import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx


def make_scenario(matriz_peso, dict_estado_inicial, T, n_var, lamb=3, dict_variaveis_fixas=None):
    colunas = []
    for var in dict_estado_inicial.keys():
        colunas.append([dict_estado_inicial[var]])
    for t in range(1, T):
        estado_anterior = []
        for var in range(n_var):
            estado_anterior.append(colunas[var][-1])
        if t > 1:
            estado_anterior= ajustar_variaveis_fixas_no_estado_anterior(dict_variaveis_fixas, dict_estado_inicial, estado_anterior)
        for var in range(n_var):
            peso_coluna = matriz_peso[:, var]
            colunas[var].append(sigmoid(lamb, estado_anterior, peso_coluna))

    colunas = np.array(colunas)
    colunas = colunas.T
    colunas = ajustar_variaveis_fixas_nas_colunas(dict_variaveis_fixas, dict_estado_inicial, colunas, T)
    df_colunas = pd.DataFrame(colunas, columns=dict_estado_inicial.keys())
    return df_colunas


def ajustar_variaveis_fixas_no_estado_anterior(variaveis_fixas, dict_estado_inicial, estado_anterior):
    if variaveis_fixas is not None:
        list_keys_variaveis_fixas = list(variaveis_fixas.keys())
        list_keys_estado_inicial = list(dict_estado_inicial.keys())
        for fixed_var in list_keys_variaveis_fixas:
            i = list_keys_estado_inicial.index(fixed_var)
            estado_anterior[i] = variaveis_fixas[fixed_var]
    return estado_anterior


def ajustar_variaveis_fixas_nas_colunas(variaveis_fixas, dict_estado_inicial, colunas, T):
    if variaveis_fixas is not None:
        for t in range(1, T):
            estado_anterior = colunas[t, :]
            colunas[t, :] = ajustar_variaveis_fixas_no_estado_anterior(variaveis_fixas, dict_estado_inicial, estado_anterior)
    return colunas



def make_scenario_CNFCM(matriz_peso, dict_estado_inicial, T, n_var, d_i=0, variaveis_fixas=None):
    colunas = []
    for var in dict_estado_inicial.keys():
        colunas.append([dict_estado_inicial[var]])
    for t in range(1, T):
        estado_anterior = []
        for var in range(n_var):
            estado_anterior.append(colunas[var][-1])
        for var in range(n_var):
            peso_coluna = matriz_peso[:, var]
            colunas[var].append(certainty_neuron_fcm(estado_anterior, peso_coluna, var, d_i))
    colunas = np.array(colunas)
    colunas = colunas.T
    df_colunas = pd.DataFrame(colunas, columns=dict_estado_inicial.keys())
    return df_colunas


# def make_scenario_fixed_variables(matriz_peso, dict_estado_inicial, T, n_var, lamb=3, variaveis_fixas=None):
#     colunas = []
#     for var in dict_estado_inicial.keys():
#         colunas.append([dict_estado_inicial[var]])
#     for t in range(1, T):
#         estado_anterior = []
#         for var in range(n_var):
#             estado_anterior.append(colunas[var][-1])
#         for var in range(n_var):
#             peso_coluna = matriz_peso[:, var]
#             colunas[var].append(sigmoid(lamb, estado_anterior, peso_coluna))
#     colunas = np.array(colunas)
#     colunas = colunas.T
#     df_colunas = pd.DataFrame(colunas, columns=dict_estado_inicial.keys())
#     return df_colunas


def certainty_neuron_fcm(estado_anterior, pesos_coluna, var, d_i=0):
    s_i = np.array(estado_anterior) @ pesos_coluna
    a_i = estado_anterior[var]
    if a_i >= 0 and s_i >= 0:
        f_m = a_i + s_i - s_i*a_i
    elif a_i < 0 and s_i < 0 and abs(a_i) <= 1 and abs(s_i) <= 1:
        f_m = a_i + s_i + s_i*a_i
    else:
        f_m = (a_i + s_i) / (1 - np.min([abs(a_i), abs(s_i)]))
    result = f_m - d_i * a_i
    if result > 1:
        result = 1
    elif result < -1:
        result = -1
    return result


def sigmoid(lamb, estado_anterior, pesos_coluna):
    return 1 / (1 + np.exp(-lamb * (np.array(estado_anterior) @ pesos_coluna)))


def plot_scenario(df_cenario, title=None):
    fig = px.line(df_cenario, title=title)
    fig.show()


def plot_matriz_pesos(matriz_peso):

    pass
