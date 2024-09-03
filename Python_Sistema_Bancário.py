#SISTEMA DO BANCO DO WILL
import os

opcao = 0
valor_saldo = 1000
limite_maximo_saque = 3
lista_extrato = ""
extrato = ""
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

    4 - Exit

    """


def Operacao_Deposito(valor_saldo, extrato):
    while True:    
        valor = input("Digite o valor a ser depositado: ")
        try:
            valor = float(valor)
        except ValueError:
            print("Valor Inválido. Digite um número válido")
            continue

        if valor > 0:
            valor_saldo += valor
            extrato = f"Depósito R$ {valor:.2f}\n"
            input(f"""Depósito de R$ {valor:.2f} efetuado com sucesso!\nPressione Enter para continuar...""") 
            return valor_saldo, extrato
        else:
            print("Valor digitado inválido.")
            input("Pressione Enter para continuar...")


def Operacao_Saque(valor_saldo, limite_maximo_saque, extrato):
    while True:
        valor = input("Digite o valor desejado para saque: ")        
        try:
            valor = float(valor)
        except ValueError:
            print("Valor inválido. Digite um número válido.")
            continue
        
        if valor > 0 and valor <= 500 and valor <= valor_saldo and limite_maximo_saque > 0:
            valor_saldo -= float(valor)
            limite_maximo_saque -= 1
            extrato = f"Saque R$ {valor:.2f}\n"
            print(f"Saque de R$ {valor:.2f} realizado")
            input("Pressione Enter para continuar...")
            return valor_saldo, limite_maximo_saque, extrato
        elif valor > valor_saldo:
            print("Saldo insuficiente")
            input("Pressione Enter para continuar...")
            return valor_saldo, limite_maximo_saque, extrato
        elif valor > 500:
            print("Valor solicitado excede o limite de R$ 500.00.")
            input("Pressione Enter para continuar...")
            return valor_saldo, limite_maximo_saque, extrato
        elif limite_maximo_saque == 0:
            print("Limite de saque excedido")
            input("Pressione Enter para continuar...")
            return valor_saldo, limite_maximo_saque, extrato
        else:
            print("Valor Inválido")
            input("Pressione Enter para continuar...")
        return valor_saldo, limite_maximo_saque, extrato

def Operacao_Extrato(lista_extrato, valor_saldo):
    print("#"*25)
    print("NÂO HOUVE MOVIMENTAÇÂO" if not lista_extrato else lista_extrato)
    print(f"\nSaldo R$ {valor_saldo:.2f}.")
    print("#"*25)
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

    if opcao == 1:
        valor_saldo, extrato = Operacao_Deposito(valor_saldo, extrato)
        lista_extrato += extrato
        limpar_terminal()
    elif opcao == 2:
        valor_saldo, limite_maximo_saque, extrato = Operacao_Saque(valor_saldo, limite_maximo_saque, extrato)
        lista_extrato += extrato
        limpar_terminal()
    elif opcao == 3:
        Operacao_Extrato(lista_extrato, valor_saldo)
        limpar_terminal()
    elif opcao == 4:
        print(menu_final)
        break
    else:
        print("Opção Inválida. Tente novamente!")
        