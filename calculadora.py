import sqlite3  # importe do banco de dados
import os  # importe para funções do sistema operacional
import unittest  # importe para testes unitários
import datetime as date  # importe para trabalhar com datas

banco = sqlite3.connect('divulga_tudo.bd')  # Variável global que estabelece a conexão com o banco de dados

CLICK_POR_VIEW = 12 / 100  # constante referente a quantos views são necessários para 1 click
SHARE_POR_CLICK = 3 / 20  # constante referente a quantos clicks são necessários para 1 share
VIEW_POR_INVESTIMENTO = 30  # constante referente ao fator de que 1 unidade monetária representa 30 views
MAX_SHARE = 4  # constante referente ao máximo de compartilhamentos de um anúncio


def configurar_o_banco():
    """
    A função configurar_o_banco tem como objetivo verificar se as tabelas já existem no banco, caso não cria-las, caso
    sim, chamar a função main para dar incio no sistema!
    :return:
    """
    try:
        cursor = banco.cursor()
        cursor.execute("CREATE TABLE clientes (cpf BIGINT(12) NOT NULL, nome VARCHAR(50)NULL DEFAULT NULL, PRIMARY KEY("
                       "cpf))")
        cursor.execute("""CREATE TABLE orcamentos (ID INTEGER PRIMARY KEY AUTOINCREMENT,nome_anuncio VARCHAR(50) NULL 
           DEFAULT NULL, data_inicio VARCHAR(11) NOT NULL, data_fim VARCHAR(11) NOT NULL, invest_por_dia FLOAT(20) 
           NOT NULL, invest_total FLOAT(20) NOT NULL, cpf BIGINT(11) NOT NULL, max_view INT(20) NOT NULL, max_clic 
           INT(20) NOT NULL, max_share INT(20) NOT NULL, FOREIGN KEY(cpf) REFERENCES clientes(cpf))""")
        banco.commit()
        main()
    except sqlite3.OperationalError:
        main()


def insert_in_cliente(valor_cpf, valor_nome):
    """ Recebe dois parâmetros e insere eles no banco de dados

    :param valor_cpf: str
    :param valor_nome: str
    :return:
    """
    cursor = banco.cursor()
    cursor.execute("INSERT INTO clientes (cpf, nome) VALUES (" + valor_cpf + ",'" + valor_nome + "')")
    banco.commit()


def insert_dados_orcamento(nome_anuncio, data_inicio, data_fim, invest_por_dia, invest_total, cpf, view, max_clic,
                           max_share):
    """
    Recebe nove parâmetros e insere eles no banco de dados!

    :param view: float
    :param nome_anuncio: str
    :param data_inicio: str
    :param data_fim: str
    :param invest_por_dia: float
    :param invest_total: float
    :param cpf: int
    :param max_clic: float
    :param max_share: float
    :return:
    """
    cursor = banco.cursor()
    cursor.execute(
        "INSERT INTO orcamentos (nome_anuncio, data_inicio, data_fim, invest_por_dia, invest_total, cpf, max_view, "
        "max_clic, max_share) VALUES ('" + nome_anuncio + "','" + data_inicio + "','" + data_fim + "'," + str(
            invest_por_dia) + "," + str(invest_total) + ", " + cpf + ", " + str(view) + ", " + str(
            max_clic) + ", " + str(max_share) + ")")
    banco.commit()


def select_dados_cpf(cpf):
    """
    Faz a busca no banco de dados a partir do parâmetro recebido e retorna na tela os valores buscados, sendo eles:
    O nome do anúncio; o ID do anúncio; Datas de início e fim; Valor por dia e total; Máximo de visualizações, cliques e
    compartilhamentos.
    :param cpf: str
    :return:
    """
    cursor = banco.cursor()
    cursor.execute(
        "SELECT id, nome_anuncio, data_inicio, data_fim, invest_por_dia, invest_total, cpf, max_view, max_clic,"
        " max_share FROM orcamentos where orcamentos.cpf = '" + cpf + "' ")
    linhas = cursor.fetchall()
    print('\n')
    print(f"O(s) orçamento(s) cadastrado(s) nesse CPF é(são):")
    for linha in linhas:
        print('\n\n')
        print(f"Nome do anuncio: {linha[1]}.")
        print(f'ID do anúncio: {linha[0]}.')
        print(f'Data de início do anúncio: {linha[2]} e a data de fim do anúncio é {linha[3]}.')
        print(f'O investimento por dia do anúncio foi de: R${linha[4]:.2f}, e o investimento total foi de: '
              f'R${linha[5]:.2f}!')
        print(f'O máximo de visualizações no final do período é de {linha[7]:.0f}, o máximo de cliques é: '
              f'{linha[8]:.0f}'
              f'e o máximo de compartilhamentos é: {linha[9]:.0f}.')
    print('\n Fim dos orçamentos! ')
    print('\n')


def select_dados_data(data_inicio, data_fim):
    """
    Faz a busca no banco de dados a partir do parâmetro recebido e retorna na tela os valores buscados, sendo eles:
    O nome do anúncio; o ID do anúncio; Datas de início e fim; Valor por dia e total; Máximo de visualizações, cliques e
    compartilhamentos.
    :param data_inicio: str
    :param data_fim: str
    :return:
    """
    cursor = banco.cursor()
    cursor.execute("SELECT clientes.nome, orcamentos.ID, orcamentos.nome_anuncio, orcamentos.data_inicio, "
                   "orcamentos.data_fim, orcamentos.invest_por_dia, orcamentos.invest_total, orcamentos.cpf, "
                   "orcamentos.max_view, orcamentos.max_clic, orcamentos.max_share FROM orcamentos INNER JOIN "
                   "clientes ON clientes.cpf = orcamentos.cpf WHERE orcamentos.data_inicio = '" + data_inicio + "' "
                   "AND orcamentos.data_fim = '" + data_fim + "'")
    linhas = cursor.fetchall()
    print('\n')
    print(f"O(s) orçamento(s) cadastrado(s) com as respectivas datas de incio e fim é(são):")
    for linha in linhas:
        print('\n')
        print(f'Nome do Cliente: {linha[0]}.')
        print(f"Nome do anuncio: {linha[2]}.")
        print(f'ID do anúncio: {linha[1]}.')
        print(f'Data de início do anúncio: {linha[3]} e a data de fim do anúncio é {linha[4]}.')
        print(f'O investimento por dia do anúncio foi de: R${linha[5]:.2f}, e o investimento total foi de: '
              f'R${linha[6]:.2f}!')
        print(f'O máximo de visualizações no final do período é de {linha[8]:.0f}, o máximo de cliques é: '
              f'{linha[9]:.0f}'
              f' e o máximo de compartilhamentos é: {linha[10]:.0f}.')

    print('\n Fim dos orçamentos! ')

    print('\n')


class UnitTest(unittest.TestCase):
    def test_contador(self):
        """Função para testar o funcionamento da função contador_de_view.

        :return:
        """
        contador = contador_de_view(3000)
        self.assertEqual(2160.0, contador)

    def test_max_view(self):
        """Função para testar o funcionamento da função max_view.

        :return:
        """
        test_max = max_view(3000.0, MAX_SHARE)
        self.assertEqual(8641.159679999999, test_max)

    def test_contador_de_click(self):
        """Função para testar o funcionamento da função contador_de_click.

        :return:
        """
        test_clic = contador_de_click(100)
        self.assertEqual(12, test_clic)

    def teste_contador_de_share(self):
        """ Função para testar o funcionamento da função contador_de_share.

        :return:
        """
        test_share = contador_de_share(300)
        self.assertEqual(5.3999999999999995, test_share)

    def test_contador_de_dias(self):
        """Função para testar o funcionamento da função contador_de_dias.

        :return:
        """
        test_dias = contador_de_dias('26/02/200', '30/02/2000')
        self.assertEqual(5, test_dias)


def contador_de_view(entrada):
    """A função contador_de_view recebe um valor referente a quantidade de visualizações recebidas e retorna a
    quantidade de visualizações após a sequência de compartilhamentos.

    :param entrada: float
    :return: float
    """

    quantidade_de_click = entrada * CLICK_POR_VIEW
    quantidade_de_share = quantidade_de_click * SHARE_POR_CLICK
    view_por_share = quantidade_de_share * 40
    return view_por_share


def max_view(entrada, max_share=MAX_SHARE):
    """A função max_view maximiza o número de views que o anúncio pode ter utilizando a função contador_de_view e
    de acordo com a MAX_SHARE. Retorna a soma (ou como chamado, montante) do máximo de views.

    :param entrada: float
    :param max_share: constant :int
    :return:float
    """
    if max_share == 0:
        return 0

    montante_de_view = entrada
    rodada = entrada

    for i in range(max_share):
        rodada = contador_de_view(rodada)
        montante_de_view += rodada
        if i > max_share:
            print('Error!')
            break
    return montante_de_view


def contador_de_click(entrada):
    """ Essa função tem o objetivo de contar a quantidade de cliques em um anuncio a partir do valor de entrada, que
    consiste na multiplicação do valor investido pela constante VIEW_POR_INVESTIMENTO

    :param entrada: float
    :return: float
    """
    quantidade_de_click = entrada * CLICK_POR_VIEW
    return quantidade_de_click


def contador_de_share(entrada):
    """ Essa função tem o objetivo de contar a quantidade de compartilhamentos em um anuncio a partir do valor de
    entrada, que consiste na multiplicação do valor investido pela constante VIEW_POR_INVESTIMENTO e depois multiplicado
    pela constante SHARE_POR_CLICK

    :param entrada:
    :return: int
    """
    quantidade_de_share = contador_de_click(entrada) * SHARE_POR_CLICK
    return quantidade_de_share


def contador_de_dias(date_inc, date_fim):
    """ Essa função recebe duas datas sendo a primeira de início e a segunda de fim e retorna a diferença de dias entre
    elas.

    :param date_inc: str
    :param date_fim: str
    :return: int
    """
    date1 = date.datetime.strptime(date_inc, '%d/%m/%Y')
    date2 = date.datetime.strptime(date_fim, '%d/%m/%Y')
    if date1 == date2:
        quantidade_dias = 1
    else:
        quantidade_dias = 1 + abs((date2 - date1).days)
    return quantidade_dias


def decisao_por_pesquisar(decisao3):
    """
    A função decisao_por_pesquisa faz select's no banco de dados de acordo com a escolha do usuário, retornando para
    tela tanto a busca por CPF ou por data!
    :param decisao3:
    :return:
    """
    if decisao3 == 1:
        os.system("cls")
        cpf = str(input('Qual o CPF do cliente? (apenas números): '))
        select_dados_cpf(cpf)
        main()

    if decisao3 == 2:
        os.system("cls")
        data_de_inicio = str(input('Digite a data de incio da publicação (dd/mm/aaaa): '))
        data_de_fim = str(input('Digite a data de termino da publicação (dd/mm/aaaa): '))
        select_dados_data(data_de_inicio, data_de_fim)
        main()

    if decisao3 == 0:
        quit()


def decisao_por_orcamento(segunda_decisao):
    """Assim como as outras funções de decisão, a função decisão_por_orcamento recebe o valor de uma decisão do usuário
    e realiza uma das ações propostas, sendo elas: Cadastrar o cliente ou cadastrar um orçamento.
    :param segunda_decisao:
    :return:
    """
    if segunda_decisao == 0:
        quit()

    if segunda_decisao == 1:
        os.system("cls")
        cpf = str(input('Por favor, digite o CPF do cliente (apenas números): '))
        nome = str(input('Por favor, digite o nome do cliente: '))
        insert_in_cliente(cpf, nome)
        print('Cadastro realizado com sucesso!')
        print('Você deseja iniciar o cadastro do anúncio? Digite 1 para SIM, 2'
              ' para voltar ao início ou 0 para encerrar o programa!')
        decisao_orcamento = int(input('Resposta: '))
        if decisao_orcamento == 1:
            decisao_por_orcamento(segunda_decisao=2)
        if decisao_orcamento == 2:
            os.system("cls")
            main()
        if decisao_orcamento == 0:
            quit()

    if segunda_decisao == 2:
        os.system("cls")
        cpf = str(input('Qual o CPF do cliente? (apenas números): '))
        nome_do_anuncio = str(input('Digite o nome do anuncio: '))
        valor_investido_por_dia = float(input('Digite o valor do investimento diário: R$ '))
        data_de_inicio = str(input('Digite a data de incio da publicação (dd/mm/aaaa): '))
        data_de_fim = str(input('Digite a data de termino da publicação (dd/mm/aaaa): '))
        view_por_investimento = valor_investido_por_dia * VIEW_POR_INVESTIMENTO
        valor_total_investido = contador_de_dias(data_de_inicio, data_de_fim) * valor_investido_por_dia
        qnt_max_de_views = max_view(view_por_investimento, MAX_SHARE) * contador_de_dias(data_de_inicio,
                                                                                         data_de_fim)
        qnt_max_de_cliques = contador_de_click(view_por_investimento) * contador_de_dias(data_de_inicio,
                                                                                         data_de_fim)
        qnt_max_de_share = contador_de_share(view_por_investimento) * contador_de_dias(data_de_inicio, data_de_fim)
        insert_dados_orcamento(nome_do_anuncio, data_de_inicio, data_de_fim, valor_investido_por_dia,
                               valor_total_investido, cpf, qnt_max_de_views, qnt_max_de_cliques,
                               qnt_max_de_share)

        print('Orçamento realizado com sucesso!')
        print('\n')
        print(f'O nome do anúncio é: {nome_do_anuncio}. ')
        print(f'O valor investido por dia foi de: R${valor_investido_por_dia:.2f}. ')
        print(f'Esse valor, investido por {contador_de_dias(data_de_inicio, data_de_fim)} dias, somou o total de '
              f'R${valor_total_investido:.2f}. ')
        print(f'A data de início foi: {data_de_inicio} e o fim foi da publicação foi {data_de_fim}. ')
        print(f'A somatória de visualizações foi de {qnt_max_de_views:.0f}, de clicks foi de: '
              f'{qnt_max_de_cliques:.0f} '
              f'e de compartilhamentos foi de {qnt_max_de_share:.0f}. ')
        print('\n\nFim do cadastro!\n')

        print('Para voltar ao início, digite 1 ou para encerrar digite 0')
        ficar_ou_nao = int(input('Resposta: '))
        if ficar_ou_nao == 1:
            os.system("cls")
            main()
        if ficar_ou_nao == 0:
            quit()


def decisao_inicial(decisao1):
    """ Recebe como parâmetro a decisão registrada na função main, e encaminha o sistema para o destino dessa decisão.
    Assim, encaminhando para a pesquisa no banco ou para o cadastro no banco.

    :param decisao1:
    :return:
    """
    if decisao1 == 1:
        os.system("cls")
        print('O que voce deseja?\n')
        print('Digite 1 para: Pesquisar por CPF do cliente')
        print('Digite 2 para: Pesquisar por data do anúncio')
        decisao3 = int(input('Resposta: '))
        decisao_por_pesquisar(decisao3)

    if decisao1 == 2:
        os.system("cls")
        print('O que voce deseja?\n')
        print('Digite 1 para: Cadastrar um novo cliente!')
        print('Digite 2 para: Realizar um orçamento! (Apenas se o Cliente já foi cadastrado!)')
        segunda_decisao = int(input('Resposta: '))
        decisao_por_orcamento(segunda_decisao)

    if decisao1 == 0:
        quit()


def main():
    """
    A função main monta a primeira decisão que o usuário deve tomar, se ele deseja fazer uma busca ou um orçamento!
    :return:
    """
    print('Olá!')
    print('Digite 1 para PESQUISAR POR UM ORÇAMENTO ou digite 2 para FAZER UM ORÇAMENTO!')
    print('Ou se preferir, digite em qualquer resposta \'0\' para encerrar o sistema!\n')
    decisao1 = int(input('Resposta: '))
    decisao_inicial(decisao1)


configurar_o_banco()  # Incio

#  Codificado pelo candidato: Marcus Alexsander Ribeiro Vasconcelos --
#  Corresponde a parte 2 do desafio para Academia Capgemini. "Uma calculadora de alcance de anúncio online." --
