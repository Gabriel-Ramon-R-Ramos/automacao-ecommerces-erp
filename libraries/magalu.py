# Importações
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

# Função de login manual
def login_mag(driver: webdriver.Chrome, login_url='https://seller.magalu.com/dashboard'):
    """Função de login manual no Magalu, devido à verificação em duas etapas.

    Acessa a página de login e aguarda que o usuário finalize o processo manualmente. 
    Verifica se o login foi concluído com sucesso, baseado em elementos da página.

    Args:
        driver (webdriver.Chrome): Objeto de controle do navegador do Selenium.
        login_url (str, optional): URL de acesso à página de login. Defaults to https://seller.magalu.com/dashboard.
    """
    driver.get(login_url)
    print("Aguardando você fazer o login...")

    while True:
        input("Pressione ENTER assim que finalizar: ")
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "PlataformaSeller-MuiShellProfile-userInfo"))
            )
            print("Login detectado com sucesso!")
            break
        except TimeoutException:
            print("Login ainda não detectado. Tente novamente.")


# Buscar produto - MAGALU
def pesquisar_produto_mag(driver: webdriver.Chrome, valor: str, tipo='SKU'):
    """Faz a busca do produto informado por dois metódos: SKU e Título. Ou qualquer outro aceito. Basta saber como é definido no HTML.

    São utilizados dois metódos, pois o MAGALU permite vários modos de pesquisas e esses são os principais.\n
    E caso não de certo por um pode adaptar o código para tentar por outro metódo de pesquisa.

    Args:
        driver (webdriver.Chrome): Objeto de controle do navegador do Selenium.
        valor (str): Valor a ser pesquisado (SKU ou Título)
        tipo (str, optional): Tipo da pesquisa aceita pela plataforma do Magalu. Defaults to 'SKU'.
    """
    wait = WebDriverWait(driver, 10)
    busca = wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, '.MaasProduct-MuiOutlinedInput-input.MaasProduct-MuiInputBase-input')))
    busca.click()

    # Selecionando SKU ou Titulo na busca
    tipo_button_xpath = f'//div[@role="button" and .//span[contains(text(), "{tipo}")]]'
    wait.until(EC.element_to_be_clickable((By.XPATH, tipo_button_xpath))).click()

    busca.send_keys(valor)
    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, '.MaasProduct-MuiButtonBase-root.MaasProduct-MuiButton-root.MaasProduct-MuiButton-contained.MaasProduct-MuiButton-root.MaasProduct-MuiButton-contained.MaasProduct-MuiButton-containedPrimary.MaasProduct-MuiButton-containedSizeLarge.MaasProduct-MuiButton-sizeLarge.MaasProduct-MuiButton-disableElevation.MaasProduct-MuiButton-fullWidth')
        )).click()


# Verifica se o produto foi encontrado
def verificar_produto_mg(driver: webdriver.Chrome, sku: str) -> bool:
    """Verifica se o produto, após a busca (`pesquisar_produto_mag()`), foi encontrado ou não. 

    Args:
        driver (webdriver.Chrome): Objeto de controle do navegador do Selenium.
        sku (str): SKU do produto

    Returns:
        bool: `True` se o produto foi encontrado e `False` caso contrário.
    """
    try:
        # Procurando o elemento mais ações
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located(
        (By.CLASS_NAME, 'icon--mode-actions')))
    except TimeoutException:
        print(f'Não foi possível encontrar o produto com o SKU: {sku} - MAGALU')
        encontrado = False
    else:
        encontrado = True

    return encontrado


# Função Auxiliar
def inativar_produto_mag(driver: webdriver.Chrome, encontrado: bool, sku: str, titulo: str):
    """Inativa o produto informado na plataforma do Magalu

    Essa função serve de auxilio para a função `excluir_produto_mag()`.\n
    Antes de usar essa função, utilize a função `pesquisar_produto_mag()` antes para acessar a página do produto.

    Args:
        driver (webdriver.Chrome): Objeto de controle do navegador do Selenium.
        encontrado (bool): Variável booleana para saber se o produto foi encontrado ou não.
        sku (str): SKU do produto.
        titulo (str): Titulo do produto.
    """
    wait = WebDriverWait(driver, 2)
    if encontrado:
        try:
            # Clicando em mais ações
            wait.until(EC.element_to_be_clickable(
                (By.CLASS_NAME, 'icon--mode-actions'))).click()
            # Clicando em inativar produto
            wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//li[@role="menuitem" and .//p[contains(text(), "Inativar")]]'))).click()
            # Confirmando a inativação
            wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//button[@data-testid="on-confirm-button"]'))).click()
        except TimeoutException:
            erro_msg = f'Não foi possivel inativar o produto {sku} - {titulo} - MAGALU'
            print(erro_msg)


# Função excluir kits - Magalu
def excluir_produto_mag(driver: webdriver.Chrome, sku: str, titulo: str):
    """Exclui o produto/anúncio especificado no Magalu, através de seu SKU e/ou Titulo.

    Temos a opção titulo como alternativa ao SKU devido a dificuldade de pesquisa no Magalu,
    por isso é recomendado passar os dois.

    Args:
        driver (webdriver.Chrome): Objeto de controle do navegador do Selenium.
        sku (str): SKU do produto que será excluido.
        titulo (str): Titulo do produto, para caso a pesquisa do SKU dê erro.
    """
    wait = WebDriverWait(driver, 2)
    # Caso apareça uma tela de notificação
    try:
        WebDriverWait(driver, 2).until(EC.element_to_be_clickable(
            (By.XPATH, '/html/body/div[3]/div[3]/div/div/div/div[3]/button'))).click()
    except TimeoutException:
        print('')

    try:
        # Resetando a pesquisa
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//button[@aria-label="Limpar"]'))).click()
    except Exception:
        print('')

    # Tentando encontrar pelo SKU
    pesquisar_produto_mag(driver, sku, tipo='SKU')
    # Verificando se o produto foi encontrado
    encontrado = verificar_produto_mg(driver, sku)
    # Inativando o produto
    inativar_produto_mag(driver, encontrado, sku, titulo)

    # Resetando a pesquisa
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//button[@aria-label="Limpar"]'))).click()

    if not encontrado:
        print('PROCURANDO PELO TITULO')
        pesquisar_produto_mag(driver, titulo, tipo='Título')

        # Verificando se o produto foi encontrado
        encontrado = verificar_produto_mg(driver, sku)

        # Inativando o produto
        inativar_produto_mag(driver, encontrado, sku, titulo)

    try:
        # Resetando a pesquisa
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//button[@aria-label="Limpar"]'))).click()
    except Exception:
        print('')
