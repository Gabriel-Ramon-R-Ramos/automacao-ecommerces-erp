# Importações
import pandas as pd
from selenium import webdriver
from libraries import opencart

# Função login
def login(driver: webdriver.Chrome) -> str:
    """Faz o login em todas as plataformas necessárias.

    Args:
        driver (webdriver.Chrome): Objeto de controle do navegador do Selenium
    """
    # Logando no Tiny
    try:
        url_product_opencart = opencart.login_opencart(
            driver, login_url="https://urldelogin.com", username="ALTERE AQUI", password="ALTERE AQUI")
    except Exception as e:
        raise RuntimeError(f"Erro ao fazer login no Tiny - {e}") from e
    return url_product_opencart


def setup() -> tuple[webdriver.Chrome, pd.DataFrame]:
    """Função de inicialização de váriavies fixa do código e organização.

    Returns:
        tuple[webdriver.Chrome, pd.DataFrame]: Retorna todas as váriaves inicializadas e organizadas.
    """
    driver = webdriver.Chrome()

    # Lendo a planilha dos produtos a serem excluídos
    # ALTERE AQUI CONFORME NECESSÁRIO
    produtos_df = pd.read_excel("ALTERE AQUI.xlsx")
    if "status" not in produtos_df.columns:
        produtos_df["status"] = '-'

    # Tratando os tipos de dados
    produtos_df = produtos_df.astype(str)

    url_product_opencart = login(driver)

    return driver, produtos_df, url_product_opencart


def main():
    """Função principal
    """
    driver, produtos_df, url_product_opencart = setup()

    for i, row in produtos_df.iterrows():
        product_id = row['ID']
        meta_tittle = row['Meta titulo']
        meta_descricao = row['Meta Descrição']
        palavra_chave = row['Meta palavras chaves']
        produtos_relacionados = row['Produtos Relacionados']
        compre_junto = row['Compre Junto']
        p_fisica = row['pessoa fisica']
        p_juridica = row['pessoa juridica']
        p_revenda = row['pessoa juridica revenda']
        slug = row['Padrão']

        print(F"ACESSNDO O PRODUTO: {meta_tittle}")
        opencart.acessar_produto_opencart(
            driver, url_product_opencart, product_id)
        opencart.ajustar_zoom(driver)
        print("ATUALIZANDO O META TITULO")
        opencart.atualizar_meta_titulo(driver, meta_tittle)
        print("ATUALIZANDO A META DESCRIÇÃO")
        opencart.atualizar_descricao(driver, meta_descricao)
        print("ATUALIZANDO AS PALAVRAS CHAVES")
        opencart.atualziar_palavra_chave(driver, palavra_chave)
        print("ATUALIZANDO OS PRODUTOS RELACIONADOS")
        opencart.atualizar_produtos_relacionados(
            driver, produtos_relacionados)
        print("ATUALIZANDO OS PRODUTOS COMPRE JUNTO")
        opencart.atualizar_compre_junto(driver, compre_junto)
        print("ATUALIZANDO AS PROMOÇÕES")
        opencart.atualizar_promocoes(
            driver, p_fisica, p_juridica, p_revenda)
        print("ATUALIZANDO O SLUG")
        opencart.atualizar_slug(driver, slug)
        print("SALVANDO AS ALTERAÇÕES")
        opencart.salvar_altercoes(driver)


main()
