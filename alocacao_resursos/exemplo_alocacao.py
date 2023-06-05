import numpy as np
import numpy_financial as npf
import pandas as pd
import scipy.optimize as opt
import copy
from parametros import t, limite_exposicao, taxa_desconto, custo_om_c, custo_om_h, custo_om_s, custo_om_e, lim_pld, lim_hidro, lim_solar, lim_eolico
from definicao_portfolio import geracao_hidro, geracao_solar, geracao_eolica, compras, vendas, preco_compras, preco_vendas, carga_total
from definicao_cenarios import df_cenario_base, df_cenario_pouca_chuva, df_cenario_desenvolvimento_mundial, df_cenario_incentivo_renovaveis, CenarioParameters
from funcoes_objetivo import limite_inf_exposicao, limite_sup_exposicao, min_calc_risco, max_calc_vpl_receita, calc_max_min
from xf_model import build_regret_matrix, build_choice_criteria_matrix, build_normalized_choice_criteria_matrix


list_cenarios = [df_cenario_base, df_cenario_pouca_chuva, df_cenario_desenvolvimento_mundial, df_cenario_incentivo_renovaveis]

list_objetos_cenarios = []
for df_cen in list_cenarios:
    obj_cenario = CenarioParameters(df_cen, lim_pld, lim_hidro, lim_solar, lim_eolico)
    list_objetos_cenarios.append(copy.deepcopy(obj_cenario))

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

list_solucoes = []
for obj_cen in list_objetos_cenarios:
    solucao_harmoniosa, f_val_max_min = calc_max_min(x0, list_bounds, list_constraint, cenario_object=obj_cen)
    list_solucoes.append(solucao_harmoniosa)
    print(f'f_val_max_min: {f_val_max_min} | solução: {solucao_harmoniosa}')

payoff_vpl = np.zeros([len(list_solucoes), len(list_objetos_cenarios)])
payoff_risco = np.zeros([len(list_solucoes), len(list_objetos_cenarios)])
for i in range(len(list_solucoes)):
    for j in range(len(list_objetos_cenarios)):
        payoff_vpl[i, j] = max_calc_vpl_receita(list_solucoes[i], list_objetos_cenarios[j])
        payoff_risco[i, j] = min_calc_risco(list_solucoes[i], list_objetos_cenarios[j])
payoff_vpl = payoff_vpl/1E6
#
regret_vpl = build_regret_matrix(-payoff_vpl)       # - because it's to be maximized
cc_vpl = build_choice_criteria_matrix(-payoff_vpl)
ncc_vpl = build_normalized_choice_criteria_matrix(cc_vpl)
#
regret_risco = build_regret_matrix(payoff_risco)
cc_risco = build_choice_criteria_matrix(payoff_risco)
ncc_risco = build_normalized_choice_criteria_matrix(cc_risco)

agregated_ncc = np.minimum(ncc_vpl, ncc_risco)

print("fim")
