from configuracoes import ARQ_PARAMETROS, ARQ_CARDS, CAMINHO_DIRETORIO_CSV, INFORMACOES_ARQUIVOS_CSV
from pathlib import Path
import csv
import copy

def configurar_arquivos_csv() -> None:
    """
    Verifica a existência do diretório e dos arquivos CSV base do sistema.
    Caso não existam, cria os arquivos com seus respectivos cabeçalhos (colunas)
    e valores iniciais definidos nas configurações.
    """
    caminho = Path(CAMINHO_DIRETORIO_CSV)
    caminho.mkdir(parents=True, exist_ok=True)

    for nome_arquivo, informacoes in INFORMACOES_ARQUIVOS_CSV.items():
        caminho_completo = caminho / nome_arquivo
        
        if not caminho_completo.exists():
            with open(caminho_completo, mode='w', newline='', encoding='utf-8') as arquivo_csv:
                escritor = csv.writer(arquivo_csv, quoting=csv.QUOTE_ALL)
                escritor.writerow(informacoes["colunas"])
                escritor.writerows(informacoes["linhas"])

def ler_csv(caminho_arquivo: str) -> list[dict]:
    """
    Lê um arquivo CSV e converte seu conteúdo em uma lista de dicionários.

    Args:
        caminho_arquivo (str): O caminho relativo ou absoluto para o arquivo CSV.

    Returns:
        list[dict]: Uma lista onde cada elemento é um dicionário representando uma linha do CSV.
    """
    with open(caminho_arquivo, 'r', newline='', encoding='utf-8') as arquivo:
       leitor = csv.DictReader(arquivo)
       return list(leitor)

def ler_colunas_csv(caminho_arquivo: str) -> list[str]:
    """
    Lê apenas a primeira linha (cabeçalho) de um arquivo CSV.

    Args:
        caminho_arquivo (str): O caminho para o arquivo CSV.

    Returns:
        list[str]: Uma lista contendo os nomes das colunas.
    """
    with open(caminho_arquivo, 'r', newline='', encoding='utf-8') as arquivo:
       leitor = csv.DictReader(arquivo)
       return leitor.fieldnames

def escrever_csv(caminho_arquivo: str, lista_conteudo: list[dict]) -> None:
    """
    Sobrescreve um arquivo CSV com novos dados passados em formato de lista de dicionários.

    Args:
        caminho_arquivo (str): O caminho do arquivo que será sobrescrito.
        lista_conteudo (list[dict]): Os dados estruturados a serem salvos.
    """
    if not lista_conteudo:
        lista_colunas = ler_colunas_csv(caminho_arquivo)
        lista_conteudo = []
    else:
        lista_colunas = list(lista_conteudo[0].keys())

    with open(caminho_arquivo, 'w', encoding='utf-8', newline='') as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=lista_colunas, quoting=csv.QUOTE_ALL)
        escritor.writeheader()
        escritor.writerows(lista_conteudo)

def ler_parametros_csv() -> dict:
    """
    Lê o arquivo de parâmetros do sistema (ex: último ID gerado) e o formata
    em um dicionário chave-valor simples.

    Returns:
        dict: Dicionário contendo os parâmetros atuais do sistema.
    """
    lista_parametros = ler_csv(ARQ_PARAMETROS)
    return {linha['parametro']: linha['valor'] for linha in lista_parametros}

def escrever_parametros_csv(dict_parametros: dict) -> None:
    """
    Recebe um dicionário de parâmetros e o converte de volta para o formato de 
    linhas para ser salvo no arquivo CSV de parâmetros.

    Args:
        dict_parametros (dict): Dicionário com os parâmetros atualizados.
    """
    lista_parametros = [{'parametro': p, 'valor': v} for p, v in dict_parametros.items()]
    escrever_csv(ARQ_PARAMETROS, lista_parametros)

def chavear_dicionarios(lista_dicionarios: list[dict], coluna_chave: str) -> dict:
    """
    Transforma uma lista de dicionários em um grande dicionário, usando uma 
    coluna específica como chave principal para facilitar buscas O(1).

    Args:
        lista_dicionarios (list[dict]): A lista contendo os dados.
        coluna_chave (str): O nome da coluna cujo valor será a chave no novo dicionário.

    Returns:
        dict: Dicionário mapeado pela coluna escolhida.
    """
    return {d[coluna_chave]: copy.deepcopy(d) for d in lista_dicionarios}

def obter_cards_por_assunto(assunto_desejado: str) -> list[dict]:
    """
    Filtra e retorna todos os cards associados a um assunto específico.
    Útil para isolar dados no momento do estudo.

    Args:
        assunto_desejado (str): O nome do assunto (ex: 'Engenharia de Requisitos').

    Returns:
        list[dict]: Uma lista contendo apenas os cards do assunto especificado.
    """
    todos_cards = ler_csv(ARQ_CARDS)
    return [card for card in todos_cards if card['assunto'] == assunto_desejado]