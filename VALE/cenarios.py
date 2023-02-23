import numpy as np
import pandas as pd
from FCM import make_scenario_CNFCM, plot_scenario, make_scenario



estado_inicial = {
                    'C1': 0.3,      # 270
                    "C2": 0.25,     # 67500
                    "C3": 0.5,      # 0%
                    'C4': 0.62,     # 0.5 %
                    'C5': 0.48,     # -1.2%
                    'C6': 0.8,      # 9%
                    'C7': 0.8,      # 6%
                    'C8': 0.25,     # baixo
                    "C9": 0.25,     # baixo
                    "C10": 0.6,     # 1%
                    'C11': 0.15,    # 4.6
                    'C12': 0.5,     # 0%
                    'C13': 0.3,     # 2.75
                    'C14': 0.7      # 2%
                }

matriz_pesos_cenario_base = np.array(
    [
        [0, 0, 0.812, 0, 0, 0, 0, 0, 0, 0, 0, -0.875, 0, 0],
        [0.937, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0.625, 0.875, 0.562, 0.75, 0, 0, 0.385, 0, 0, 0, 0],
        [-0.875, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0.875, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [-0.375, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [-0.125, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0.188, -0.063, 0, 0.937, 0, 0, 0, 0, 0],
        [0, 0, 0, 0.812, -0.687, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0.75, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.75, 0, 0],
        [0, -0.375, 0, 0, -0.625, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0.812, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, -0.5, 0, 0, -0.25, 0, 0, 0, 0, 0, 0, -0.687, 0, 0],
        [0.063, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
)

df_cenario_base = make_scenario(matriz_pesos_cenario_base, estado_inicial, 15, n_var=14)
plot_scenario(df_cenario_base, 'cenario_base')

dict_variaveis_fixas = {'C8': 0.0}
df_cenario_pouca_chuva = make_scenario(matriz_pesos_cenario_base, estado_inicial, 15, n_var=14, dict_variaveis_fixas=dict_variaveis_fixas)
plot_scenario(df_cenario_pouca_chuva, 'pouca_chuva')

dict_variaveis_fixas = {'C10': 1.0, 'C14': 1.0}
df_cenario_desenvolvimento_mundial = make_scenario(matriz_pesos_cenario_base, estado_inicial, 15, n_var=14, dict_variaveis_fixas=dict_variaveis_fixas)
plot_scenario(df_cenario_desenvolvimento_mundial, 'desenvolvimnto_mundial')

dict_variaveis_fixas = {'C6': 1.0, 'C7': 1.0}
df_cenario_incentivo_renovaveis = make_scenario(matriz_pesos_cenario_base, estado_inicial, 15, n_var=14, dict_variaveis_fixas=dict_variaveis_fixas)
plot_scenario(df_cenario_incentivo_renovaveis, 'incentivo_renovaveis')


dict_cenarios_preco = {
    'cenario_base': df_cenario_base['C1'],
    'pouca_chuva': df_cenario_pouca_chuva['C1'],
    'desenvolvimnto_mundial': df_cenario_desenvolvimento_mundial['C1'],
    'incentivo_renovaveis': df_cenario_incentivo_renovaveis['C1'],
}
df_preco = pd.DataFrame(dict_cenarios_preco)
plot_scenario(df_preco, 'Preços nos cenarios')

print('-------------- FIM da construção de cenários!')


def find_fuzzy_value(valor_real, lim_inf, lim_sup):
    return 1 - (lim_sup - valor_real)/(lim_sup - lim_inf)

def find_real_value(valor_fuzzy, lim_inf, lim_sup):
    return lim_sup - (lim_sup - lim_inf) * (1 - valor_fuzzy)