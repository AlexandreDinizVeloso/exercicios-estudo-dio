def menu():
    menu = """\n
    ===============Menu===============
    = [d]\tDepositar
    = [s]\tSacar
    = [e]\tExtrato
    = [c]\tNova Conta
    = [u]\tNovo Usuário
    = [lc]\tListar Contas
    = [q]\tSair
    ==================================
    => """
    return input(menu)

def deposito(saldo, valor, extrato):
    if valor <= 0:
        operacao(400, "O valor informado é inválido.")
    else:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        operacao(200)
    return saldo, extrato

def saque(*, saldo, valor, extrato, numero_saques, LIMITE_SAQUES):
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
    return saldo, extrato

def exibir_extrato(saldo, /, *, extrato):
    if extrato == "":
        print("Não há registros de movimentação na conta.")
    else:
        print(extrato)
        print(f"Saldo: R$ {saldo}")
    return 

def criar_usuario(usuarios):
    cpf = input("Informe o CPF do usuário(somente número): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        return operacao(400, "Cpf já registrado.")

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (rua, n° - bairro - cidade/estado): ")
    usuarios.append({"nome": nome, "cpf": cpf, "data_nascimento": data_nascimento, "endereco": endereco})
    return operacao(200)

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário(somente número): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        operacao(200)
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    return operacao(400, "Usuário não encontrado.")

def filtrar_usuario(cpf, usuarios):
    filtragem = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return filtragem[0] if filtragem else None

def listar_contas(contas):
    if contas:
        for conta in contas:
            conteudo = f"""\
                ========================================
                = Agência:\t{conta["agencia"]}
                = Conta:\t{conta["numero_conta"]}
                = Titular:\t{conta["usuario"]["nome"]}
                ========================================
                """
            print(conteudo)
        return
    return print("Não foi encontrado contas cadastradas.")

def operacao(numero, causa = None):
    if numero == 200:
        return print("Operação efetuada com sucesso.")
    elif numero == 400:
        return print(f"Operação falhou: {causa}")

def main():
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    LIMITE_SAQUES = 3
    usuarios = []
    contas = []
    AGENCIA = "0001"

    while True:
        opção = menu()
        if opção == "d":
            saldo, extrato = deposito(saldo, valor, extrato)

        elif opção == "s":
            saldo, extrato = saque(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                numero_saques=numero_saques,
                LIMITE_SAQUES=LIMITE_SAQUES
            )
            
        elif opção == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opção == "c":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)


        elif opção == "u":
            criar_usuario(usuarios)
        
        elif opção == "lc":
            listar_contas(contas)
                
        elif opção == "q":
            break
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

main()