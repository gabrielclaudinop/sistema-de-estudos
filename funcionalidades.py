from utilitarios import ler_csv, escrever_csv, ler_parametros_csv, escrever_parametros_csv, chavear_dicionarios, obter_cards_por_assunto
from configuracoes import ARQ_ASSUNTOS, ARQ_CARDS, DIR_NOVOS_CARDS, CAMINHO_DIRETORIO_CSV, INFORMACOES_ARQUIVOS_CSV
from pathlib import Path
import csv

def recriar_arquivos_csv() -> None:
    """
    Função de manutenção para formatar e recriar os arquivos CSV, apagando seus dados.
    O usuário pode digitar 'TODOS' ou listar arquivos específicos separados por espaço.
    """
    caminho = Path(CAMINHO_DIRETORIO_CSV)
    arquivos_recriar = input('Quais arquivos você deseja recriar? (Sintaxe: TODOS | arq1.csv arq2.csv ...)\n').split()

    for nome_arquivo, informacoes in INFORMACOES_ARQUIVOS_CSV.items():
        caminho_completo = caminho / nome_arquivo

        if 'TODOS' in arquivos_recriar or nome_arquivo in arquivos_recriar:
            with open(caminho_completo, mode='w', newline='', encoding='utf-8') as arquivo_csv:
                escritor = csv.writer(arquivo_csv, quoting=csv.QUOTE_ALL)
                escritor.writerow(informacoes["colunas"])
                escritor.writerows(informacoes["linhas"])
    print("\nArquivos recriados de acordo com a seleção.")

def atualizar_assuntos(cards: list[dict]) -> None:
    """
    Verifica a lista de novos cards e adiciona os nomes de assuntos inéditos
    à tabela de 'assuntos.csv'.

    Args:
        cards (list[dict]): A lista de novos cards recém-processados.
    """
    lista_assuntos = ler_csv(ARQ_ASSUNTOS)
    dict_parametros = ler_parametros_csv()
    
    id_ultimo_assunto = int(dict_parametros.get('id_ultimo_assunto', 0))
    dict_assuntos = chavear_dicionarios(lista_assuntos, 'titulo')

    for card in cards:
        assunto = card['assunto']
        if assunto not in dict_assuntos:
            id_ultimo_assunto += 1
            dict_assuntos[assunto] = {'id': str(id_ultimo_assunto), 'titulo': assunto}
            
    assuntos = sorted(dict_assuntos.values(), key=lambda d: d['titulo'])
    
    dict_parametros['id_ultimo_assunto'] = str(id_ultimo_assunto)
    escrever_parametros_csv(dict_parametros)
    escrever_csv(ARQ_ASSUNTOS, assuntos)

def adicionar_novos_cards(arquivo_com_novos_cards: str | None = None) -> None:
    """
    Lê um arquivo CSV contendo novos flashcards e os integra ao banco de dados principal.
    
    Inicializa os cards com os parâmetros exigidos pela API 6.x do FSRS (estabilidade, 
    dificuldade e estado) para que estejam prontos para o algoritmo de repetição.

    Args:
        arquivo_com_novos_cards (str | None): O nome do arquivo a ser importado.
                                              Se None, solicita o nome via input.
    """
    if not arquivo_com_novos_cards:
        arquivo_com_novos_cards = input(f'Digite o nome do arquivo com os novos cards (deve estar no diretório {DIR_NOVOS_CARDS}/): ')
    
    caminho_novos_cards = Path(DIR_NOVOS_CARDS) / arquivo_com_novos_cards

    if not caminho_novos_cards.exists():
        print(f'Arquivo inexistente: {caminho_novos_cards}')
        return

    lista_cards = ler_csv(ARQ_CARDS)
    lista_novos_cards = ler_csv(str(caminho_novos_cards))
    
    dict_parametros = ler_parametros_csv()
    id_ultimo_card = int(dict_parametros.get('id_ultimo_card', -1))

    cards = lista_cards.copy()
    
    for i, novo_card in enumerate(lista_novos_cards):
        id_ultimo_card += 1
        
        card = {
            'id': str(id_ultimo_card),
            'frente': novo_card['frente'],
            'verso': novo_card['verso'],
            'assunto': novo_card.get('assunto', '@sem assunto/'),
            'estado': 'Novo',
            'estabilidade': '0',
            'dificuldade': '0',
            'data_proxima_revisao': ''
        }
        
        cards.append(card)
        lista_novos_cards[i] = card

    dict_parametros['id_ultimo_card'] = str(id_ultimo_card)
    escrever_parametros_csv(dict_parametros)

    atualizar_assuntos(lista_novos_cards)
    escrever_csv(ARQ_CARDS, cards)
    print(f"{len(lista_novos_cards)} cards processados e adicionados com sucesso.")