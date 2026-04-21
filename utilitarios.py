from configuracoes import ARQ_PARAMETROS, CAMINHO_DIRETORIO_CSV, INFORMACOES_ARQUIVOS_CSV
from pathlib import Path
import csv
import copy

def configurar_arquivos_csv():
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
    with open(caminho_arquivo, 'r', newline='', encoding='utf-8') as arquivo:
       leitor = csv.DictReader(arquivo)
       lista_conteudo = list(leitor)
    return lista_conteudo

def ler_colunas_csv(caminho_arquivo: str) -> list[str]:
    with open(caminho_arquivo, 'r', newline='', encoding='utf-8') as arquivo:
       leitor = csv.DictReader(arquivo)
       lista_colunas = leitor.fieldnames
    return lista_colunas

def escrever_csv(caminho_arquivo: str, lista_conteudo: list[dict]) -> None:
    lista_colunas = ler_colunas_csv(caminho_arquivo)
    with open(caminho_arquivo, 'w', encoding='utf-8', newline='') as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=lista_colunas, quoting=csv.QUOTE_ALL)
        escritor.writeheader()
        escritor.writerows(lista_conteudo)

def ler_parametros_csv() -> dict:
    lista_parametros = ler_csv(ARQ_PARAMETROS)
    dict_parametros = {}
    for linha in lista_parametros:
        parametro = linha['parametro']
        valor = linha['valor']
        dict_parametros[parametro] = valor
    return dict_parametros

def escrever_parametros_csv(dict_parametros: dict) -> None:
    lista_parametros = []
    for parametro, valor in dict_parametros.items():
        lista_parametros.append({'parametro': parametro, 'valor': valor})
    escrever_csv(ARQ_PARAMETROS, lista_parametros)

def chavear_dicionarios(lista_dicionarios: list[dict], coluna_chave: str) -> dict:
    dicionarios_chaveados = {}
    for dicionario in lista_dicionarios:
        chave = dicionario[coluna_chave]
        dicionarios_chaveados[chave] = copy.deepcopy(dicionario)
    return dicionarios_chaveados