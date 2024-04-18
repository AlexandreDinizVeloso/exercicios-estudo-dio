from abc import ABC

# def menu():
#     menu = """\n
#     ===============Menu===============
#     = [d]\tDepositar
#     = [s]\tSacar
#     = [e]\tExtrato
#     = [c]\tNova Conta
#     = [u]\tNovo Usuário
#     = [lc]\tListar Contas
#     = [q]\tSair
#     ==================================
#     => """
#     return input(menu)

# def deposito(saldo, valor, extrato):
#     if valor <= 0:
#         operacao(400, "O valor informado é inválido.")
#     else:
#         saldo += valor
#         extrato += f"Depósito: R$ {valor:.2f}\n"
#         operacao(200)
#     return saldo, extrato

# def saque(*, saldo, valor, extrato, numero_saques, LIMITE_SAQUES):
#     if numero_saques >= 3:
#         operacao(400, "Número de saques máximo excedido.")
#     else:
#         valor = float(input("Digite o valor a ser sacado: "))
#         if valor > 500:
#             operacao(400, "Valor de saque máximo excedido.")
#         elif valor > saldo:
#             operacao(400, "Saldo insuficiente.")
#         else:
#             saldo -= valor
#             extrato += f"Saque: R$ {valor:.2f}\n"
#             numero_saques += 1
#             operacao(200)
#     return saldo, extrato

# def exibir_extrato(saldo, /, *, extrato):
#     if extrato == "":
#         print("Não há registros de movimentação na conta.")
#     else:
#         print(extrato)
#         print(f"Saldo: R$ {saldo}")
#     return 

# def criar_usuario(usuarios):
#     cpf = input("Informe o CPF do usuário(somente número): ")
#     usuario = filtrar_usuario(cpf, usuarios)

#     if usuario:
#         return operacao(400, "Cpf já registrado.")

#     nome = input("Informe o nome completo: ")
#     data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
#     endereco = input("Informe o endereço (rua, n° - bairro - cidade/estado): ")
#     usuarios.append({"nome": nome, "cpf": cpf, "data_nascimento": data_nascimento, "endereco": endereco})
#     return operacao(200)

# def criar_conta(agencia, numero_conta, usuarios):
#     cpf = input("Informe o CPF do usuário(somente número): ")
#     usuario = filtrar_usuario(cpf, usuarios)

#     if usuario:
#         operacao(200)
#         return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
#     return operacao(400, "Usuário não encontrado.")

# def filtrar_usuario(cpf, usuarios):
#     filtragem = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
#     return filtragem[0] if filtragem else None

# def listar_contas(contas):
#     if contas:
#         for conta in contas:
#             conteudo = f"""\
#                 ========================================
#                 = Agência:\t{conta["agencia"]}
#                 = Conta:\t{conta["numero_conta"]}
#                 = Titular:\t{conta["usuario"]["nome"]}
#                 ========================================
#                 """
#             print(conteudo)
#         return
#     return print("Não foi encontrado contas cadastradas.")

# def operacao(numero, causa = None):
#     if numero == 200:
#         return print("Operação efetuada com sucesso.")
#     elif numero == 400:
#         return print(f"Operação falhou: {causa}")

# def main():
#     saldo = 0
#     limite = 500
#     extrato = ""
#     numero_saques = 0
#     LIMITE_SAQUES = 3
#     usuarios = []
#     contas = []
#     AGENCIA = "0001"

#     while True:
#         opção = menu()
#         if opção == "d":
#             saldo, extrato = deposito(saldo, valor, extrato)

#         elif opção == "s":
#             saldo, extrato = saque(
#                 saldo=saldo,
#                 valor=valor,
#                 extrato=extrato,
#                 numero_saques=numero_saques,
#                 LIMITE_SAQUES=LIMITE_SAQUES
#             )
            
#         elif opção == "e":
#             exibir_extrato(saldo, extrato=extrato)

#         elif opção == "c":
#             numero_conta = len(contas) + 1
#             conta = criar_conta(AGENCIA, numero_conta, usuarios)

#             if conta:
#                 contas.append(conta)


#         elif opção == "u":
#             criar_usuario(usuarios)
        
#         elif opção == "lc":
#             listar_contas(contas)
                
#         elif opção == "q":
#             break
#         else:
#             print("Operação inválida, por favor selecione novamente a operação desejada.")

# main()

class conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = historico()

    @classmethod
    def nova_conta(cls, numero, cliente):
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
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def operacao(self, numero, causa=None):
        self.numero = numero
        self.causa = causa
        if self.numero == 200:
            print("Operação efetuada com sucesso.")
        elif self.numero == 400:
            print(f"Operação falhou: {self.causa}")

    def sacar(self, valor):
        if valor > self._saldo:
            self.operacao(400, "Saldo insuficiente.")
            return False
        elif valor <= 0:
            self.operacao(400, "Valor inválido.")
            return False
        self._saldo -= valor
        self.operacao(200)
        self._historico.adicionar_transacao("Saque", valor)
        return True

    def depositar(self, valor):
        if valor <= 0:
            self.operacao(400, "Valor inválido.")
            return False
        self._saldo += valor
        self.operacao(200)
        self._historico.adicionar_transacao("Depósito", valor)
        return True

class conta_corrente(conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
    
    def sacar(self, valor):
        numero_saques = len(self._historico._saque)
        if numero_saques >= self.limite_saques:
            self.operacao(400, "Limite de saques alcançado.")
            return False
        elif valor > self.limite:
            self.operacao(400, "Valor acima do limite de saque permitido.")
            return False
        return super().sacar(valor)
    
    def depositar(self, valor):
        if valor <= 0:
            self.operacao(400, "Valor inválido.")
            return False
        super().depositar(valor)
        return True

class historico:
    def __init__(self):
        self._saque = []
        self._deposito = []
        self._transacoes = [self._saque, self._deposito]

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, tipo, valor):
        if tipo == "Saque":
            self._saque.append((len(self._saque) + 1, valor))
        elif tipo == "Depósito":
            self._deposito.append((len(self._deposito) + 1, valor))

class cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class pessoa_fisica(cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass

class saque(transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao("Saque", self.valor)

class deposito(transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao("Depósito", self.valor)