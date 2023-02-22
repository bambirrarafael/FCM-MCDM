import numpy as np
import pandas as pd
from FCM import make_scenario_CNFCM, plot_scenario, make_scenario


estado_inicial = {
                    'C1': 0.1,
                    "C2": 0.1,
                    "C3": 0.1,
                    'C4': 0.1,
                    'C5': 0.1,
                    'C6': 0.1,
                    'C7': 0.1,
                    'C8': 0.1,
                    "C9": 0.1,
                    "C10": 0.1,
                    'C11': 0.1,
                    'C12': 0.1,
                    'C13': 0.1,
                    'C14': 0.1,
                    'C15': 0,
                    'C16': 0,
                    'C17': 0,
                }

matriz_pesos = np.array(
    [
        [0, 0, 0.812, 0, 0, 0, 0, 0, 0, 0, 0, -0.875, 0, 0, 0, 0, 0],
        [0.937, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0.625, 0.875, 0.562, 0.75, 0, 0, 0.385, 0, 0, 0, 0, 0, 0, 0],
        [-0.875, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0.875, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [-0.375, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [-0.125, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0.188, -0.063, 0, 0.937, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0.812, -0.687, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0.75, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.75, 0, 0, 0, 0, 0],
        [0, -0.375, 0, 0, -0.625, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0.812, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, -0.5, 0, 0, -0.25, 0, 0, 0, 0, 0, 0, -0.687, 0, 0, 0, 0, 0],
        [0.063, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0.063, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0.188, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0.125, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
)



df_cenario = make_scenario_CNFCM(matriz_pesos, estado_inicial, 120, n_var=17, d_i=0.3)
plot_scenario(df_cenario)
print(matriz_pesos)
