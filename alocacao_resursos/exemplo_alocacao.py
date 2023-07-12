import numpy as np
import numpy_financial as npf
import pandas as pd
import scipy.optimize as opt
import copy
from parametros import t, limite_exposicao, taxa_desconto, custo_om_c, custo_om_h, custo_om_s, custo_om_e, lim_pld, lim_hidro, lim_solar, lim_eolico
from definicao_portfolio import geracao_hidro, geracao_solar, geracao_eolica, compras, vendas, preco_compras, preco_vendas, carga_total
from definicao_cenarios import df_cenario_base, df_cenario_pouca_chuva, df_cenario_desenvolvimento_mundial, df_cenario_incentivo_renovaveis, CenarioParameters
from funcoes_objetivo import limite_inf_exposicao, limite_sup_exposicao, min_calc_risco, max_calc_vpl_receita, calc_max_min, restricao_orcamento, calc_diversidade, max_calc_diversidade, min_calc_diversidade
from xf_model import build_regret_matrix, build_choice_criteria_matrix, build_normalized_choice_criteria_matrix
from xr_models import evaluate_on_xr_model

list_cenarios = [df_cenario_base, df_cenario_pouca_chuva, df_cenario_desenvolvimento_mundial, df_cenario_incentivo_renovaveis]

list_objetos_cenarios = []
for df_cen in list_cenarios:
    obj_cenario = CenarioParameters(df_cen, lim_pld, lim_hidro, lim_solar, lim_eolico)
    list_objetos_cenarios.append(copy.deepcopy(obj_cenario))

x0 = np.zeros(4)

                            # contratos         usinas hidraulicas          solares             eólicas
limites_inferiores_variaveis = [0] * 4
limites_superiores_variaveis = [100] * 4
list_bounds = []
for i in range(4):
    list_bounds.append([limites_inferiores_variaveis[i], limites_superiores_variaveis[i]])

list_solucoes = []
for obj_cen in list_objetos_cenarios:
    list_constraint = [{'type': 'ineq', 'fun': restricao_orcamento, 'args': (obj_cen,)}]  # definição da restrição
    #
    solucao_harmoniosa, f_val_max_min = calc_max_min(x0, list_bounds, cenario_object=obj_cen)
    list_solucoes.append(solucao_harmoniosa)
    print(f'f_val_max_min: {f_val_max_min} | solução: {solucao_harmoniosa}')

payoff_vpl = np.zeros([len(list_solucoes), len(list_objetos_cenarios)])
payoff_risco = np.zeros([len(list_solucoes), len(list_objetos_cenarios)])
for i in range(len(list_solucoes)):
    for j in range(len(list_objetos_cenarios)):
        payoff_vpl[i, j] = max_calc_vpl_receita(list_solucoes[i], list_objetos_cenarios[j])
        payoff_risco[i, j] = min_calc_risco(list_solucoes[i], list_objetos_cenarios[j])
payoff_vpl = payoff_vpl/1E6
payoff_risco = payoff_risco/1E6
#
regret_vpl = build_regret_matrix(-payoff_vpl)       # - because it's to be maximized
cc_vpl = build_choice_criteria_matrix(-payoff_vpl)
ncc_vpl = build_normalized_choice_criteria_matrix(cc_vpl)
#
regret_risco = build_regret_matrix(payoff_risco)
cc_risco = build_choice_criteria_matrix(payoff_risco)
ncc_risco = build_normalized_choice_criteria_matrix(cc_risco)

agregated_ncc = np.minimum(ncc_vpl, ncc_risco)

#### XR

solucao_min_diversidade = opt.minimize(min_calc_diversidade, x0, bounds=list_bounds, method='L-BFGS-B')
solucao_max_diversidade = opt.minimize(max_calc_diversidade, x0, bounds=list_bounds, method='L-BFGS-B')
solucao_max_diversidade.fun = - solucao_max_diversidade.fun

d_solucoes = np.array([calc_diversidade(list_solucoes[0]), calc_diversidade(list_solucoes[3])])
mu_hat_Rp = np.zeros([2, 2])
mu_hat_Rp[0, 0] = (d_solucoes[0] - d_solucoes[0])/(2*(solucao_max_diversidade.fun - solucao_min_diversidade.fun)) + 0.5
mu_hat_Rp[1, 1] = (d_solucoes[1] - d_solucoes[1])/(2*(solucao_max_diversidade.fun - solucao_min_diversidade.fun)) + 0.5
mu_hat_Rp[0, 1] = (d_solucoes[0] - d_solucoes[1])/(2*(solucao_max_diversidade.fun - solucao_min_diversidade.fun)) + 0.5
mu_hat_Rp[1, 0] = (d_solucoes[1] - d_solucoes[0])/(2*(solucao_max_diversidade.fun - solucao_min_diversidade.fun)) + 0.5

mu_Rp = np.zeros([2, 2])
for i in range(2):
    for j in range(2):
        if mu_hat_Rp[i, j] >= 0.5:
            mu_Rp[i, j] = 1
        else:
            mu_Rp[i, j] = 1 + mu_hat_Rp[i, j] - mu_hat_Rp[j, i]


result = evaluate_on_xr_model(mu_Rp)

print("fim")
