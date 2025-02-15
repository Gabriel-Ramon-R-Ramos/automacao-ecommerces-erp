# Importações
import os
import pandas as pd

# Função criar tabela de log - FUNÇÃO OBSOLETA
def criar_df_log() -> pd.DataFrame:
    """FUNÇÃO OBSOLETA. Cria uma dataframe do pandas para armazernar os erros durante o programa

    Returns:
        pd.DataFrame: Dataframe para armazernar os logs
    """
    logs_df = pd.DataFrame(columns=['ID', 'Erro'])
    return logs_df


# Função armazenar erro - FUNÇÃO OBSOLETA
def armazenar_erros(dtframe: pd.DataFrame, sku: str, error: str) -> pd.DataFrame:
    """FUNÇÃO OBSOLETA. Atualiza um Dataframe com os ID dos produtos e a descrições de todos
     os erros em except de produtos que acontecer.

    Args:
        dtframe (pd.DataFrame): DataFrame onde será armazenadas os logs
        sku (str): SKU do produto
        error (str): Mensagem de erro gerada pelo except

    Returns:
        pd.DataFrame: Dataframe com o erros atualizados
    """
    new_row = pd.DataFrame({'ID': [sku], 'Erro': [error]})
    dtframe = pd.concat([dtframe, new_row], ignore_index=True)

    return dtframe


def atualizar_status_csv(df: pd.DataFrame,
                         path_log: str,
                         sku: str,
                         column_name: str = "status") -> pd.DataFrame:
    """Atualiza o dataframe base para saber se a `ação desejada` foi feita ou não. Para arquivos CSV

    Args:
        df (pd.DataFrame): Dataframe que tenha uma coluna do tipo `str` para atualizar o status.\n
        Recomendo utilizar o Dataframe onde o SKU está sendo consultado pelo programa.
        path_log (str): Caminho do arquivo CSV que armazena os erros durante o programa.
        sku (str): SKU do produto que terá o status mudado.
        column_name (str): Nome da coluna que terá a verificação do status. Defaults to "status"

    Returns:
        pd.DataFrame: Dataframe com o status atualizado.
    """
    # Verifica se o arquivo existe e se não está vazio
    if os.path.exists(path_log) and os.path.getsize(path_log) > 0:
        logs_df = pd.read_csv(path_log, encoding="latin1")
    else:
        # Cria um DataFrame vazio com as colunas esperadas, caso seja necessário
        columns = ["asctime", "levelname", "message", "sku", "funcName", "lineno"]
        logs_df = pd.DataFrame(columns=columns)

    # Verifica o status e atualiza o DataFrame base
    if not logs_df.empty and sku in logs_df['sku'].values:
        df.loc[df['SKU'] == sku, column_name] = 'ERRO'
    else:
        df.loc[df['SKU'] == sku, column_name] = 'FEITO'

    return df


def atualizar_status_log(df: pd.DataFrame,
                         path_log: str,
                         sku: str,
                         column_name: str = "status") -> pd.DataFrame:
    """Atualiza o dataframe base para saber se a `ação desejada` foi feita ou não. Para arquivos LOG.

    Args:
        df (pd.DataFrame): Dataframe que tenha uma coluna do tipo `str` para atualizar o status.
        path_log (str): Caminho do arquivo LOG que armazena os erros durante o programa.
        sku (str): SKU do produto que terá o status mudado.
        column_name (str): Nome da coluna que terá a verificação do status. Defaults to "status"

    Returns:
        pd.DataFrame: Dataframe com o status atualizado.
    """
# Verifica se o arquivo de log existe e se não está vazio
    if os.path.exists(path_log) and os.path.getsize(path_log) > 0:
        # Lê o arquivo de log
        with open(path_log, 'r', encoding="utf-8") as log_file:
            logs = log_file.readlines()

        # Verifica se o SKU está presente no arquivo de log
        sku_encontrado = any(sku in line for line in logs)
        
        # Atualiza o status no DataFrame com base na verificação
        if sku_encontrado:
            df.loc[df['SKU'] == sku, column_name] = 'ERRO'
        else:
            df.loc[df['SKU'] == sku, column_name] = 'FEITO'
    else:
        # Se o arquivo não existir ou estiver vazio, assume como 'FEITO'
        df.loc[df['SKU'] == sku, column_name] = 'FEITO'

    return df
