import numpy as np
import numpy_financial as npf
import pandas as pd
import scipy.optimize as opt
from parametros import t, limite_exposicao, taxa_desconto, custo_om_c, custo_om_h, custo_om_s, custo_om_e, lim_pld, lim_hidro, lim_solar, lim_eolico
from definicao_portfolio import geracao_hidro, geracao_solar, geracao_eolica, compras, vendas, preco_compras, preco_vendas, carga_total
from definicao_cenarios import df_cenario_base, df_cenario_pouca_chuva, df_cenario_desenvolvimento_mundial, df_cenario_incentivo_renovaveis, CenarioParameters
from funcoes_objetivo import limite_inf_exposicao, limite_sup_exposicao, min_calc_risco, max_calc_vpl_receita, calc_max_min


list_cenarios = [df_cenario_base, df_cenario_pouca_chuva, df_cenario_desenvolvimento_mundial, df_cenario_incentivo_renovaveis]

list_objetos_cenarios = []
for cen in list_cenarios:
    list_objetos_cenarios.append(CenarioParameters(df_cenario_base, lim_pld, lim_hidro, lim_solar, lim_eolico))

x0 = np.zeros(4)

                            # contratos         usinas hidraulicas          solares             eólicas
limites_inferiores_variaveis = [-100] + [-geracao_hidro[0]] + [-geracao_solar[0]] + [-geracao_eolica[0]]
limites_superiores_variaveis = [100] * 4
list_bounds = []
for i in range(4):
    list_bounds.append([limites_inferiores_variaveis[i], limites_superiores_variaveis[i]])
list_constraint = [
    {'type': 'ineq', 'fun': limite_inf_exposicao},
    {'type': 'ineq', 'fun': limite_sup_exposicao}
]

solucao_harmoniosa, f_val_max_min = calc_max_min(x0, list_bounds, list_constraint, cenario_object=list_objetos_cenarios[0])


print("fim")
