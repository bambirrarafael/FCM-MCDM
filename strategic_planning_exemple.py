import numpy as np
import pandas as pd
from FCM import make_scenario_CNFCM, plot_scenario


estado_inicial = {
                    'C1': 0.1,
                    "C2": 0.1,
                    "C3": 0.1,
                    'C4': 0.1,
                    'C5': 0.1,
                    'C6': 0.1,
                    'C7': 0.1
                }

matriz_pesos = np.array(
    [
        [0,     0.9,    -0.4,   0,      -0.5,   0,      0],
        [0,     0,      0.7,    0.8,    0,      -0.7,   0],
        [0,     0,      0,      0,      -0.2,   0.8,    0],
        [0,     0.2,    0.7,    0,      0,      0,      0.9],
        [0,     0,      -0.4,      0,      0,      0.8,    0],
        [0.9,   0,      -0.3,   0,      0,      0,      0],
        [0,     0,      0,      -0.3,   0.7,    0,      0]
    ]
)

df_cenario = make_scenario_CNFCM(matriz_pesos, estado_inicial, 80, n_var=7, d_i=0.5)
plot_scenario(df_cenario)
print(matriz_pesos)
