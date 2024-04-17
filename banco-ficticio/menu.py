menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

def operacao(numero, causa = None):
    if numero == 200:
        print("Operação efetuada com sucesso.")
    elif numero == 400:
        print(f"Operação falhou: {causa}")

while True:
    opção = input(menu)
    if opção == "d":
        valor = float(input("Digite o valor a ser depositado: "))
        if valor <= 0:
            operacao(400, "O valor informado é inválido.")
        else:
            saldo += valor
            extrato += f"Depósito: R$ {valor:.2f}\n"
            operacao(200)

    elif opção == "s":
        if numero_saques >= 3:
            operacao(400, "Número de saques máximo excedido.")
        else:
            valor = float(input("Digite o valor a ser sacado: "))
            if valor > 500:
                operacao(400, "Valor de saque máximo excedido.")
            elif valor > saldo:
                operacao(400, "Saldo insuficiente.")
            else:
                saldo -= valor
                extrato += f"Saque: R$ {valor:.2f}\n"
                numero_saques += 1
                operacao(200)

    elif opção == "e":
        if extrato == "":
            print("Não há registros de movimentação na conta.")
        else:
            print(extrato)
            print(f"Saldo: R$ {saldo}")
            
        g
    elif opção == "q":
        break
    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")git