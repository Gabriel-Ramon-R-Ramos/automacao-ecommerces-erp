# Importações
import logging
import pandas as pd
from selenium import webdriver
from libraries import tiny
from libraries import planilhas

# Função login
def login(driver: webdriver.Chrome) -> str:
    """Faz o login em todas as plataformas necessárias.

    Args:
        driver (webdriver.Chrome): Objeto de controle do navegador do Selenium
    """
    # Logando no Tiny
    try:
        tiny.login_manual(driver)
    except RuntimeError as e:
        error_msg = f"Erro ao fazer login no Tiny - {e}"
        logging.error(error_msg, extra={"sku": ""})
        raise RuntimeError(f"Erro ao fazer login no Tiny - {e}") from e


# Função Setup
def setup() -> tuple[webdriver.Chrome, pd.DataFrame]:
    """Função de inicialização de váriavies fixa do código e organização.

    Returns:
        tuple[webdriver.Chrome, pd.DataFrame]: Retorna todas as váriaves inicializadas e organizadas.
    """
    # Criando o driver
    driver = webdriver.Chrome()

    # Configurando o Logging
    logging.basicConfig(
    filename='erro_logs_atualizar_precos.log',
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s | %(sku)s | %(funcName)s | %(lineno)d',
    datefmt='%d/%m/%Y %H:%M:%S'
    )

    # Lendo a planilha dos produtos a serem excluídos
    produtos_df = pd.read_excel("lista 18122024_1.xlsx") # ALTERE AQUI CONFORME NECESSÁRIO
    if "status" not in produtos_df.columns:
        produtos_df["status"] = '-'
    # Tratando os tipos de dados por coluna
    produtos_df = produtos_df.astype({'ID': 'string',
                                      'SKU': 'string',
                                      'Descrição': 'string',
                                      'Preço': 'Float32',
                                      'Preço promocional': 'Float32',
                                      'Lp-Mkp': 'float32',
                                      'Lp-Mkp Promocional': 'float32',
                                      'Revenda': 'float32',
                                      'Revenda Promocional': 'float32',
                                      'status': 'string'})
    produtos_df[produtos_df.select_dtypes(include=['float32', 'float64', 'float']).columns] = produtos_df.select_dtypes(include=['float32', 'float64', 'float']).round(2)

    login(driver)

    return driver, produtos_df


# Função principal
def main():
    """Função principal"""
    driver, produtos_df = setup()

    for i, row in produtos_df.iterrows():
        product_id = row["ID"]
        sku = row["SKU"]
        status = row["status"]

        if 'FEITO' not in status:
            try:
                tiny.acessar_produto(driver, product_id) # Acessando o produto
                tiny.clicar_editar_produtos(driver) # Clicando no botão de edição
                tiny.atualizar_preco(driver, row["Preço"])
                tiny.atualizar_preco(driver, row["Preço promocional"], promocional=True)
                tiny.atualizar_preco_site(driver, row["Preço"])
                tiny.atualizar_preco_site(driver, row["Preço promocional"], promocional=True)
                tiny.atualizar_preco_mkp(driver, row["Lp-Mkp"])
                tiny.atualizar_preco_mkp(driver, row["Lp-Mkp Promocional"], promocional=True)
                tiny.atualizar_preco_revenda(driver, row["Revenda"])
                tiny.atualizar_preco_revenda(driver, row["Revenda Promocional"], promocional=True)
                tiny.clicar_salvar_edicao_produtos(driver) # Salvando as edições
                print("")
            except RuntimeError as e:
                driver.refresh()
                print(e)
                logging.error(e, extra={'sku': sku})

            try:
                tiny.sincronizar_produtos_sites(driver, opencart=True)
            except RuntimeError as e:
                driver.refresh()
                print(e)
                logging.error(e, extra={'sku': sku})

            try:
                tiny.sincronizar_mkp_ml(driver)
            except RuntimeError as e:
                driver.refresh()
                print(e)
                logging.error(e, extra={'sku': sku})

            try:
                tiny.sincronizar_mkp_magalu(driver)
            except RuntimeError as e:
                driver.refresh()
                print(e)
                logging.error(e, extra={'sku': sku})

        produtos_df = planilhas.atualizar_status_log(produtos_df, "erro_logs_atualizar_precos.xlsx", sku)
        produtos_df.to_excel('lista 18122024_1.xlsx', index=False) # MUDAR O NOME CONFORME NECESSÁRIO


main()
