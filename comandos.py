from funcionalidades import adicionar_novos_cards, recriar_arquivos_csv, estudar_assuntos

mapa_comandos = {
    '1': ('Adicionar novos cards', adicionar_novos_cards),
    '2': ('Estudar assuntos', estudar_assuntos),
    '100': ('Recriar arquivos csv', recriar_arquivos_csv)
}

def exibir_menu() -> None:
    """
    Itera sobre o mapa de comandos e exibe as opções disponíveis formatadas no terminal.
    """
    print('\n==== MENU ====')
    print('0 - Sair')
    
    for id_cmd, (titulo, _) in mapa_comandos.items():
        print(f'{id_cmd} - {titulo}')

def executar_comando(id_cmd: str) -> None:
    """
    Recebe o ID do comando digitado pelo usuário, busca a função associada 
    no dicionário `mapa_comandos` e a invoca.

    Args:
        id_cmd (str): O número do comando digitado.
    """
    comando = mapa_comandos.get(id_cmd)
    
    if not comando:
        print(f'O número de comando não é válido: {id_cmd}')
        return
    
    titulo, funcao = comando
    print(f'\n-----------------\nExecutando: {titulo}\n')
    funcao()