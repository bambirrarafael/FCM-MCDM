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

risco = min_calc_risco(x0, list_objetos_cenarios[0])
vpl = max_calc_vpl_receita(x0, list_objetos_cenarios[0])
max_min = calc_max_min(x0, list_objetos_cenarios[0])

# exp = calc_exposicao(x_contrat, x_hidro, x_solar, x_eolico)
# vpl_receita = calc_vpl(x)
# risco = calc_risco(x)
                            # contratos         usinas hidraulicas          solares             eólicas
limites_inferiores_variaveis = [-100] + list(-geracao_hidro[0]) + list(-geracao_solar[0]) + list(-geracao_eolica[0])
limites_superiores_variaveis = [100] * 4
list_bounds = []
for i in range(4 * t):
    list_bounds.append([limites_inferiores_variaveis[i], limites_superiores_variaveis[i]])
list_constraint = [
    {'type': 'ineq', 'fun': limite_inf_exposicao},
    {'type': 'ineq', 'fun': limite_sup_exposicao}
]

#
# funções para o risco
result = opt.minimize(min_calc_risco, x0, bounds=list_bounds) # , constraints=list_constraint)
fval_min_calc_risco = result.fun
xval_min_calc_risco = result.x
result = opt.minimize(max_calc_risco, x0, bounds=list_bounds)
fval_max_calc_risco = -result.fun
xval_max_calc_risco = result.x
#
# funções para a receita
result = opt.minimize(min_calc_vpl_receita, x0, bounds=list_bounds)
fval_min_calc_vpl_receita = result.fun
xval_min_calc_vpl_receita = result.x
result = opt.minimize(max_calc_vpl_receita, x0, bounds=list_bounds)
fval_max_calc_vpl_receita = -result.fun
xval_max_calc_vpl_receita = result.x

args_max_min = (fval_max_calc_risco, fval_min_calc_risco, fval_max_calc_vpl_receita, fval_min_calc_vpl_receita)
result = opt.minimize(max_min, xval_min_calc_risco, args=args_max_min, bounds=list_bounds)
f_val_max_min = -result.fun
solucao_harmoniosa = result.x



print("fim")
