import numpy as np
import numpy_financial as npf
import scipy.optimize as opt
from parametros import t, limite_exposicao, taxa_desconto, custo_om_c, custo_om_h, custo_om_s, custo_om_e
from parametros import limite_orcamento_gamma as gamma
from definicao_portfolio import geracao_hidro, geracao_solar, geracao_eolica, compras, vendas, preco_compras, preco_vendas, carga_total


def max_calc_diversidade(x):
    return - calc_diversidade(x)


def min_calc_diversidade(x):
    return calc_diversidade(x)


def calc_diversidade(x):
    epsilon = 1e-7
    N = len(x) + epsilon
    x_contrat = x[0]
    x_hidro = x[1]
    x_solar = x[2]
    x_eolico = x[3]
    recursos_totais = np.sum(x) + compras + geracao_hidro + geracao_solar + geracao_eolica
    p_contrat = (x_contrat + compras) / recursos_totais
    p_hidro = (x_hidro + geracao_hidro) / recursos_totais
    p_solar = (x_solar + geracao_solar) / recursos_totais
    p_eolico = (x_eolico + geracao_eolica) / recursos_totais
    d_t = - ((p_contrat * np.log(p_contrat + epsilon) / np.log(N)) +
             (p_hidro * np.log(p_hidro + epsilon) / np.log(N)) +
             (p_solar * np.log(p_solar + epsilon) / np.log(N)) +
             (p_eolico * np.log(p_eolico + epsilon) / np.log(N)))
    return np.mean(d_t)


def calc_vpl_receita(x, cenario_object):
    x_contrat = x[0]
    x_hidro = x[1]
    x_solar = x[2]
    x_eolico = x[3]
    exp = calc_exposicao(x)

    vetor_receita = 8760 * (vendas * preco_vendas + cenario_object.pld * exp - compras * preco_compras - custo_om_h * geracao_hidro - custo_om_s * geracao_solar - cenario_object.p_c * x_contrat - cenario_object.p_h * x_hidro - cenario_object.p_s * x_solar - cenario_object.p_w * x_eolico)
    return npf.npv(rate=taxa_desconto, values=vetor_receita)


def min_calc_vpl_receita(x, cenario_object):
    return calc_vpl_receita(x, cenario_object)


def max_calc_vpl_receita(x, cenario_object):
    return -calc_vpl_receita(x, cenario_object)


def calc_risco(x, cenario_object):
    x_contrat = x[0]
    x_hidro = x[1]
    x_solar = x[2]
    x_eolico = x[3]
    exp = calc_exposicao(x)
    cenario_object.sigma_spot = np.std(exp)
    energia_a = abs(cenario_object.sigma_spot * (cenario_object.pld * exp))
    energia_b = abs(cenario_object.sigma_c * (cenario_object.p_c * x_contrat + preco_compras * compras))
    energia_c = cenario_object.sigma_h * (cenario_object.p_h * x_hidro + custo_om_h * geracao_hidro)
    energia_d = cenario_object.sigma_s * (cenario_object.p_s * x_solar + custo_om_s * geracao_solar)
    energia_e = cenario_object.sigma_w * (cenario_object.p_w * x_eolico + custo_om_e * geracao_eolica)
    denominador_energia = exp + x_contrat + x_hidro + x_solar + x_eolico + compras + geracao_hidro + geracao_solar + geracao_eolica
    preco_a = abs(cenario_object.phi_spot * exp)
    preco_b = cenario_object.phi_c * (x_contrat + compras)
    preco_c = cenario_object.phi_h * (x_hidro + geracao_hidro)
    preco_d = cenario_object.phi_s * (x_solar + geracao_solar)
    preco_e = cenario_object.phi_w * (x_eolico + geracao_eolica)
    risco_de_energia = (energia_a + energia_b + energia_c + energia_d + energia_e)/denominador_energia
    risco_de_preco = preco_a + preco_b + preco_c + preco_d + preco_e
    vertor_risco = 8760*(risco_de_energia + risco_de_preco)
    return np.mean(vertor_risco)


def min_calc_risco(x, cenario_object):
    return calc_risco(x, cenario_object)


def max_calc_risco(x, cenario_object):
    return -calc_risco(x, cenario_object)


def calc_exposicao(x):
    x_contrat = x[0]
    x_hidro = x[1]
    x_solar = x[2]
    x_eolico = x[3]
    return compras + geracao_hidro + geracao_solar + x_contrat + x_hidro + x_solar + x_eolico - vendas - carga_total



def min_mu_risco(x, f_max, f_min, cenario_object):
    f_val = calc_risco(x, cenario_object)
    return (f_max - f_val) / (f_max - f_min)


def max_mu_receita(x, f_max, f_min, cenario_object):
    f_val = calc_vpl_receita(x, cenario_object)
    return (f_val - f_min) / (f_max - f_min)


def max_min(x, fval_max_calc_risco, fval_min_calc_risco, fval_max_calc_vpl_receita, fval_min_calc_vpl_receita, cenario_object):
    #
    # definição de mu para a receita e pro risco
    f_val_mu_risco = min_mu_risco(x, fval_max_calc_risco, fval_min_calc_risco, cenario_object)
    f_val_mu_receita = max_mu_receita(x, fval_max_calc_vpl_receita, fval_min_calc_vpl_receita, cenario_object)
    #
    mu_D = np.min([f_val_mu_risco, f_val_mu_receita])
    return - mu_D


def calc_max_min(x0, list_bounds, cenario_object):
    #
    # funções para o risco
    result_min_risco = opt.minimize(min_calc_risco, x0, args=cenario_object, bounds=list_bounds)#, constraints=list_constraint, method='SLSQP')
    fval_min_calc_risco = result_min_risco.fun
    xval_min_calc_risco = result_min_risco.x
    result_max_risco = opt.minimize(max_calc_risco, x0, args=cenario_object, bounds=list_bounds)#, constraints=list_constraint, method='SLSQP')
    fval_max_calc_risco = -result_max_risco.fun
    xval_max_calc_risco = result_max_risco.x
    #
    # funções para a receita
    result_min_vpl = opt.minimize(min_calc_vpl_receita, x0, args=cenario_object, bounds=list_bounds)#, constraints=list_constraint, method='SLSQP')
    fval_min_calc_vpl_receita = result_min_vpl.fun
    xval_min_calc_vpl_receita = result_min_vpl.x
    result_max_vpl = opt.minimize(max_calc_vpl_receita, x0, args=cenario_object, bounds=list_bounds)#, constraints=list_constraint, method='SLSQP')
    fval_max_calc_vpl_receita = -result_max_vpl.fun
    xval_max_calc_vpl_receita = result_max_vpl.x

    args_max_min = (fval_max_calc_risco, fval_min_calc_risco, fval_max_calc_vpl_receita, fval_min_calc_vpl_receita, cenario_object)
    result = opt.minimize(max_min, xval_min_calc_risco, args=args_max_min, bounds=list_bounds)#, constraints=list_constraint, method='SLSQP')
    f_val_max_min = -result.fun
    solucao_harmoniosa = result.x
    return solucao_harmoniosa, f_val_max_min


def limite_inf_exposicao(x):
    return -calc_exposicao(x) - limite_exposicao


def limite_sup_exposicao(x):
    return calc_exposicao(x) - limite_exposicao


def restricao_orcamento(x, cenario_object):
    x_contrat = x[0]
    x_hidro = x[1]
    x_solar = x[2]
    x_eolico = x[3]
    p_contrat = cenario_object.p_c * x_contrat
    p_hidro = cenario_object.p_h * x_hidro
    p_solar = cenario_object.p_s * x_solar
    p_eolica = cenario_object.p_w * x_eolico
    return gamma - 8765 * 15 * (p_contrat + p_hidro + p_solar + p_eolica)
