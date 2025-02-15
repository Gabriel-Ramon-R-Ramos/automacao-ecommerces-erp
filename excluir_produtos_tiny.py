# Importações
import os
import logging
import pandas as pd
from selenium import webdriver
import libraries as orion

# Função login
def login(driver: webdriver.Chrome, aba_tiny: str, aba_opencart: str, aba_ml: str, aba_mag: str) -> str:
    """Faz o login em todas as plataformas necessárias.

    Args:
        driver (webdriver.Chrome): Objeto de controle do navegador do Selenium
        aba_tiny (str): código da aba gerada pelo Selenium referente ao Tiny
        aba_opencart (str): código da aba gerada pelo Selenium referente ao Opencart
        aba_ml (str): código da aba gerada pelo Selenium referente ao Mercado Livre
        aba_mag (str): código da aba gerada pelo Selenium referente ao Magalu

    Returns:
        str: Url com o token de acesso para não desconectar da sessão atual na Opencart
    """
    
    # Logando no Tiny
    driver.switch_to.window(aba_tiny)
    try:
        orion.tiny.login_manual(driver)
    except RuntimeError as e:
        error_msg = f"Erro ao fazer login no Tiny - {e}"
        logging.error(error_msg, extra={"sku": ""})
        raise RuntimeError(f"Erro ao fazer login no Tiny - {e}") from e

    # Logando na Opencart
    driver.switch_to.window(aba_opencart)
    try:
        url_product_opencart = orion.opencart.login_opencart(driver)
    except RuntimeError as e:
        error_msg = f"Erro ao fazer login na Opencart - {e}"
        logging.error(error_msg, extra={"sku": ""})
        raise RuntimeError(f"Erro ao fazer login na Opencart - {e}") from e

    # Logando no Mercado Livre
    driver.switch_to.window(aba_ml)
    try:
        orion.mercado_livre.login_ml(driver)  # Login manual, aperte ENTER para concluir o login
    except RuntimeError as e:
        error_msg = f"Erro ao fazer login no Mercado Livre - {e}"
        logging.error(error_msg, extra={"sku": ""})
        raise RuntimeError(f"Erro ao fazer login no Mercado Livre - {e}") from e

    # Logando no Magalu
    driver.switch_to.window(aba_mag)
    try:
        orion.magalu.login_mag(driver)  # Login manual, aperte ENTER para concluir o login
    except RuntimeError as e:
        error_msg = f"Erro ao fazer login no Magalu - {e}"
        logging.error(error_msg, extra={"sku": ""})
        raise RuntimeError(f"Erro ao fazer login no Magalu - {e}") from e
    
    return url_product_opencart

# Função Setup
def setup() -> tuple[webdriver.Chrome, str, str, str, str, pd.DataFrame]:
    """Função de inicialização de váriavies fixa do código e organização.

    Returns:
        tuple[webdriver.Chrome, pd.DataFrame, str, str]: Retorna todas as váriaves inicializadas e organizadas.
    """
    # Criando o driver
    driver = webdriver.Chrome()

    # Abrindo duas novas abas
    driver.execute_script("window.open('');")
    driver.execute_script("window.open('');")
    driver.execute_script("window.open('');")

    # Gerenciando as abas
    aba_tiny = driver.window_handles[0]
    aba_ml = driver.window_handles[1]
    aba_mag = driver.window_handles[2]
    aba_opencart = driver.window_handles[3]

    # Configurando o Logging
    logging.basicConfig(
    filename='erro_logs.csv',
    level=logging.INFO,
    format='%(asctime)s,%(levelname)s,%(message)s,%(sku)s,%(funcName)s,%(lineno)d',
    datefmt='%d/%m/%Y %H:%M:%S'
    )

    # Verifica se o arquivo existe e se não está vazio
    if not os.path.exists('erro_logs.csv') or os.path.getsize('erro_logs.csv') == 0:
        columns = ["asctime", "levelname", "message", "sku", "funcName", "lineno"]
        pd.DataFrame(columns=columns).to_csv('erro_logs.csv', index=False)

    # Lendo a planilha dos produtos a serem excluídos
    produtos_df = pd.read_excel("excluir_produtos.xlsx")
    # Tratando os tipos de dados por coluna
    produtos_df = produtos_df.astype({'Tiny': 'string', 'Ecommerce': 'string', 'ML': 'string', 'Magalu': 'string'})

    return driver, aba_tiny, aba_ml, aba_mag, aba_opencart, produtos_df

# Função Principal
def main():
    """Função principal"""
    # Setup inicial (variáveis inicializadas e configuradas)
    driver, aba_tiny, aba_ml, aba_mag, aba_opencart, produtos_df = setup()

    url_product_opencart = login(driver, aba_tiny, aba_opencart, aba_ml, aba_mag)

    # Percorrendo a planilha
    for i, row in produtos_df.iterrows():
        # Capturando os elementos principais
        sku = row['SKU']
        titulo = row['Descrição']
        tiny_status = row['Tiny']
        opencart_status = row['Ecommerce']
        ml_status = row['ML']
        mag_status = row['Magalu']

        # Verifica se o status não está como "FEITO" para evitar refazer as ações.
        if pd.isna(tiny_status) or tiny_status != "FEITO":
            driver.switch_to.window(aba_tiny)  # Mudando para aba do Tiny
            # Pesquisando o produto no tiny
            encontrado = orion.tiny.pesquisar_produto(driver, sku)
            if encontrado:
                try:
                    # Excluindo o produto no tiny
                    orion.tiny.excluir_produto(driver, sku)
                except Exception as e:
                    error_msg = f'Não foi possível excluir o produto {sku} no TINY - {e}'
                    print(error_msg)
                    logging.error(error_msg, extra={'sku': sku})

                # Atualizando o status - TINY
                produtos_df = orion.planilhas.atualizar_status_csv(produtos_df, "erro_logs.csv", sku, 'Tiny')
                produtos_df.to_excel('excluir_produtos.xlsx', index=False)

        if pd.isna(opencart_status) or opencart_status != "FEITO":
            # Mudando para o Opencart
            driver.switch_to.window(aba_opencart)
            # Pesquisando o produto
            orion.opencart.pesquisar_produto_opencart(driver, url_product_opencart, sku)

            try:
                # Excluindo o produto na Opencart
                orion.opencart.excluir_produto_opencart(driver, sku)
            except Exception as e:
                error_msg = f'Não foi possível excluir o produto {sku} no OPENCART - {e}'
                print(error_msg)
                logging.error(error_msg, extra={'sku': sku})

            # Atualizando o status - OPENCART
            produtos_df = orion.planilhas.atualizar_status_csv(produtos_df, "erro_logs.csv", sku, 'Ecommerce')
            produtos_df.to_excel('excluir_produtos.xlsx', index=False)

        if pd.isna(ml_status) or ml_status != "FEITO":
            driver.switch_to.window(aba_ml)  # Mudando para aba do ML
            try:
                #Excluindo produtos do Mercado Livre
                orion.mercado_livre.excluir_produto_ml(driver, sku)
            except Exception as e:
                error_msg = f'Não foi possível excluir o produto {sku} no MERCADO LIVRE - {e}'
                print(error_msg)
                logging.error(error_msg, extra={'sku': sku})

            # Atualizando o status - ML
            produtos_df = orion.planilhas.atualizar_status_csv(produtos_df, "erro_logs.csv", sku, 'ML')
            produtos_df.to_excel('excluir_produtos.xlsx', index=False)

        if pd.isna(mag_status) or mag_status != "FEITO":
            driver.switch_to.window(aba_mag)  # Mudando para aba do Magalu
            try:
                # Excluindo produtos do Magalu
                orion.magalu.excluir_produto_mag(driver, sku, titulo)
            except Exception as e:
                error_msg = f'Não foi possível excluir o produto {sku} no MAGALU - {e}'
                print(error_msg)
                logging.error(error_msg, extra={'sku': sku})

            # Atualizando o status - MAGALU
            produtos_df = orion.planilhas.atualizar_status_csv(produtos_df, "erro_logs.csv", sku, 'Magalu')
            produtos_df.to_excel('excluir_produtos.xlsx', index=False)

    print("Exclusão concluída!")


main()
