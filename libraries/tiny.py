# Importações
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

# Funções auxiliares
def clicar_editar_produtos(driver: webdriver.Chrome):
    """Tenta cliclar no botão de edição de produtos. Obs: Importante estar na página do produto para funcionar

    Args:
        driver (webdriver.Chrome): Objeto de controle do Selenium

    Raises:
        RuntimeError: Erro ao clicar no botão editar produto
    """
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.CLASS_NAME, 'btn-edicao-item'))).click()
    except Exception as e:
        raise RuntimeError(f"Erroa ao cliclar em editar o produto: {str(e)}") from e


def clicar_salvar_edicao_produtos(driver:webdriver.Chrome):
    """Tenta salvar as edições feitas no produto

    Args:
        driver (webdriver.Chrome): Objeto de controle do Selenium

    Raises:
        RuntimeError: Erroa ao clicar em salvar as edições do produto
    """
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.ID, 'botaoSalvar'))).click()
    except Exception as e:
        raise RuntimeError(f"Erro ao salvar as edições do produto: {str(e)}") from e


def clicar_aba_precos(driver: webdriver.Chrome):
    """Tentar clicar na aba de preços do produto. Obs: Importante estar na tela de edição do produto para funcionar.

    Args:
        driver (webdriver.Chrome): Objeto de controle do Selenium.

    Raises:
        RuntimeError: Erro ao acessar a aba de preços
    """
    try:
        driver.find_element(By.XPATH, '//*[@id="link-precos"]').click()
    except Exception as e:
        raise RuntimeError(f"Erro ao acessar a aba de preços: {str(e)}") from e


def encontrar_lista_precos(driver: webdriver.Chrome, lista_id: str) -> (WebElement | None):
    """Procura a lista de preço informada no ID na tabela de lista de preços. Obs: Importante estar na aba de preços do produto e no modo edição para funcionar.
    
    VERIFIQUE O CÓDIGO DESSA FUNÇÃO ANTES DE UTILIZA-LA

    Args:
        driver (webdriver.Chrome): Objeto de controle do Selenium
        lista_id (str):

    Returns:
        (WebElement | None): Retorna o elemento encontrado, se não None.
    """
    try:
        return WebDriverWait(driver, 2).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, f'table > tbody > tr > td > input[value="{lista_id}"]')))
    except Exception:
        return None # Se não econtrar, retona None


def configurar_lista_precos(driver: webdriver.Chrome, lista_id: str):
    """Configura a lista de preço informada (adiciona ela ao produto).\n
    VERIFIQUE O CÓDIGO DESSA FUNÇÃO ANTES DE UTILIZA-LA
    
    Obs:  Importante estar na aba de preços do produto e no modo edição para funcionar.

    Args:
        driver (webdriver.Chrome): Objeto de controle do Selenium
        lista_id (str): Id da lista de preço.

    Raises:
        RuntimeError: Erro ao adiconar a lista de preço ao produto, verique o ID da lista.
    """
    try:
        lista_precos_elem = driver.find_element(By.ID, 'idListaPreco')
        lista_precos = Select(lista_precos_elem)
        lista_precos.select_by_value(f'{lista_id}')  # Seleciona a opção correta
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'button[onclick="adicionarProdutoListaPreco();"]'))).click()
        print("Lista de preços configurada com sucesso.")
    except Exception as e:
        raise RuntimeError(f"Erro ao configurar lista de preços, verifique o ID da lista: {str(e)}") from e


def atualizar_lista_preco(driver: webdriver.Chrome, price: str, lista_id: str, colum_price = "preco"):
    """Atualiza os preços que estão na lista. VERIFIQUE O CÓDIGO DESSA FUNÇÃO ANTES DE UTILIZA-LA\n
    Obs:  Importante estar na aba de preços do produto e no modo edição para funcionar.

    Args:
        driver (webdriver.Chrome): Objeto de controle do Selenium
        price (str): Novo preço do produto
        lista_id (str): Id da lista de preço.
        colum_price (str, optional): Coluna que será alterada (preco ou precoPromocional). Defaults to "preco".

    Raises:
        RuntimeError: Erro ao atualizar o preço, verifique as colunas e o ID da lista.
    """
    try:
        site_row = WebDriverWait(driver, 5).until(EC.visibility_of_element_located(
            (By.XPATH, f'//input[@value="{lista_id}"]/ancestor::tr')))
        preco_elem = site_row.find_element(By.XPATH, f'.//input[contains(@name, "[{colum_price}]")]')

        # Obtém o valor atual e verifica se precisa ser atualizado
        valor_mkp_elem = str(preco_elem.get_attribute('value')).replace('.', '').replace(',', '.')
        if valor_mkp_elem != str(price):
            preco_elem.clear()
            preco_elem.send_keys(Keys.BACK_SPACE * 4, str(price).replace('.', ','))
            print(f"Preço antigo: {valor_mkp_elem}\nNovo preço: {price}")
        else:
            print("O preço já está atualizado.")
    except Exception as e:
        raise RuntimeError(f"Erro ao atualizar o preço: {str(e)}") from e


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


# Função de login no tiny - INATIVA
def login(driver: webdriver.Chrome, login_url='https://erp.tiny.com.br/login/', username='ALTERE AQUI', password='ALTERE AQUI'):
    """Faz o login na plataforma do Tiny ERP (Olist).

    Args:
        driver (webdriver.Chrome): Objeto de controle do navegador do Selenium
        login_url (str, optional): URL de acesso à página de login Defaults to 'https://erp.tiny.com.br/login/'.
        username (str, optional): Nome de usuário para fazer o acesso. Defaults to ''.
        password (str, optional): Senha para fazer o acesso. Defaults to ''.
    """
    print('LOGANDO - TINY')
    wait = WebDriverWait(driver, 10)

    # Acessando a URL de login
    driver.get(login_url)

    # Preenchendo o campo de e-mail
    email_field = wait.until(EC.presence_of_element_located(
        (By.NAME, 'username')))
    email_field.clear()
    email_field.send_keys(username)

    # Preenchendo o campo de senha
    password_field = driver.find_element(By.NAME, 'password')
    password_field.clear()
    password_field.send_keys(password)

    # Clicando no botão de login
    driver.find_element(By.CSS_SELECTOR, '.sc-ispOId.fPZXsr').click()

    time.sleep(2)

    # Esperar por possíveis mensagens de erro
    try:
        logado = wait.until(
            EC.presence_of_element_located((By.TAG_NAME, 'h3'))).text
        if 'Este usuário já está logado em outro dispositivo' in logado:
            driver.find_element(
                By.CSS_SELECTOR, '.btn.btn-primary').click()
    except RuntimeError as e:
        print(f"Erro ao confirmar login: {str(e)}")


# Login manual - TINY
def login_manual(driver: webdriver.Chrome, login_url='https://erp.tiny.com.br/login/'):
    """Função de login manual no Tiny, devido à verificação em duas etapas.

    Acessa a página de login e aguarda que o usuário finalize o processo manualmente. 
    Verifica se o login foi concluído com sucesso, baseado em elementos da página.

    Args:
        driver (webdriver.Chrome): Objeto de controle do Selenium
        login_url (str, optional): URL de acesso à página de login. Defaults to 'https://erp.tiny.com.br/login/'.
    """
    driver.get(login_url)
    print("Aguardando você fazer o login...")

    while True:
        input("Pressione ENTER assim que finalizar: ")
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "card-logo-empresa"))
            )
            print("Login detectado com sucesso!")
            break
        except TimeoutException:
            print("Login ainda não detectado. Tente novamente.")


# Função Pesquisar Produto - TINY
def pesquisar_produto(driver: webdriver.Chrome, sku: str, product_url='https://erp.tiny.com.br/produtos#list') -> bool:
    """Pesquisa o produto que será excluido no Tiny.

    Args:
        driver (webdriver.Chrome): Objeto de controle do Selenium
        sku (str): Sku do produto que será excluido
        product_url (str): URL para acessar a lista de produtos. Default to 'https://erp.tiny.com.br/produtos#list'
    
    Returns:
        bool: `True` se o produto for encontrado, `False` caso contrario
    """
    print('PESQUISANDO O PRODUTO - TINY')
    wait = WebDriverWait(driver, 10)
    # Acessando a lista de produtos
    driver.get(product_url)

    try:
        # Clicando no campo de busca e pressionando ENTER
        busca = wait.until(EC.visibility_of_element_located(
            (By.ID, "pesquisa-mini")))
        busca.clear()
        busca.send_keys(sku, Keys.ENTER)
        busca.send_keys(Keys.ENTER)
    except Exception as e:
        raise f'Erro ao pesquisar o produto {sku}: {str(e)}'

    # Verificando se encontrou o produto
    try:
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, f'table#tabelaListagem tr[codigo="{sku}"]')))
        encontrado = True
    except Exception:
        print("Elemento não encontrado no TINY")
        encontrado = False

    return encontrado


# Função excluir produto - TINY
def excluir_produto(driver: webdriver.Chrome, sku: str, product_url='https://erp.tiny.com.br/produtos#list'):
    """Exclui o produto solicitado. OBS: Funciona somente se a função `pesquisar_produto`
    for importada.

    Args:
        driver (webdriver.Chrome): Objeto de controle do Selenium
        sku (str): SKU do produto que será excluido
        product_url (str, optional): URL para acessar a lista de produtos. Default to 'https://erp.tiny.com.br/produtos#list'
    """
    if not pesquisar_produto(driver, sku, product_url):
        print(f"Produto com SKU {sku} não encontrado. A exclusão não será realizada.")
        raise ValueError(f"Produto com SKU {sku} não encontrado. A exclusão não será realizada.")

    print('EXCLUINDO O PRODUTO - TINY')
    wait = WebDriverWait(driver, 10)

    try:
        # Mudando o ZOOM para 75%
        driver.execute_script("document.body.style.zoom = '75%'")
        # Seleciona o produto
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, f'//*[@codigo="{sku}"]/td[1]/span'))).click()

        # Selecionando mais ações
        mais_acoes = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//div[@class="dropdown dropup dropdown-in featured-actions-menu"]//button[@class="btn btn-menu-acoes dropdown-toggle" and contains(., "Mais ações")]')))
        mais_acoes.click()

        # Selecionando e rolando o dropdow até o final
        div_ul = wait.until(EC.visibility_of_element_located(
            (By.ID, 'menuAcoesEmMassa')))
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", div_ul)

        # Excluindo o produto
        excluir_btn = wait.until(EC.element_to_be_clickable(
            (By.ID, 'btnExcluirMobile')))
        excluir_btn.click()

        # Selecionando excluir anexo
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//div[@class="checkbox"]/label'))).click()

        # Confirmando exclusão
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//button[@popup-action="confirm"]'))).click()
    except Exception as e:
        raise RuntimeError(f'Erro ao excluir o produto {sku}: {str(e)}') from e


# Função acessar produto - TINY
def acessar_produto(driver:webdriver.Chrome, product_id: str, product_url='https://erp.tiny.com.br/produtos#edit/'):
    """Acessa a página do produto informado pelo ID no tiny

    Args:
        driver (webdriver.Chrome): Objeto de controle do Selenium
        product_id (str): ID do produto fornecido pelo Tiny
        product_url (str, optional): URL para acessar a página do produtos.. Defaults to 'https://erp.tiny.com.br/produtos#edit/'.
    """
    print(f'ACESSANDO O PRODUTO {product_id}- TINY')
    try:
        driver.get(f'{product_url}{product_id}')
    except Exception as e:
        raise RuntimeError(f"Erro ao acessar o produto {product_id} - {str(e)}") from e


# Função para atualziar o preço - TINY
def atualizar_preco(driver: webdriver.Chrome, product_price: str, promocional=False):
    """Atualiza o preço do produto da aba pricipal

    Args:
        driver (webdriver.Chrome): Objeto de controle do Selenium
        product_price (str): Preço do produto que será atualizado
        promocional (bool, optional): True para atualizar o preco promocional. Defaults to False
    """
    wait = WebDriverWait(driver, 10)
    print('ATUALIZANDO PREÇO DO PRODUTO - TINY')
    try:
        if promocional:
            preco_elem = wait.until(
            EC.presence_of_element_located((By.ID, 'precoPromocional')))
        else:
            preco_elem = wait.until(
                EC.presence_of_element_located((By.ID, 'preco')))

        valor_preco_elem = str(preco_elem.get_attribute('value')).replace('.', '').replace(',', '.') # Valor vem do TINY

        # Verifica se os preços são iguas
        if valor_preco_elem != str(product_price):
            preco_elem.clear()
            preco_elem.send_keys(Keys.BACK_SPACE * 4,
                                str(product_price).replace('.', ','))
            print(f'Preço antigo: {valor_preco_elem}\nNovo preço: {product_price}')
    except Exception as e:
        raise RuntimeError(f"Erro ao atualizar o preco no Tiny - {str(e)}") from e


# Função atualizar preços marketplaces - TINY
def atualizar_preco_mkp(driver: webdriver.Chrome, mkp_price: str, promocional=False):
    """Atualiza o preco dos marketplaces pelo valor informado. VERIFIQUE O CÓDIGO DESSA FUNÇÃO ANTES DE UTILIZA-LA

    Args:
        driver (webdriver.Chrome): Objeto de controle do Selenium
        mkp_price (str): Novo preco do marketplaces
        promocional (bool, optional): True para atualizar o preco promocional. Defaults to False

    Raises:
        RuntimeError: Não foi possível atualizar o preco dos mkp, verifique a função
    """
    try:
        print("ATUALIZANDO PRECOS MKP - TINY")
        clicar_aba_precos(driver)
        mkp_table = encontrar_lista_precos(driver, "ALTERE AQUI")
        if mkp_table is None:
            configurar_lista_precos(driver, "ALTERE AQUI")
        if promocional:
            atualizar_lista_preco(driver, mkp_price, "ALTERE AQUI", colum_price="ALTERE AQUI")
        else:
            atualizar_lista_preco(driver, mkp_price, "ALTERE AQUI")
    except Exception as e:
        raise RuntimeError(f"Erro ao atualizar o preco do mkp - {str(e)}") from e


# Função atualizar preco site - TINY
def atualizar_preco_site(driver: webdriver.Chrome, site_price: str, promocional=False):
    """Atualzia o preco do site pelo valor informado. VERIFIQUE O CÓDIGO DESSA FUNÇÃO ANTES DE UTILIZA-LA

    Args:
        driver (webdriver.Chrome): Objeto de controle do Selenium
        site_price (str): Novo preço do site
        promocional (bool, optional):  True para atualizar o preco promocional. Defaults to False.

    Raises:
        RuntimeError:  Não foi possível atualizar o preco do site, verifique a função
    """
    try:
        print("ATUALIZANDO PRECOS DO SITE - TINY")
        clicar_aba_precos(driver)
        site_table = encontrar_lista_precos(driver, "ALTERE AQUI")
        if site_table is None:
            configurar_lista_precos(driver, "ALTERE AQUI")
        if promocional:
            atualizar_lista_preco(driver, site_price, "ALTERE AQUI", colum_price="ALTERE AQUI")
        else:
            atualizar_lista_preco(driver, site_price, "ALTERE AQUI")
    except Exception as e:
        raise RuntimeError(f"Erro ao atualizar o preco do site - {str(e)}") from e


# Função atualizar preços revenda - TINY
def atualizar_preco_revenda(driver: webdriver.Chrome, revenda_price: str, promocional=False):
    """Atualzia o preco da revenda pelo valor informado. VERIFIQUE O CÓDIGO DESSA FUNÇÃO ANTES DE UTILIZA-LA

    Args:
        driver (webdriver.Chrome): Objeto de controle do Selenium
        site_price (str): Novo preço da revenda
        promocional (bool, optional):  True para atualizar o preco promocional. Defaults to False.

    Raises:
        RuntimeError:  Não foi possível atualizar o preco do site, verifique a função
    """
    try:
        print("ATUALIZANDO PRECOS DE REVENDA - TINY")
        clicar_aba_precos(driver)
        revenda_table = encontrar_lista_precos(driver, "ALTERE AQUI")
        if revenda_table is None:
            configurar_lista_precos(driver, "ALTERE AQUI")
        if promocional:
            atualizar_lista_preco(driver, revenda_price, "ALTERE AQUI", colum_price="ALTERE AQUI")
        else:
            atualizar_lista_preco(driver, revenda_price, "ALTERE AQUI")
    except Exception as e:
        raise RuntimeError(f"Erro ao atualizar o preco da revenda - {str(e)}") from e    


def verificar_alerta_de_envio(driver: webdriver.Chrome):
    """Verifica se há um alerta após enviar o produto para as plataformas de venda,
    dando a opção de confirmar o envio ou não

    Args:
        driver (webdriver.Chrome): Objeto de controle do Selenium

    Raises:
        RuntimeError: Ocorre quando não é possível clicar no botão de confirmar o envio ou cancelar
    """
    try:
        botao_confirmar = WebDriverWait(driver, 2).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '.btn.btn-sm.btn-primary')))
        botao_cancelar =  WebDriverWait(driver, 2).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '.btn.btn-sm.btn-default')))
    except Exception:
        print('Alerta de envio não encontrado')
        botao_confirmar = None
        botao_cancelar = None
    else:
        if botao_cancelar and botao_confirmar:
            try:
                if 'Atualizar Preços'.lower() in botao_confirmar.text.lower():
                    while True:
                        # escolha = input('Você deseja proseguir? (S/N)').strip().lower()
                        escolha = 's' # Define a escolha como sempre sim
                        if escolha == 's':
                            botao_confirmar.click()
                            break
                        if escolha == 'n':
                            botao_cancelar.click()
                            break
            except Exception as e:
                raise RuntimeError(f'Erro ao clicar no alerta de envio - {str(e)}') from e


# Função enviar precos para as plataformas - TINY
def enviar_precos(driver: webdriver.Chrome):
    """Envia o preço dos produto para as plataforma de vendas: Opencart, Magalu, Mercado Livre e Mercado livre Full

    Args:
        driver (webdriver.Chrome): Objeto de controle do Selenium

    Raises:
        RuntimeError: Quando o clique no botão do menu de ações falha
        RuntimeError: Quando o clique no botão de enviar o produto falha
        RuntimeError: Ocorre quando o verificar_alerta_de_envio dá um erro
        RuntimeError: Quando o produto é enviado, mas a confirmação de envio fica na tela e não consegue ser fechada
    """
    wait = WebDriverWait(driver, 10)
    try:
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="page-wrapper"]/div[5]/div[1]/div/div[2]/button'))).click() # Clicando no menu ações
    except Exception as e:
        raise RuntimeError(f"Erro ao clicar no menu ações - {str(e)}") from e

    wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="im_13"]/a'))).click() # Clicando em enviar para o e-commerce
    wait.until(EC.element_to_be_clickable(
        (By.CLASS_NAME, 'form-control-select'))).click() # Selecionar as plataformar de envio
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="bs-modal"]/div/div/div/div[2]/div[3]/div[1]/div/ul/li[1]/a/div/label'))).click() # Clicando em selecionar todos
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="bs-modal"]/div/div/div/div[2]/div[3]/div[1]/div/ul/li[7]/a/div/label'))).click() # Descelecionando a Skyhub
    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, '.sincronizar-preco-produtos.scope-preco-selecao.btn.btn-primary'))).click() # Clicando no botão selecionar

    try:
        wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'button[onclick="envioPrecoEcommerce.iniciar();"]'))).click() # Clicando no botão de enviar
    except Exception as e:
        raise RuntimeError(f'Erro ao clicar no botão de enviar o produto - {str(e)}') from e

    try:
        verificar_alerta_de_envio(driver)
    except Exception as e:
        raise RuntimeError(f'Erro ao clicar no alerta de envio - {str(e)}') from e

    try:
        wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '.sincronizar-preco-produtos.scope-preco-sincronizado.btn.btn-default'))).click() # Fechando a tela de confirmação
    except Exception as e:
        driver.refresh()
        raise RuntimeError(f'Erro ao clicar no botão de fechar confirmação - {str(e)}') from e


# Função enviar para ml
def sincronizar_mkp_ml(driver: webdriver.Chrome):
    """Faz o envio/sincronização do produto para o Mercado Livre

    Args:
        driver (webdriver.Chrome): Objeto de controle do Selenium

    Raises:
        RuntimeError: Ocorreu um erro ao interagir com algum elemento
    """
    wait = WebDriverWait(driver, 20)
    try:
        clicar_elemento(wait, By.CSS_SELECTOR, 'button.featured-action[original-title=" Enviar para o e-commerce"]', "Enviar para o e-commerce")

        select_elem = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#plataformaSincronizarProdutosEcommerce')))
        select = Select(select_elem)
        select.select_by_value("7093")

        clicar_elemento(wait, By.ID, "btn-interface-anuncios", "Continuar envio de produtos")

        actions = ActionChains(driver)
        move_element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "widget-dropdown-actions")))
        actions.move_to_element(move_element).perform()

        clicar_elemento(wait, By.CLASS_NAME, "checkbox-lote-anuncio", "checkbox anúncio")
        clicar_elemento(wait, By.CSS_SELECTOR, 'button.featured-action[original-title=" Utilizar descrição complementar do produto"]', "utilizar descrição complementar")
        clicar_elemento(wait, By.CLASS_NAME, "widget-dropdown-actions", "card anúncio")
        clicar_elemento(wait, By.CSS_SELECTOR, 'li[tab-anuncio="atributos"]', "ficha técnica")

        try:
            xpath = "//label[contains(text(), 'Marca')]/following-sibling::div[1]//div[contains(@class, 'input-group')]//input[@type='text']"
            marca_input = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            marca_input.clear()
            marca_input.send_keys("Orion")
        except Exception:
            print("Não foi possível alterar a marca do produto")

        try:
            xpath = "//label[contains(text(), 'Modelo')]/following-sibling::div[1]//div[contains(@class, 'input-group')]//input[@type='text']"
            modelo_input = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            modelo_input.clear()
            modelo_input.send_keys("Orion")
        except Exception:
            print("Não foi possível alterar o modelo do produto")

        clicar_elemento(wait, By.CLASS_NAME, 'btn-salvar', "salvar anúncio")
        clicar_elemento(wait, By.CSS_SELECTOR, 'button[onclick="revisaoEnvio.enviar();"]', "enviar anúncio")
        
        finalizar_btn = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'btn-finalizar')))
        finalizar_btn = wait.until(EC.element_to_be_clickable(finalizar_btn))
        driver.execute_script("arguments[0].click();", finalizar_btn)
    except Exception as e:
        raise RuntimeError(f"Erro ao sincronizar no ML: {str(e)}") from e


# Função enviar para ml_full
def sincronizar_mkp_ml_full(driver: webdriver.Chrome):
    """Faz o envio/sincronização do produto para o Mercado Livre FULL

    Args:
        driver (webdriver.Chrome): Objeto de controle do Selenium

    Raises:
        RuntimeError: Ocorreu um erro ao interagir com algum elemento
    """
    wait = WebDriverWait(driver, 20)
    try:
        clicar_elemento(wait, By.CSS_SELECTOR, 'button.featured-action[original-title=" Enviar para o e-commerce"]', "Enviar para o e-commerce")

        select_elem = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#plataformaSincronizarProdutosEcommerce')))
        select = Select(select_elem)
        select.select_by_value("7609")

        clicar_elemento(wait, By.ID, "btn-interface-anuncios", "Continuar envio de produtos")

        actions = ActionChains(driver)
        move_element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "widget-dropdown-actions")))
        actions.move_to_element(move_element).perform()

        clicar_elemento(wait, By.CLASS_NAME, "checkbox-lote-anuncio", "checkbox anúncio")
        clicar_elemento(wait, By.CSS_SELECTOR, 'button.featured-action[original-title=" Utilizar descrição complementar do produto"]', "utilizar descrição complementar")
        clicar_elemento(wait, By.CLASS_NAME, "widget-dropdown-actions", "card anúncio")
        clicar_elemento(wait, By.CSS_SELECTOR, 'li[tab-anuncio="atributos"]', "ficha técnica")

        try:
            xpath = "//label[contains(text(), 'Marca')]/following-sibling::div[1]//div[contains(@class, 'input-group')]//input[@type='text']"
            marca_input = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            marca_input.clear()
            marca_input.send_keys("Orion")
        except RuntimeError:
            print("Não foi possível alterar a marca do produto")

        try:
            xpath = "//label[contains(text(), 'Modelo')]/following-sibling::div[1]//div[contains(@class, 'input-group')]//input[@type='text']"
            modelo_input = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            modelo_input.clear()
            modelo_input.send_keys("Orion")
        except RuntimeError:
            print("Não foi possível alterar o modelo do produto")

        clicar_elemento(wait, By.CLASS_NAME, 'btn-salvar', "salvar anúncio")
        clicar_elemento(wait, By.CSS_SELECTOR, 'button[onclick="revisaoEnvio.enviar();"]', "enviar anúncio")
        clicar_elemento(wait, By.CLASS_NAME, 'btn-finalizar', "finalizar")
    except Exception as e:
        raise RuntimeError (f"Erro ao sincronizar no ML_FULL: {str(e)}") from e


# Função enviar para magalu
def sincronizar_mkp_magalu(driver: webdriver.Chrome):
    """Faz o envio/sincronização do produto para o Magalu
    Args:
        driver (webdriver.Chrome): Objeto de controle do Selenium

    Raises:
        RuntimeError: Ocorreu um erro ao interagir com algum elemento
    """
    wait = WebDriverWait(driver, 20)
    try:
        clicar_elemento(wait, By.CSS_SELECTOR, 'button.featured-action[original-title=" Enviar para o e-commerce"]', "Enviar para o e-commerce")

        select_elem = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#plataformaSincronizarProdutosEcommerce')))
        select = Select(select_elem)
        select.select_by_value("7594")

        clicar_elemento(wait, By.ID, "btn-interface-anuncios", "Continuar envio de produtos")

        actions = ActionChains(driver)
        move_element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "widget-dropdown-actions")))
        actions.move_to_element(move_element).perform()

        clicar_elemento(wait, By.CLASS_NAME, "checkbox-lote-anuncio", "checkbox anúncio")
        clicar_elemento(wait, By.CSS_SELECTOR, 'button.featured-action[original-title=" Utilizar descrição complementar do produto"]', "utilizar descrição complementar")

        clicar_elemento(wait, By.CSS_SELECTOR, 'button[onclick="revisaoEnvio.enviar();"]', "enviar anúncio")

        finalizar_btn = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'btn-finalizar')))
        finalizar_btn = wait.until(EC.element_to_be_clickable(finalizar_btn))
        driver.execute_script("arguments[0].click();", finalizar_btn)
    except Exception as e:
        raise RuntimeError(f"Erro ao sincronizar no MAGALU: {str(e)}") from e


# Função sincronizar produto site - TINY
def sincronizar_produtos_sites(driver: webdriver.Chrome,
                              opencart:bool=False,
                              woocommerce:bool=False):
    """Sicroniza/Envia os produtos para plataformas de e-commerce selecionadas.

    Args:
        driver (webdriver.Chrome): Objeto de controle do Selenium
        opencart (bool, optional): Seleciona o opencart. Defaults to False.
        woocommerce (bool, optional): Seleciona o woocommercer. Defaults to False.
    """
    wait = WebDriverWait(driver, 20)
    plataformas = {
        "opencart": (opencart, "7673"),
        "woocommerce": (woocommerce, "7689"),
    }

    if not any([opencart, woocommerce]):
        raise ValueError('Nenhuma plataforma foi selecionada para sincronização.')

    for nome_plataforma, (deve_sincronizar, id_plataforma) in plataformas.items():
        if deve_sincronizar:
            try:
                print(f"Sincronizando com a plataforma: {nome_plataforma}...")
                clicar_elemento(wait, By.CSS_SELECTOR, 'button.featured-action[original-title=" Enviar para o e-commerce"]', "enviar para e-commerce")

                select_elem = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#plataformaSincronizarProdutosEcommerce')))
                select = Select(select_elem)
                select.select_by_value(id_plataforma)

                clicar_elemento(wait, By.CSS_SELECTOR, 'button#btnEnvioProdutoEcommercePopup', "botão avançar")
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#waitEnvioProdutoEcommercePopup.hide")))
                clicar_elemento(wait, By.CSS_SELECTOR, 'button#btnEnvioProdutoEcommercePopup', "botão avançar")
                # driver.execute_script("arguments[0].scrollIntoView(true);", avancar_btn_elem)
                # driver.execute_script("arguments[0].click();", avancar_btn_elem)

                clicar_elemento(wait, By.ID, 'btnFecharEnvioProdutoEcommercePopup', "botão fechar")
                print(f"Sincronização com {nome_plataforma} concluída.")
                driver.refresh()
            except Exception as e:
                raise RuntimeError(f"Erro ao sincronizar com {nome_plataforma}: {str(e)}") from e
