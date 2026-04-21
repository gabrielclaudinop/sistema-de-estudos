from utilitarios import configurar_arquivos_csv

configurar_arquivos_csv()

from comandos import exibir_menu, executar_comando

while True:
    exibir_menu()
    id_comando = input('\nDIGITE O NÚMERO DO COMANDO: ')
    if id_comando == '0':
        break
    executar_comando(id_comando)
    print()