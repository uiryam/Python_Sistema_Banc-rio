#SISTEMA DO BANCO DO WILL
import os
from datetime import datetime
from abc import ABC, abstractclassmethod, abstractproperty

opcao = 0
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


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
    
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

    def __str__(self):
        return (f"Nome: {self.nome}\n"
                f"CPF: {self.cpf}\n"
                f"Data de Nascimento: {self.data_nascimento}\n"
                f"Endereço: {', '.join(self.endereco)}")

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._clinete = cliente
        self._historico = Historico()
    
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._clinete
    
    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("operação felhou! sem saldo suficiente")

        elif valor > 0:
            self._saldo -= valor
            print("Saque realizado!")
            return True
        
        else:
            print("Valor invalido")
            return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("Depósito realizado!")
        else:
            print("valor errado")
            return False
        return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao ["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self.limite
        excedeu_saque = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("valor de saque excedido")
            input("Pressione Enter para continuar...")

        elif excedeu_saque:
            print("numero de saques excedido")
            input("Pressione Enter para continuar...")
        
        else:
            return super().sacar(valor)
        
        return False
    
    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

class Historico:
    def __init__(self):
        self._transacoes = []
    
    @property
    def transacoes(self):
        return self._transacoes
        
    def adicionar_transacao(self, transacao):
        self.transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractproperty
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("Cliente não possui conta")
        input("Pressione Enter para continuar...")
        return
    
    return cliente.contas[0]

def filtrar_cliente(clientes, cpf=0, nome=None):
    if cpf != 0:
        clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
        return clientes_filtrados[0] if clientes_filtrados else None
    elif nome is not None:
        clientes_filtrados = [cliente for cliente in clientes if nome.lower() in cliente.nome.lower()]
        limpar_terminal()
        if not clientes_filtrados:
            print("Nenhum usuário encontrado com esse nome.")
            input("Pressione Enter para continuar...")
        
        elif len(clientes_filtrados) == 1:
            return clientes_filtrados[0]
        
        else:
            print("\nUsuários encontrados:")
            for i, cliente in enumerate(clientes_filtrados, 1):
                print(f"{i} - Nome: {cliente.nome}, CPF: {cliente.cpf}")
            
            opcao = input("\nDigite o numero do usuário desejado ou 0 para voltar ao menu anterior: ")

            try:
                opcao = int(opcao)
                if opcao == 0:
                    return None
                elif 1 <= opcao <= len(clientes_filtrados):
                    return clientes_filtrados[opcao - 1]
                else:
                    print("Opção inválida. Voltando ao menu anterior.")
                    input("Pressione Enter para continuar...")
                    return None
            except ValueError:
                print("Entrada inválida. Vontando ao menu anterior.")
                input("Pressione Enter para continuar...")
                return None

def depositar(clientes):
    cpf = input("Digite o número do CPF do cliente: ")
    cliente = filtrar_cliente(clientes, cpf)
    if not cliente:
        print("Cliente não encontrado")
        input("Pressione Enter para continuar...")
        return
    
    if not cliente.contas:
        print("\nCliente não possui contas cadastradas!")
        input("Pressione Enter para continuar...")
        return

    if len(cliente.contas) > 1:
        print("\nCliente possui mais de uma conta.")
        print("Selecione a conta para depositar:")
        for i, conta in enumerate(cliente.contas, 1):
            print(f"{i} - Conta número: {conta.numero}, Saldo: R$ {conta.saldo:.2f}")

        opcao = input("Escolha o número da conta ou 0 para cancelar: ")

        try:
            opcao = int(opcao)
            if opcao == 0:
                print("Operação cancelada.")
                return
            elif 1 <= opcao <= len(cliente.contas):
                conta_selecionada = cliente.contas[opcao - 1]
            else:
                print("Opção inválida.")
                return
        except ValueError:
            print("Entrada inválida.")
            return
    else:
        conta_selecionada = cliente.contas[0]

    valor = float(input("Informe o valor a ser depositado: "))
    transacao = Deposito(valor)

    cliente.realizar_transacao(conta_selecionada, transacao)
    print(f"Depósito de R$ {valor:.2f} realizado com sucesso na conta {conta_selecionada.numero}!")
    input("Pressione Enter para continuar...")

def sacar(clientes):
    cpf = input("Informe o número do CPF do cliente: ")
    cliente = filtrar_cliente(clientes, cpf)

    if not cliente:
        print("\nCliente não encontrado!")
        input("Pressione Enter para continuar...")
        return
    if not cliente.contas:
        print("\nCliente não possui contas cadastradas!")
        input("Pressione Enter para continuar...")
        return

    if len(cliente.contas) > 1:
        print("\nCliente possui mais de uma conta.")
        print("Selecione a conta para sacar:")
        for i, conta in enumerate(cliente.contas, 1):
            print(f"{i} - Conta número: {conta.numero}, Saldo: R$ {conta.saldo:.2f}")

        opcao = input("Escolha o número da conta ou 0 para cancelar: ")

        try:
            opcao = int(opcao)
            if opcao == 0:
                print("Operação cancelada.")
                input("Pressione Enter para continuar...")
                return
            elif 1 <= opcao <= len(cliente.contas):
                conta_selecionada = cliente.contas[opcao - 1]
            else:
                print("Opção inválida.")
                input("Pressione Enter para continuar...")
                return
        except ValueError:
            print("Entrada inválida.")
            input("Pressione Enter para continuar...")
            return
    else:
        conta_selecionada = cliente.contas[0]

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    cliente.realizar_transacao(conta_selecionada, transacao)
    print(f"Saque de R$ {valor:.2f} realizado com sucesso na conta {conta_selecionada.numero}!")
    input("Pressione Enter para continuar...")

def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(clientes, cpf)
    if not cliente:
        print("\nCliente não encontrado!")
        input("Pressione Enter para continuar...")
        return

    if not cliente.contas:
        print("\nCliente não possui contas!")
        input("Pressione Enter para continuar...")
        return

    limpar_terminal()
    print("\nContas disponíveis:")
    for i, conta in enumerate(cliente.contas, 1):
        print(f"{i} - Agência: {conta.agencia} -- Número da conta: {conta.numero}")

    opcao = input("\nDigite o número da conta que deseja ver o extrato ou 0 para cancelar: ")

    try:
        opcao = int(opcao)
        if opcao == 0:
            print("Operação cancelada.")
            input("Pressione Enter para continuar...")
            return
        elif 1 <= opcao <= len(cliente.contas):
            conta = cliente.contas[opcao - 1]
        else:
            print("Opção inválida.")
            input("Pressione Enter para continuar...")
            return
    except ValueError:
        print("Entrada inválida.")
        input("Pressione Enter para continuar...")
        return

    limpar_terminal()
    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\t\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\tR$ {conta.saldo:.2f}")
    print("==========================================")
    input("Pressione Enter para continuar...")

def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(str(conta))
    input("Pressione Enter para continuar...")

def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(clientes, cpf)

    if cliente:
        print("\n@@@ Já existe cliente com esse CPF! @@@")
        input("Pressione Enter para continuar...")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    logradouro = input("Digite o Logradouro: ")
    nro = input("Digite o número do imóvel: ")
    bairro = input("Digite o Bairro: ")
    cidade = input("Digite o nome da Cidade: ")
    estado = input("Digite a sigla do Estado: ")
    endereco = [logradouro, nro, bairro, cidade, estado]

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print("\n=== Cliente criado com sucesso! ===")

    input("Pressione Enter para continuar...")

def listar_clientes(clientes):
    for cliente in clientes:
        print(str(cliente))
        input("Pressione Enter para continuar...")

def criar_conta(contas, clientes):
    numero_conta = len(contas) + 1
    print("""
          Selecione o cliente para criar a conta:

          1 - Buscar cliente por CPF
          2 - Buscar cliente por nome
          """)
    opcao = input("Selecione a opção: ")
    if opcao == "1":
        cpf = input("Digite o número do CPF (Apenas números): ")
        cliente = filtrar_cliente(clientes, cpf)

        if cliente:
            print("Usuário encontrado, criando conta...")
            conta = ContaCorrente.nova_conta(cliente = cliente, numero=numero_conta)
            contas.append(conta) 
            cliente.contas.append(conta)
            print("\nConta criada com sucesso:")
            print(f"Nome: {conta.cliente.nome}")
            print(f"Número da conta: {conta.numero}")
            print(f"Agência: {conta.agencia}")
            input("Pressione Enter para continuar...")    
        else:
            print("CPF não encontrado, o usuário deve ser cadastrado.")
            input("Pressione Enter para continuar...")
        
    elif opcao == "2":
        nome = input("Digite o nome do cliente: ")
        cliente = filtrar_cliente(clientes, nome=nome)

        if cliente:
             print(f"Usuário selecionado:\nNome: {cliente.nome}\nCPF: {cliente.cpf}")
             print("Criando conta...")
             conta = ContaCorrente.nova_conta(cliente = cliente, numero=numero_conta)
             contas.append(conta) 
             cliente.contas.append(conta)
             print("\nConta criada com sucesso:")
             print(f"Nome: {conta.cliente.nome}")
             print(f"Número da conta: {conta.numero}")
             print(f"Agência: {conta.agencia}")
             input("Pressione Enter para continuar...")
        else:
            print("Nenhum usuário selecionado ou encontrado.")
            input("Pressione Enter para continuar...")

def limpar_terminal():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

print(menu_inicial)
input("Pressione Enter para continuar...")
limpar_terminal()

def Menu():
    clientes = []
    contas = []

    while True:
        opcao = input(menu)
        limpar_terminal()        
        try:
            opcao = int(opcao)
        except ValueError:
            print("Valor inválido. Digite um número válido.")
            continue

        if opcao == 1: # Operação Depósito
            depositar(clientes)
            limpar_terminal()
        elif opcao == 2: # Operação Saque
            sacar(clientes)
            limpar_terminal()
        elif opcao == 3: # Operação Extrato
            exibir_extrato(clientes)
            limpar_terminal()
        elif opcao == 4: # Operação Criar Cliente
            criar_cliente(clientes)
            limpar_terminal()
        elif opcao == 5: # Operação Listar Usuários
            listar_clientes(clientes)
            limpar_terminal()
        elif opcao == 6: # Operação Criar Conta
            criar_conta(contas, clientes)
        elif opcao == 7: # Operação Listar contas
            listar_contas(contas)
        elif opcao == 8: # Operação Menu Final
            print(menu_final)
            break
        else:
            print("Opção Inválida. Tente novamente!")
Menu()      