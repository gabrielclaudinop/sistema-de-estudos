ARQ_ASSUNTOS = 'csv/assuntos.csv'
ARQ_CARDS = 'csv/cards.csv'
ARQ_PARAMETROS = 'csv/parametros.csv'
DIR_NOVOS_CARDS = 'novos-assuntos'
CAMINHO_DIRETORIO_CSV = 'csv'

INFORMACOES_ARQUIVOS_CSV = {
    'assuntos.csv': {
        'colunas': ['id', 'titulo'],
        'linhas': [
            ['0', '/@sem assunto/']
        ]
    },
    'cards.csv': {
        'colunas': ['id', 'frente', 'verso', 'assunto'],
        'linhas': []
    },
    'historico_revisoes.csv': {
        'colunas': ['id', 'id_card', 'dificuldade', 'data', 'data_proxima_revisao'],
        'linhas': []
    },
    'logs.csv': {
        'colunas': ['acao', 'funcao_desfazer'],
        'linhas': []
    },
    'parametros.csv': {
        'colunas': ['parametro', 'valor'],
        'linhas': [
            ['id_ultimo_card', '-1'],
            ['id_ultimo_assunto', '0']
        ]
    }
}