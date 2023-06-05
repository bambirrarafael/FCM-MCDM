import numpy as np
import pandas as pd
from FCM import make_scenario_CNFCM, plot_scenario, make_scenario


class CenarioParameters:
    def __init__(self, df_cenario, lim_pld, lim_hidro, lim_eolico, lim_solar):
        t = len(df_cenario)
        pld_fuzzy = np.zeros(t)
        gsf_hidro_fuzzy = np.zeros(t)
        gsf_solar_fuzzy = np.zeros(t)
        gsf_eolico_fuzzy = np.zeros(t)

        for i in range(t):
            pld_fuzzy[i] = df_cenario_base['C1'].iloc[i]  # for cenario in list_cenarios:
            gsf_hidro_fuzzy[i] = np.mean(df_cenario_base['C4'].iloc[i])
            gsf_eolico_fuzzy[i] = np.mean(df_cenario_base['C6'].iloc[i])
            gsf_solar_fuzzy[i] = np.mean(df_cenario_base['C7'].iloc[i])

        self.pld = find_real_value(pld_fuzzy, lim_pld[0], lim_pld[1])
        self.gsf_hidro = find_real_value(gsf_hidro_fuzzy, lim_hidro[0], lim_hidro[1])
        self.gsf_eolico = find_real_value(gsf_eolico_fuzzy, lim_eolico[0], lim_eolico[1])
        self.gsf_solar = find_real_value(gsf_solar_fuzzy, lim_solar[0], lim_solar[1])
        #
        self.p_spot = np.mean(self.pld)
        self.p_c = 198.00
        self.p_h = 130.00
        self.p_w = 120.00
        self.p_s = 143.00
        #
        self.sigma_spot = np.std(self.pld)
        self.sigma_c = 0.00
        self.sigma_h = np.std(self.gsf_hidro)
        self.sigma_w = np.std(self.gsf_eolico)
        self.sigma_s = np.std(self.gsf_solar)


def find_fuzzy_value(valor_real, lim_inf, lim_sup):
    return 1 - (lim_sup - valor_real)/(lim_sup - lim_inf)


def find_real_value(valor_fuzzy, lim_inf, lim_sup):
    return lim_sup - (lim_sup - lim_inf) * (1 - valor_fuzzy)


estado_inicial = {
                    'C1': 0.3,      # 270           Prec¸o da energia
                    "C2": 0.25,     # 67500         Demanda de energia
                    "C3": 0.5,      # 0%            investimentos setor elétrico
                    'C4': 0.62,     # 0.5 %         geracao hidraulica
                    'C5': 0.48,     # -1.2%         geracao termica
                    'C6': 0.8,      # 9%            geracao eólica
                    'C7': 0.8,      # 6%            geracao solar
                    'C8': 0.25,     # baixo         precipitacao
                    "C9": 0.25,     # baixo         energia armazenada
                    "C10": 0.6,     # 1%            PIB Brasil
                    'C11': 0.15,    # 4.6           Preço gás natural
                    'C12': 0.5,     # 0%            producao industria
                    'C13': 0.3,     # 2.75          preço óleo combustivel
                    'C14': 0.7      # 2%            PIB paraguai
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
