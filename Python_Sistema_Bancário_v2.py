#SISTEMA DO BANCO DO WILL
import os
import datetime

opcao = 0
valor_saldo = 1000
limite_maximo_saque = 3
limite_maximo_transacoes = 3
lista_extrato = ""
extrato = ""
usuarios = [["57691629451", "Filipe Breno Joaquim de Paula", "18/01/1967", ["Rua Poeta Lázaro, 711", "Coroadinho", "São Luís", "MA" ]],
            ["34668371629", "Levi Paulo Galvão", "19/07/1949", ["Rua Steiner Galli, 314", "Olaria", "Campo Grande", "MS"]],
            ["56781345902", "Filipe Augusto Costa", "25/12/1990", ["Rua Getúlio Vargas, 123", "Bairro Novo", "Fortaleza", "CE"]]]
lista_cpf = [item[0] for item in usuarios]
contas = []
menu_inicial = """
        =========================
        ||                     ||
        ||    BANCO DO WILL    ||
        ||                     ||
        ||     ___________     ||
        ||    |    | |    |    ||
        ||    |____| |____|    ||
        ||    |____|_|____|    ||
        =========================

               BEM VINDO!!!
        """
menu_final = """
        =========================
        ||                     ||
        ||    BANCO DO WILL    ||
        ||                     ||
        ||     ___________     ||
        ||    |    | |    |    ||
        ||    |____| |____|    ||
        ||    |____|_|____|    ||
        =========================

             VOLTE SEMPRE!!!
        """
menu = """
    BANCO WILL
        
    Escolha uma opção:
    1 - Depósito
    2 - Saque
    3 - Extrato
    4 - Cadastrar cliente
    5 - Listar clientes cadastrados
    6 - Criar nova conta
    7 - Listar contas cadastradas

    8 - Exit

    """


def Operacao_Deposito(valor_saldo, extrato, limite_maximo_transacoes, /):
    while True:    
        valor = input("Digite o valor a ser depositado: ")
        try:
            valor = float(valor)
        except ValueError:
            print("Valor Inválido. Digite um número válido")
            continue
        extrato = ""
        if valor > 0 and limite_maximo_transacoes > 0:
            data = datetime.datetime.now()
            valor_saldo += valor
            limite_maximo_transacoes -= 1
            extrato = f"{data.strftime('%d/%m/%Y %H:%M:%S')}  Depósito R$ {valor:.2f}\n"
            input(f"Depósito de R$ {valor:.2f} efetuado com sucesso!\nPressione Enter para continuar...") 
            return valor_saldo, extrato, limite_maximo_transacoes
        elif limite_maximo_transacoes <=0:
            print("Limite de transações excedido, tente a operação outro dia")
            input("Pressione Enter para continuar...")
            limite_maximo_transacoes -= 1
            return valor_saldo, extrato, limite_maximo_transacoes  
        else:
            print("Valor digitado inválido.")
            input("Pressione Enter para continuar...")

def Operacao_Saque(*, valor_saldo, limite_maximo_saque, limite_maximo_transacoes):
    while True:
        valor = input("Digite o valor desejado para saque: ")        
        try:
            valor = float(valor)
        except ValueError:
            print("Valor inválido. Digite um número válido.")
            continue
        extrato = ""
        if valor > 0 and valor <= 500 and valor <= valor_saldo and limite_maximo_saque > 0 and limite_maximo_transacoes > 0:
            data = datetime.datetime.now()
            valor_saldo -= float(valor)
            limite_maximo_saque -= 1
            limite_maximo_transacoes -= 1
            extrato = f"{data.strftime('%d/%m/%Y %H:%M:%S')}  Saque R$ {valor:.2f}\n"
            print(f"Saque de R$ {valor:.2f} realizado")
            input("Pressione Enter para continuar...")
            return valor_saldo, limite_maximo_saque, limite_maximo_transacoes, extrato
        elif valor > valor_saldo:
            print("Saldo insuficiente")
            input("Pressione Enter para continuar...")
            return valor_saldo, limite_maximo_saque, limite_maximo_transacoes, extrato
        elif valor > 500:
            print("Valor solicitado excede o limite de R$ 500.00.")
            input("Pressione Enter para continuar...")
            return valor_saldo, limite_maximo_saque, limite_maximo_transacoes, extrato
        elif limite_maximo_saque == 0:
            print("Limite de saque excedido")
            input("Pressione Enter para continuar...")
            return valor_saldo, limite_maximo_saque, limite_maximo_transacoes, extrato
        elif limite_maximo_transacoes <= 0:
            print("Limite de transações excedido, tente a operação outro dia")
            input("Pressione Enter para continuar...")
            limite_maximo_transacoes -= 1
            return valor_saldo, limite_maximo_saque, limite_maximo_transacoes, extrato            
        else:
            print("Valor Inválido")
            input("Pressione Enter para continuar...")
        return valor_saldo, limite_maximo_saque, limite_maximo_transacoes, extrato

def Operacao_Extrato(valor_saldo, /, *, lista_extrato):
    print("#"*20, " EXTRATO ", "#"*20)
    print("-"*41)
    print("NÂO HOUVE MOVIMENTAÇÂO" if not lista_extrato else lista_extrato)
    print(f"\nSaldo R$ {valor_saldo:.2f}.\n")
    print("#"*51)
    input("Pressione Enter para continuar...")

def Operacao_Criar_usuario(lista_cpf):
    print(lista_cpf)
    numero_Cpf = input("Digite somente os numeros do CPF: ")
    if lista_cpf.count(numero_Cpf) == 0:
        nome = input("Digite o nome do cliente: ")
        data_nascimento = input("Digite a data de nascimento (dd/mm/aaaa): ")
        logradouro = input("Digite o Logradouro: ")
        bairro = input("Digite o Bairro: ")
        cidade = input("Digite o nome da Cidade: ")
        estado = input("Digite a sigla do Estado: ")
        endereco = [logradouro, bairro, cidade, estado]
        cpf = [numero_Cpf, nome, data_nascimento, endereco]
        print("\nCadatro realizado com sucesso.")
        input("Pressione Enter para continuar...")
        return cpf
    else:
        print(f"Cliente com o CPF {numero_Cpf}, já tem cadastro.")
        input("Pressione Enter para continuar...")

def Operacao_listar_usuarios(usuarios):
    for usuario in usuarios:
        cpf = usuario[0]
        nome = usuario[1]
        data_nascimento = usuario[2]
        endereco = usuario[3]
        
        print(("=")*80, f"""
        Nome: {nome}
        CPF: {cpf}
        Data de Nascimento: {data_nascimento}
        Endereço: {endereco[0]}, Bairro {endereco[1]}, {endereco[2]} - {endereco[3]}
        """)
    input("Pressione Enter para continuar...")

def Buscador_de_usuarios(consulta, usuarios):
    if consulta.isdigit():
        for usuario in usuarios:
            if usuario[0] == consulta:
                return usuario  
        print("CPF não encontrado.")
        return None
    else:
        resultados = []
        for usuario in usuarios:
            if consulta.lower() in usuario[1].lower():
                resultados.append(usuario)
        
        if len(resultados) == 0:
            print("nenhum usuário encontrado com esse nome.")
            return None
        
        elif len(resultados) == 1:
            return resultados[0]
        
        else:
            print("\nUsuários encontrados:")
            for i, usuario in enumerate(resultados, 1):
                print(f"{i} - Nome: {usuario[1]}, CPF: {usuario[0]}")
            
            opcao = input("\nDigite o numero do usuário desejado ou 0 para voltar ao menu anterior: ")

            try:
                opcao = int(opcao)
                if opcao == 0:
                    return None
                elif 1 <= opcao <= len(resultados):
                    return resultados[opcao - 1]
                else:
                    print("Opção inválida. Voltando ao menu anterior.")
                    return None
            except ValueError:
                print("Entrada inválida. Vontando ao menu anterior.")
                return None

def gerar_numero_conta(contas):
    if contas:
        ultimo_numero_conta = int(contas[-1]["numero_conta"])
        return f"{ultimo_numero_conta + 1:04d}"
    else:
        return "0001"  # Se não houver contas, começa com 0001

def criar_conta(usuario, contas):
    numero_conta = gerar_numero_conta(contas)
    agencia = "0001"

    conta = {
        "cpf": usuario[0],
        "nome": usuario[1],
        "agencia": agencia,
        "numero_conta": numero_conta
        }
    
    return conta

def Operacao_criar_conta(usuarios, contas):
    print("""
          Selecione o cliente para criar a conta:

          1 - Buscar cliente por CPF
          2 - Buscar cliente por nome
          """)
    opcao = input("Selecione a opção: ")
    if opcao == "1":
        consulta = input("Digite o número do CPF (Apenas números): ")
        usuario = Buscador_de_usuarios(consulta, usuarios)

        if usuario:
            print("Usuário encontrado, criando conta...")
            nova_conta = criar_conta(usuario, contas)
            contas.append(nova_conta) 
            print("\nConta criada com sucesso:")
            print(f"Nome: {nova_conta['nome']}")
            print(f"CPF: {nova_conta['cpf']}")
            print(f"Número da conta: {nova_conta['numero_conta']}")
            print(f"Agência: {nova_conta['agencia']}")
            input("Pressione Enter para continuar...")    
        else:
            print("CPF não encontrado, o usuário deve ser cadastrado.")
            input("Pressione Enter para continuar...")
        
    elif opcao == "2":
        consulta = input("Digite o nome do cliente: ")
        usuario = Buscador_de_usuarios(consulta, usuarios)

        if usuario:
             print(f"Usuário selecionado:\nNome: {usuario[1]}\nCPF: {usuario[0]}\nData de Nascimento: {usuario[2]}")
             print("Usuário encontrado, criando conta...")
             nova_conta = criar_conta(usuario, contas)
             contas.append(nova_conta) 
             print("\nConta criada com sucesso:")
             print(f"Nome: {nova_conta['nome']}")
             print(f"CPF: {nova_conta['cpf']}")
             print(f"Número da conta: {nova_conta['numero_conta']}")
             print(f"Agência: {nova_conta['agencia']}")
             input("Pressione Enter para continuar...")
        else:
            print("Nenhum usuário selecionado ou encontrado.")

def Operacao_listar_contas(contas):
    if len(contas) > 0:
        for conta in contas:
            cpf = conta['cpf']
            nome = conta['nome']
            agencia = conta['agencia']
            numero_conta = conta['numero_conta']

            print(("=")*80, f"""
Nome: {nome}
CPF: {cpf}
Agência: {agencia}
Numero da Conta: {numero_conta}
                """)
    else:
        print("NÃO HÁ CONTAS CADASTRADAS.")
    input("Pressione Enter para continuar...")

def limpar_terminal():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

print(menu_inicial)
input("Pressione Enter para continuar...")
limpar_terminal()

while True:
    opcao = input(menu)
    limpar_terminal()        
    try:
        opcao = float(opcao)
    except ValueError:
        print("Valor inválido. Digite um número válido.")
        continue

    if opcao == 1: # Operação Depósito
        valor_saldo, extrato, limite_maximo_transacoes = Operacao_Deposito(valor_saldo, extrato, limite_maximo_transacoes)
        if limite_maximo_transacoes >= 0:
            lista_extrato += extrato
        limpar_terminal()
    elif opcao == 2: # Operação Saque
        valor_saldo, limite_maximo_saque, limite_maximo_transacoes, extrato = Operacao_Saque(valor_saldo=valor_saldo, limite_maximo_saque=limite_maximo_saque, limite_maximo_transacoes=limite_maximo_transacoes)
        if limite_maximo_transacoes >= 0:
            lista_extrato += extrato
        limpar_terminal()
    elif opcao == 3: # Operação Extrato
        Operacao_Extrato(valor_saldo, lista_extrato=lista_extrato)
        limpar_terminal()
    elif opcao == 4: # Operação Criar Extrato
        novo_usuario = Operacao_Criar_usuario(lista_cpf)
        if novo_usuario is not None:
            usuarios.append(novo_usuario)
            lista_cpf = [item[0] for item in usuarios]
            lista_usuarios = [item[1] for item in usuarios]
        limpar_terminal()
    elif opcao == 5: # Operação Listar Usuários
        Operacao_listar_usuarios(usuarios)
        limpar_terminal()
    elif opcao == 6: # Operação Criar Conta
        Operacao_criar_conta(usuarios, contas)
    elif opcao == 7: # Operação Listar contas
        Operacao_listar_contas(contas)
    elif opcao == 8: # Operação Menu Final
        print(menu_final)
        break
    else:
        print("Opção Inválida. Tente novamente!")
        