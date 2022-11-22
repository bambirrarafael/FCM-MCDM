import numpy as np
import plotly.express as px

import FCM
from FCM import make_scenario

estado_inicial = {
    'Áreas de terras alagadas': 0.5,
    "População de peixes": 0.5,
    "Poluição": 0.5,
    'sustento (receita)': 0.5,
    'Policiamento': 0.5
}

matriz_peso = np.array([
    [0,     1,    -0.1,     0.8,    0],
    [0,     0,      0,      1,      0],
    [-0.2,  -1,     0,      -0.2,   0],
    [0,     0,      0,      0,      0],
    [0.2,   0.5,    -0.5,   -0.2,   0]
])

df_cenario = make_scenario(matriz_peso, estado_inicial, 7)

FCM.plot_scenario(df_cenario)