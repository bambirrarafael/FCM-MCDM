import numpy as np
import numpy_financial as npf
from parametros import t, limite_exposicao, taxa_desconto, custo_om_c, custo_om_h, custo_om_s, custo_om_e
from definicao_portfolio import geracao_hidro, geracao_solar, geracao_eolica, compras, vendas, preco_compras, preco_vendas, carga_total


def calc_vpl_receita(x, cenario_object):
    x_contrat = x[0]
    x_hidro = x[1]
    x_solar = x[2]
    x_eolico = x[3]
    exp = calc_exposicao(x)
    receita_financeira = 8760 * (vendas * preco_vendas + cenario_object.pld * exp - compras * preco_compras - custo_om_h * geracao_hidro - custo_om_s * geracao_solar - cenario_object.p_c * x_contrat - cenario_object.p_h * x_hidro - cenario_object.p_s * x_solar - cenario_object.p_w * x_eolico)
    return npf.npv(rate=taxa_desconto, values=receita_financeira)


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
    return np.mean(abs(cenario_object.sigma_spot * exp) + abs(cenario_object.sigma_c * (x_contrat + compras)) + cenario_object.sigma_h * (x_hidro + geracao_hidro) + cenario_object.sigma_w * (x_eolico + geracao_eolica) + cenario_object.sigma_s * (x_solar + geracao_solar))


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


def calc_max_min(x, cenario_object):
    fval_max_calc_risco = max_calc_risco(x, cenario_object)
    fval_min_calc_risco = min_calc_risco(x, cenario_object)
    fval_max_calc_vpl_receita = max_calc_vpl_receita(x, cenario_object)
    fval_min_calc_vpl_receita = min_calc_vpl_receita(x, cenario_object)
    return max_min(x, fval_max_calc_risco, fval_min_calc_risco, fval_max_calc_vpl_receita, fval_min_calc_vpl_receita, cenario_object)


def limite_inf_exposicao(x):
    return -calc_exposicao(x) - limite_exposicao


def limite_sup_exposicao(x):
    return calc_exposicao(x) - limite_exposicao