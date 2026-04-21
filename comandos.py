from funcionalidades import adicionar_novos_cards, estudar_assunto, recriar_arquivos_csv

lista_comandos = [
    {
        'id': '0',
        'titulo': 'Sair',
        'funcao': None
    },
    {
        'id': '1',
        'titulo': 'Adicionar novos cards',
        'funcao': lambda: adicionar_novos_cards()
    },
    {
        'id': '2',
        'titulo': 'Estudar assunto',
        'funcao': lambda: estudar_assunto()
    },
    {
        'id': '100',
        'titulo': 'Recriar arquivos csv',
        'funcao': lambda: recriar_arquivos_csv()
    }
]

def exibir_menu() -> None:
    print('==== MENU ====')
    for comando in lista_comandos:
        print(f'{comando['id']} - {comando['titulo']}')

def executar_comando(id: str) -> None:
    comando_encontrado = False
    for comando in lista_comandos:
        if comando['id'] == id:
            comando_encontrado = True
            break

    if not comando_encontrado:
        print(f'O número de comando não é válido: {id}')
        return
    
    print(f'-----------------\nExecutando: {comando['titulo']}\n')
    funcao = comando['funcao']
    funcao()