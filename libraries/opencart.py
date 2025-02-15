# Importações
import re
import time
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Função AUXILIARES
def clicar_elemento(wait: WebDriverWait, by_type: By, elememto: WebElement, descricao: str=''):
    """Clica em um elemento

    Args:
        wait (WebDriverWait): Tempo de esperar até que o clique seja possível
        by_type (By): Tipo do elemento clicaveç
        elememto (WebElement): Elemento clicável
        descricao (str, optional): Descrição do clique. Defaults to ''.

    Raises:
        RuntimeError: Erro ao clicar no elemenot informado
    """
    try:
        click_elem = wait.until(EC.visibility_of_element_located((by_type, elememto)))
        wait.until(EC.element_to_be_clickable(click_elem)).click()
    except Exception as e:
        raise RuntimeError(f"Erro ao clicar no elememto {descricao} - {str(e)}") from e


def scrolar_comeco(driver:webdriver.Chrome):
    """Roal até o começo da página

    Args:
        driver (webdriver.Chrome): Objeto de controle do Selenium
    """
    driver.execute_script("window.scrollTo(0, 0);")


def scrolar_final(driver:webdriver.Chrome):
    """Rola até o final da página

    Args:
        driver (webdriver.Chrome): Objeto de controle do Selenium
    """
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


def ajustar_zoom(driver:webdriver.Chrome, zoom:str='75%'):
    """Ajusta o zoom da página

    Args:
        driver (webdriver.Chrome): Objeto de controle do Selenium
        zoom (str, optional): Porcentagem de zoom. Defaults to '75%'.
    """
    driver.execute_script(f"document.body.style.zoom='{zoom}'")


# Função login - OPENCART
def login_opencart(driver: webdriver.Chrome, login_url='URL DO LOGIN', username='SEU USUSARIO', password='SUA SENHA'):
    """Faz o acesso ao login no painel adiministrativo da WebThomas para a Opencart
    e retorna a url com o token de acesso atual para não se desconectar da sessão.

    Args:
        driver (webdriver.Chrome): Objeto de controle do navegador do Selenium
        login_url (str, optional): URL de acesso à página de login. Defaults to ''.
        username (str, optional): Nome de usuário para fazer o acesso. Defaults to ''.
        password (str, optional): Senha para fazer o acesso. Defaults to ''.

    Returns:
        str: Url com o token de acesso para não desconectar da sessão atual
    """
    wait = WebDriverWait(driver, 10)

    # Acessando a página de login
    print('LOGANDO - OPENCART')
    driver.get(login_url)

    # Preenchendo o campo de usuário
    email_field = wait.until(EC.presence_of_element_located(
        (By.NAME, 'username')))
    email_field.clear()
    email_field.send_keys(username)

    # Preenchendo o campo senha
    senha_field = wait.until(EC.presence_of_element_located(
        (By.NAME, 'password')))
    senha_field.clear()
    senha_field.send_keys(password)

    # Clicando em ACESSAR
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    print('CAPTURANDO O TOKEN')
    print('-' * 20)
    # Capturando a url atual
    url = driver.current_url
    # Dividindo a URL a partir de '&user_token'
    url_parts = url.split('&user_token=')
    # Armazenando o token
    token = url_parts[1]
    # Substituindo a URL do produto
    url_product = f'https://www.orionferramentas.com/painel/index.php?route=catalog/product/edit&user_token={token}'

    return url_product


# Função verificar produto - OPENCART
def verificar_produto_opencart(driver: webdriver.Chrome) -> bool:
    """Verifica se o produto existe na Opecart.

    Args:
        driver (webdriver.Chrome): Objeto de controle do navegador do Selenium.

    Returns:
        bool: True se o produto existe, False caso contrário.
    """
    wait = WebDriverWait(driver, 2)

    print('VERIFICANDO SE O PRODUTO EXISTE')
    try:
        # Capturando o ID do produto
        produto = wait.until(EC.visibility_of_element_located(
            (By.NAME, 'selected[]'))).get_attribute('value')
    except Exception:
        print('O produto não existe na Opencart')
        produto = None

    # Verificando se o produto existe
    return produto is not None and produto != ''


# Função Acessar produto
def acessar_produto_opencart(driver: webdriver.Chrome, url_product: str, product_id: str | int):
    """Acessa um produto no opencart WebTHomas\n
    Deve se usar a função `login()` antes para conseguir a url
    com o token ativo e acessar a plataforma

    Args:
        driver (webdriver.Chrome): Objeto de controle do Selenium
        url_product (str): url com o token ativo para manter a sessão
        product_id (str | int): ID do produto fornecido pelo tiny
    """
    # Acessando o produto
    driver.get(f'{url_product}&product_id={product_id}')


# Função pesquisar produto
def pesquisar_produto_opencart(driver: webdriver.Chrome, url_product: str, sku: str):
    """Pesquisa um produto no opencart WebTHomas\n
    Deve se usar a função `login()` antes para conseguir a url
    com o token ativo e acessar a plataforma

    Args:
        driver (webdriver.Chrome): Objeto de controle do Selenium
        url_product (str): url com o token ativo para manter a sessão
        sku (str): SKU do produto
    """
    # Acessando o produto
    driver.get(f'{url_product}&filter_sku{sku}')


# Função para atualizar ou adicionar uma categoria para o produto
def atualizar_categoria_opencart(driver: webdriver.Chrome, category: str, product_id: str | int):
    """Atualiza ou adiciona uma categoria para o produto na Opencart WebThomas

    Args:
        driver (webdriver.Chrome): Objeto de controle do Selenium
        category (str): Nome da categoria existente que o produto irá ser atribuido
        product_id (str | int): ID do produto fornecido pelo Tiny
    """
    wait = WebDriverWait(driver, 10)

    # Verificando se o produto existe no site
    existe = verificar_produto_opencart(driver)

    # Se existir atualiza o produto
    if existe:
        print('ATUALIZANDO A CATEGORIA DO PRODUTO')
        # Clicando na aba Ligações
        wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'a[href="#tab-links"]'))).click()

        # Selecionando o label departamentos
        departamentos = wait.until(EC.visibility_of_element_located(
            (By.ID, 'input-category')))

        # Pesquisando a categoria
        departamentos.send_keys(category)

        # Tentando adicionar a categoria
        try:
            # Procurando a opção da categoria
            dropdown_option = wait.until(EC.visibility_of_element_located(
                (By.XPATH, f'//ul[@class="dropdown-menu"]/li/a[contains(text(), "{category}")]')))

            # Adicionando a categoria
            dropdown_option.click()
        except Exception as e:
            error_mgs = f"Erro ao selecionar a categoria '{category}': {e}"
            print(error_mgs)

        # Salvando as alterações
        botao_salvar = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'button.btn.btn-primary[data-original-title="Salvar"]')))

        # Clicando no botão salvar
        botao_salvar.click()
    else:
        error_mgs = f'O produto de ID: {product_id} não existe no site'
        print(error_mgs)


# Função excluir produto - Opencart
def excluir_produto_opencart(driver: webdriver.Chrome, sku: str):
    """Exclui o produto informado.

    Essa função é dependente da função `login()` para acessar a plataforma e\n
    da função `pesquisar_produtos_opencart()` para pesquisar o produto.

    Args:
        driver (webdriver.Chrome): Objeto de controle do navegador do Selenium
        sku (str): SKU do produto, somente para confirmar se o produto foi encontrado.
    """
    wait = WebDriverWait(driver, 10)

    # Verificando se o produto foi encontrado
    encontrado = verificar_produto_opencart(driver)
    
    if encontrado:
        # Selecionando o produto
        wait.until(EC.visibility_of_element_located(
                (By.NAME, 'selected[]'))).click()
        # Clicando em excluir produto
        wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'button[data-original-title="Excluir"]')
        )).click()
        # Confirmando o pop-up
        wait.until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert.accept()
    else:
        # Lança uma exceção caso o produto não seja encontrado
        raise ValueError(f"O produto com SKU '{sku}' não foi encontrado no Opencart.")


def atualizar_produtos_relacionados(driver:webdriver.Chrome, related_products:str):
    """Atualiza os produtos que se relaciona a um produto conforme a lista de produto relacionados. 

    Args:
        driver (webdriver.Chrome): Objeto de controle do Selenium
        related_products (str): lista que se relacionam com o produto
    """
    wait = WebDriverWait(driver, 5)
    scrolar_comeco(driver)
    time.sleep(1)
    scrolar_final(driver)
    clicar_elemento(wait, By.CSS_SELECTOR, 'a[href="#tab-links"]', "aba ligações")
    label_relacionados = wait.until(EC.visibility_of_element_located((By.ID, 'input-related')))
    products = related_products.split('\n')
    for produto in products:
        try:
            produto = re.sub(r'^\d+-', '', produto)
            label_relacionados.clear()
            label_relacionados.send_keys(produto)
            clicar_elemento(wait, By.XPATH, f'//ul[@class="dropdown-menu"]/li/a[contains(text(), "{produto}")]', "selcionar produto relacionado")
        except Exception:
            print(f"Não foi possível relacionar o produto: {produto}")


def atualizar_compre_junto(driver:webdriver.Chrome, compre_junto:str):
    """Atualiza os produtos que podem ser comprado junto com o principal

    Args:
        driver (webdriver.Chrome): Objeto de controle do Selenium
        compre_junto (str): Lista dos produtos que se relacionam
    """
    wait = WebDriverWait(driver, 5)
    scrolar_comeco(driver)
    time.sleep(1)
    scrolar_final(driver)
    clicar_elemento(wait, By.CSS_SELECTOR, 'a[href="#tab-links"]', "aba ligações")
    label_compre_junto = wait.until(EC.visibility_of_element_located((By.ID, 'input-buy_together')))
    products = compre_junto.split('\n')
    for produto in products:
        try:
            produto = re.sub(r'^\d+-', '', produto)
            label_compre_junto.clear()
            label_compre_junto.send_keys(produto)
            clicar_elemento(wait, By.XPATH, f'//ul[@class="dropdown-menu"]/li/a[contains(text(), "{produto}")]', "selcionar produto relacionado")
        except Exception:
            print(f"Não foi possível relacionar no compre junto o produto: {produto}")


def atualizar_promocoes(driver:webdriver.Chrome, p_fisica:str, p_juridica:str, p_revenda:str):
    """atualiza as promoções conforme os preços informados

    Args:
        driver (webdriver.Chrome): Objeto de controle do Selenium
        p_fisica (str): Preço para pessoas físicas
        p_juridica (str): Preço para pessoas juridicas
        p_revenda (str): Preços para revendedores
    """
    wait = WebDriverWait(driver, 20)
    clicar_elemento(wait, By.CSS_SELECTOR, 'a[href="#tab-special"]', "aba promoções")
    clicar_elemento(wait, By.CSS_SELECTOR, 'button[onclick="addSpecial();"]', 'Adicionar promoção')
    time.sleep(1)
    clicar_elemento(wait, By.CSS_SELECTOR, 'button[onclick="addSpecial();"]', 'Adicionar promoção')
    # ---- Provisorio até pensar em uma solução melhor
    select_fisica = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'select[name="product_special[0][customer_group_id]"]')))
    select_0 = Select(select_fisica)
    select_0.select_by_value("1")
    
    select_juridica = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'select[name="product_special[1][customer_group_id]"]')))
    select_1 = Select(select_juridica)
    select_1.select_by_value("2")
    
    select_revenda = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'select[name="product_special[2][customer_group_id]"]')))
    select_2 = Select(select_revenda)
    select_2.select_by_value("3")
    # ----
    preco_fisica_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="product_special[0][price]"]')))
    preco_fisica_input.clear()
    preco_fisica_input.send_keys(p_fisica.replace(',', '.'))
    
    preco_juridica_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="product_special[1][price]"]')))
    preco_juridica_input.clear()
    preco_juridica_input.send_keys(p_juridica.replace(',', '.'))

    preco_revenda_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="product_special[2][price]"]')))
    preco_revenda_input.clear()
    preco_revenda_input.send_keys(p_revenda.replace(',', '.'))


def atualizar_slug(driver:webdriver.Chrome, slug:str):
    """Atualiza o slug (url amigável) do produto

    Args:
        driver (webdriver.Chrome): Objeto de controle do Selenium
        slug (str): URL amigavél
    """
    wait = WebDriverWait(driver, 20)
    clicar_elemento(wait, By.CSS_SELECTOR, 'a[href="#tab-seo"]', "aba seo")
    slug_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[placeholder="URL amigável"]')))
    slug_input.clear()
    slug_input.send_keys(slug)


def atualizar_meta_titulo(driver:webdriver.Chrome, meta_titulo:str):
    """Atualiza o meta titulo do produto

    Args:
        driver (webdriver.Chrome): objeto de controle do Selenium
        meta_titulo (str): Meta titulo que será atualizado
    """
    wait = WebDriverWait(driver, 20)
    scrolar_final(driver)
    meta_titulo_input = wait.until(EC.visibility_of_element_located((By.ID, 'input-meta-title2')))
    meta_titulo_input.clear()
    meta_titulo_input.send_keys(meta_titulo)


def atualizar_descricao(driver:webdriver.Chrome, descricao:str):
    """Atualiza a meta descrição do produto

    Args:
        driver (webdriver.Chrome): objeto de controle do Selenium
        descricao (str): Descrição que será atualizada
    """
    wait = WebDriverWait(driver, 20)
    scrolar_final(driver)
    descricao_input = wait.until(EC.visibility_of_element_located((By.ID, 'input-meta-description2')))
    descricao_input.clear()
    descricao_input.send_keys(descricao)


def atualziar_palavra_chave(driver:webdriver.Chrome, palavra_chave:str):
    """Atualzia a meta palavra chave do produto

    Args:
        driver (webdriver.Chrome): Objeto de controle do Selenium
        palavra_chave (str): Palavras chaves separadas por virgula, somente.
    """
    wait = WebDriverWait(driver, 20)
    scrolar_final(driver)
    palavra_input = wait.until(EC.visibility_of_element_located((By.ID, 'input-meta-keyword2')))
    palavra_input.clear()
    palavra_input.send_keys(palavra_chave)


def salvar_altercoes(driver:webdriver.Chrome):
    """Salva as alterações feitas

    Args:
        driver (webdriver.Chrome): Objeto de controle do Selenium
    """
    wait = WebDriverWait(driver, 20)
    clicar_elemento(wait, By.CSS_SELECTOR, 'button.btn.btn-primary[data-original-title="Salvar"]', 'Salvar alterações')
