from utilitarios import ler_csv, escrever_csv, ler_parametros_csv, escrever_parametros_csv, chavear_dicionarios, obter_cards_por_assunto, anexar_linha_csv
from configuracoes import ARQ_ASSUNTOS, ARQ_CARDS, DIR_NOVOS_CARDS, CAMINHO_DIRETORIO_CSV, INFORMACOES_ARQUIVOS_CSV
from datetime import datetime, timezone, timedelta
from collections import deque
from fsrs import Scheduler, Card, Rating
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
            'assunto': novo_card.get('assunto', '@sem assunto/')
        }
        
        cards.append(card)
        lista_novos_cards[i] = card

    dict_parametros['id_ultimo_card'] = str(id_ultimo_card)
    escrever_parametros_csv(dict_parametros)

    atualizar_assuntos(lista_novos_cards)
    escrever_csv(ARQ_CARDS, cards)
    print(f"{len(lista_novos_cards)} cards processados e adicionados com sucesso.")

def estudar_assuntos() -> None:
    """
    Inicia uma sessão de estudos. Permite ao utilizador indicar um prefixo de assunto
    e reconstrói o estado dos cards através do histórico para agendar e ordenar os estudos.
    """
    assunto_prefixo = input('Digite o assunto que deseja estudar (ex: "Ensino Fundamental/Matemática/"): ')

    if assunto_prefixo[-1] != '/':
        print("O nome do assunto deve terminar com /")
        return

    try:
        max_novos = int(input('Quantidade máxima de assuntos novos a estudar hoje: '))
    except ValueError:
        print("Valor inválido. Considerando 0 cards novos.")
        max_novos = 0

    todos_cards = ler_csv(ARQ_CARDS)
    cards_filtrados = [c for c in todos_cards if c['assunto'].startswith(assunto_prefixo)]

    if not cards_filtrados:
        print("Nenhum card encontrado com este prefixo de assunto.")
        return

    caminho_historico = Path(CAMINHO_DIRETORIO_CSV) / 'historico_revisoes.csv'
    historico_completo = ler_csv(str(caminho_historico)) if caminho_historico.exists() else []
    
    hist_por_card = {}
    for log in historico_completo:
        id_c = log['id_card']
        if id_c not in hist_por_card:
            hist_por_card[id_c] = []
        hist_por_card[id_c].append(log)

    scheduler = Scheduler()
    agora = datetime.now(timezone.utc)
    cards_revisao = []
    cards_novos = []

    print("\nCalculando estados e retenção a partir do histórico...")
    for c in cards_filtrados:
        card_fsrs = Card()
        logs = hist_por_card.get(c['id'], [])
        
        for log in logs:
            data_log = datetime.fromisoformat(log['data'])
            dificuldade = Rating(int(log['dificuldade']))
            card_fsrs, _ = scheduler.review_card(card_fsrs, dificuldade, data_log)

        item = {'dados': c, 'fsrs': card_fsrs}

        if not logs:
            cards_novos.append(item)
        else:
            if card_fsrs.due <= agora or c['id'] == '20':
                item['retencao'] = scheduler.get_card_retrievability(card_fsrs, agora)
                cards_revisao.append(item)

    cards_revisao.sort(key=lambda x: x['retencao'])
    cards_novos = cards_novos[:max_novos]

    fila = deque(cards_revisao + cards_novos)
    
    if not fila:
        print("Não tem cards pendentes para esse assunto hoje.")
        return

    print(f"\nIniciando: {len(cards_revisao)} a revisar, {len(cards_novos)} novos.\n")

    maior_id_hist = max([int(log['id']) for log in historico_completo]) if historico_completo else 0

    while fila:
        item = fila.popleft()
        card_csv = item['dados']
        card_fsrs = item['fsrs']

        print("-" * 45)
        print(f"Assunto: {card_csv['assunto']}")
        print(f"Frente:  {card_csv['frente']}")
        input("Pressione ENTER para revelar o verso...")
        print(f"Verso:   {card_csv['verso']}")
        
        while True:
            resp = input("Indique a dificuldade (1-Errei, 2-Difícil, 3-Bom, 4-Fácil): ").strip()
            if resp in ['1', '2', '3', '4']:
                break
            print("Opção inválida. Digite de 1 a 4.")
        
        rating = Rating(int(resp))
        agora_resp = datetime.now(timezone.utc)
        
        print()
        print(card_fsrs.due, scheduler.get_card_retrievability(card_fsrs, agora_resp + timedelta(days=1)))
        novo_card_fsrs, _ = scheduler.review_card(card_fsrs, rating, agora_resp)
        print(novo_card_fsrs.due, scheduler.get_card_retrievability(novo_card_fsrs, agora_resp + timedelta(days=1)))
        print()
        
        maior_id_hist += 1
        novo_log = {
            'id': str(maior_id_hist),
            'id_card': card_csv['id'],
            'dificuldade': resp,
            'data': agora_resp.isoformat()
        }
        
        anexar_linha_csv(str(caminho_historico), novo_log)
        
        item['fsrs'] = novo_card_fsrs
        if novo_card_fsrs.due - agora_resp < timedelta(hours=12):
            fila.append(item)
            print("[✓ O card voltará ao fim da fila para ser consolidado ainda hoje]")

    print("\nSessão de estudos concluída!")