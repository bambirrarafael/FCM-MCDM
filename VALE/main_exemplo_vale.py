import numpy as np
import pandas as pd
import numpy_financial as npf
from portfolio import geracao_hidro, geracao_solar, geracao_eolica, compras, vendas, preco_compras, preco_vendas, carga_total
from cenarios import df_cenario_base, df_cenario_pouca_chuva, df_cenario_desenvolvimento_mundial, df_cenario_incentivo_renovaveis


def calc_receita(x_contrat, x_hidro, x_solar, x_eolico):
    exp = calc_exposicao(x_contrat, x_hidro, x_solar, x_eolico)
    return 8760 * (vendas * preco_vendas + pld * exp - compras * preco_compras - custo_om_hidro * geracao_hidro - custo_om_solar * geracao_solar - p_contrat * x_contrat - p_hidro * x_hidro - p_solar * x_solar - p_eolico * x_eolico)


def calc_risco(x_contrat, x_hidro, x_solar, x_eolico):
    exp = calc_exposicao(x_contrat, x_hidro, x_solar, x_eolico)
    return np.mean( abs(sigma_spot*exp) + abs(sigma_c*(x_contrat + compras)) + sigma_h*(x_hidro + geracao_hidro) + sigma_w*(x_eolico+geracao_eolica) + sigma_s*(x_solar + geracao_solar) )


def calc_exposicao(x_contrat, x_hidro, x_solar, x_eolico):
    return compras + geracao_hidro + geracao_solar + x_contrat + x_hidro + x_solar + x_eolico - vendas - carga_total


list_cenarios = [df_cenario_base, df_cenario_pouca_chuva, df_cenario_desenvolvimento_mundial, df_cenario_incentivo_renovaveis]

t = 15
taxa_desconto = 0.05
lim_pld = [50, 600]
lim_hidro = [-0.15, 0.1]
lim_solar = [-0.1, 0.1]
lim_eolico = [-0.15, 0.15]

custo_om_hidro = np.zeros(t)
custo_om_solar = np.zeros(t)
custo_om_eolico = np.zeros(t)

x_contrat = np.zeros(t)
x_hidro = np.zeros(t)
x_solar = np.zeros(t)
x_eolico = np.zeros(t)


pld_fuzzy = np.zeros(t)
gsf_hidro_fuzzy = np.zeros(t)
gsf_solar_fuzzy = np.zeros(t)
gsf_eolico_fuzzy = np.zeros(t)

for i in range(t):
    pld_fuzzy[i] = df_cenario_base['C1'].iloc[i]        #  for cenario in list_cenarios:
    # gsf_hidro_fuzzy[i] = np.mean(df_cenario_base['C4'].iloc[12 * i:12 * i + 12])
    # gsf_solar_fuzzy[i] = np.mean(df_cenario_base['C7'].iloc[12 * i:12 * i + 12])
    # gsf_eolico_fuzzy[i] = np.mean(df_cenario_base['C6'].iloc[12 * i:12 * i + 12])

pld = lim_pld[1] - ((1 - pld_fuzzy) * (lim_pld[1] - lim_pld[0]))
# gsf_hidro = lim_hidro[1] - ((1 - gsf_hidro_fuzzy) * (lim_hidro[1] - lim_hidro[0]))/2
# geracao_hidro = geracao_hidro + geracao_hidro * gsf_hidro
# gsf_solar = lim_solar[1] - ((1 - gsf_solar_fuzzy) * (lim_solar[1] - lim_solar[0]))/2
# geracao_solar = geracao_solar + geracao_solar * gsf_solar

p_contrat = 0.2
p_hidro = 0.2
p_solar = 0.2
p_eolico = 0.2

sigma_spot = 0.2
sigma_c = 0.2
sigma_h = 0.2
sigma_w = 0.2
sigma_s = 0.2




exp = calc_exposicao(x_contrat, x_hidro, x_solar, x_eolico)

receita_financeira = calc_receita(x_contrat, x_hidro, x_solar, x_eolico)

vpl = npf.npv(rate=taxa_desconto, values=receita_financeira)

print("fim")
