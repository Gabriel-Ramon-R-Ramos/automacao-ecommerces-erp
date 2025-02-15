# Importações
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

# Função de login manual
def login_ml(driver: webdriver.Chrome, login_url='https://www.mercadolivre.com/jms/mlb/lgz/msl/login'):
    """Função de login manual no Mercado Livre, devido à verificação em duas etapas.

    Acessa a página de login e aguarda que o usuário finalize o processo manualmente. 
    Verifica se o login foi concluído com sucesso, baseado em elementos da página.

    Args:
        driver (webdriver.Chrome): Objeto de controle do navegador do Selenium.
        login_url (str, optional): URL de acesso à página de login. Defaults to'https://www.mercadolivre.com/jms/mlb/lgz/msl/login'.
    """
    driver.get(login_url)
    print("Aguardando você fazer o login...")

    while True:
        input("Pressione ENTER assim que finalizar: ")
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "nav-header-user"))
            )
            print("Login detectado com sucesso!")
            break
        except TimeoutException:
            print("Login ainda não detectado. Tente novamente.")


# Função excluir anúncios - Mercado livre
def excluir_produto_ml(driver: webdriver.Chrome, sku: str|int):
    """Exclui o produto/anúncio especificado no mercado livre, através do seu SKU.

    Args:
        driver (webdriver.Chrome): Objeto de controle do navegador do Selenium
        sku (str | int): SKU do produto/anúncio que será excluido
    """
    wait = WebDriverWait(driver, 5)

    # Link do produto para excluir
    url_product = f'https://www.mercadolivre.com.br/anuncios/lista?page=1&search={sku}'
    # Acessando o produto
    driver.get(url_product)

    # Obtém a altura total da página
    total_height = driver.execute_script("return document.body.scrollHeight")
    # Calcula 50% da altura total
    half_height = total_height / 2
    # Faz o scroll até 50% da página
    driver.execute_script(f"window.scrollTo(0, {half_height});")

    # Clicando na opção selecionar tudo
    try:
        wait.until(EC.element_to_be_clickable(
            (By.CLASS_NAME, 'andes-checkbox__input'))).click()
    except TimeoutException as e:
        error_msg = f'Não foi possivel encontrar o produto de SKU: {sku} - MERCADO LIVRE'
        print(error_msg)
        raise RuntimeError(f"{error_msg} - {e}") from e

    # Clicando na opção excluir
    wait.until(EC.element_to_be_clickable(
        (By.ID, ':R9rlacq5p6:'))).click()

    # Confirmando a exclusão //*[@id=":rs:"]
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//button[@class="andes-button andes-button--large andes-button--loud" and .//span[text()="Excluir"]]'))).click()

# Função excluir anúncios - Mercado livre
def pausar_produto_ml(driver: webdriver.Chrome, sku: str|int):
    """Pausa o produto/anúncio especificado no mercado livre, através do seu SKU.

    Args:
        driver (webdriver.Chrome): Objeto de controle do navegador do Selenium
        sku (str | int): SKU do produto/anúncio que será excluido
    """
    wait = WebDriverWait(driver, 5)

    # Link do produto para excluir
    url_product = f'https://www.mercadolivre.com.br/anuncios/lista?page=1&search={sku}'
    # Acessando o produto
    driver.get(url_product)

    # Obtém a altura total da página
    total_height = driver.execute_script("return document.body.scrollHeight")
    # Calcula 50% da altura total
    half_height = total_height / 2
    # Faz o scroll até 50% da página
    driver.execute_script(f"window.scrollTo(0, {half_height});")

    # Clicando na opção selecionar tudo
    try:
        wait.until(EC.element_to_be_clickable(
            (By.CLASS_NAME, 'andes-checkbox__input'))).click()
    except TimeoutException as e:
        error_msg = f'Não foi possivel encontrar o produto de SKU: {sku} - MERCADO LIVRE'
        print(error_msg)
        raise RuntimeError(f"{error_msg} - {e}") from e

    try:
        # Clicando na opção pausar
        wait.until(EC.element_to_be_clickable(
            (By.ID, ':R8rmacq5p6:'))).click()
    except TimeoutError as e:
        error_msg = f"Não foi possível pausar o produto de SKU: {sku} - MERCADO LIVRE"
        print(error_msg)
        raise RuntimeError(f"{error_msg} = {e}") from e

    # Confirmando o pause do produto
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id=":r14t:"]/span'))).click()
