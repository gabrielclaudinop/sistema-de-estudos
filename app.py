from utilitarios import configurar_arquivos_csv
from comandos import exibir_menu, executar_comando

def main() -> None:
    """
    Função principal que gerencia o ciclo de vida da aplicação.
    Configura a infraestrutura inicial e mantém o loop do menu ativo
    até que o usuário opte por encerrar.
    """
    configurar_arquivos_csv()
    print("Sistema de Estudos Iniciado.")

    while True:
        exibir_menu()
        id_comando = input('\nDIGITE O NÚMERO DO COMANDO: ').strip()
        
        if id_comando == '0':
            print("Encerrando o sistema...")
            break
            
        executar_comando(id_comando)

if __name__ == '__main__':
    main()