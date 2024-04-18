from abc import ABC, abstractclassmethod, abstractproperty

class conta:
    def __init__(self, numero, usuario):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = usuario
        self._historico = historico()
    
    def __str__(self):
        return f"""\n
        ==================================
        = Proprietário:\t\t{self._cliente.nome}
        = Número da Conta:\t{self._numero}
        ==================================
        """

    @classmethod
    def nova_conta(cls, numero, usuario):
        return cls(numero, usuario)

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
    def usuario(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico
        
    def sacar(self, valor):
        if valor > self._saldo:
            operacao(400, "Saldo insuficiente.")
            return False
        elif valor <= 0:
            operacao(400, "Valor inválido.")
            return False
        self._saldo -= valor
        operacao(200)
        self._historico.adicionar_transacao("Saque", valor)
        return True

    def depositar(self, valor):
        if valor <= 0:
            operacao(400, "Valor inválido.")
            return False
        self._saldo += valor
        operacao(200)
        self._historico.adicionar_transacao("Depósito", valor)
        return True

class conta_corrente(conta):
    def __init__(self, numero, usuario, limite=500, limite_saques=3):
        super().__init__(numero, usuario)
        self.limite = limite
        self.limite_saques = limite_saques
        self.saques_feitos = 0
    
    def sacar(self, valor):
        if self.saques_feitos >= self.limite_saques:
            operacao(400, "Limite de saques alcançado.")
            return False
        elif valor > self.limite:
            operacao(400, "Valor acima do limite de saque permitido.")
            return False
        sucesso = super().sacar(valor)
        if sucesso:
            self.saques_feitos += 1
        return sucesso
    
    def depositar(self, valor):
        if valor <= 0:
            operacao(400, "Valor inválido.")
            return False
        super().depositar(valor)
        return True

class historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, tipo, valor):
        self._transacoes.append({"tipo": tipo, "valor": valor})

    def transacoes_por_tipo(self, tipo):
        return [t for t in self._transacoes if t["tipo"] == tipo]

class usuario:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class pessoa_fisica(usuario):
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

def operacao(numero, causa=None):
    numero = numero
    causa = causa
    if numero == 200:
        print("Operação efetuada com sucesso.")
    elif numero == 400:
        print(f"Operação falhou: {causa}")

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

def filtrar_usuario(cpf, usuarios):
    filtragem = [usuario for usuario in usuarios if usuario.cpf == cpf]
    return filtragem[0] if filtragem else None


def recuperar_conta_usuario(usuario):
    if not usuario.contas:
        operacao(400, "Usuário não possui contas.")
        return None
    for n in range(len(usuario.contas)):
        if isinstance(usuario.contas[n], conta_corrente):
            print(f"= [{n + 1}]\tConta n°{usuario.contas[n].numero}")
        else:
            print(f"= [{n + 1}]\tConta n°{usuario.contas[n].numero_conta}")
    escolha_input = input("Digite qual conta deseja utilizar: ")
    if not escolha_input:
        operacao(400, "Escolha inválida.")
        return None
    try:
        escolha = int(escolha_input)
    except ValueError:
        operacao(400, "Escolha inválida.")
        return None
    if escolha < 1 or escolha > len(usuario.contas):
        operacao(400, "Escolha inválida.")
        return None
    return usuario.contas[escolha - 1]

def depositar(usuarios):
    cpf = input("Informe o CPF do usuario: ")
    usuario_selecionado = filtrar_usuario(cpf, usuarios)
    if not usuario_selecionado:
        operacao(400, "Usuário não encontrado.")
        return
    valor_input = input("Informe o valor do depósito: ")
    if not valor_input:
        operacao(400, "Valor inválido.")
        return
    try:
        valor = float(valor_input)
    except ValueError:
        operacao(400, "Valor inválido.")
        return
    transacao = deposito(valor)
    conta = recuperar_conta_usuario(usuario_selecionado)
    if not conta:
        return
    usuario_selecionado.realizar_transacao(conta, transacao)

def sacar(usuarios):
    cpf = input("Informe o CPF do usuario: ")
    usuario_selecionado = filtrar_usuario(cpf, usuarios)
    if not usuario_selecionado:
        operacao(400, "Usuário não encontrado.")
        return
    valor_input = input("Informe o valor do saque: ")
    if not valor_input:
        operacao(400, "Valor inválido.")
        return
    try:
        valor = float(valor_input)
    except ValueError:
        operacao(400, "Valor inválido.")
        return
    transacao = saque(valor)
    conta = recuperar_conta_usuario(usuario_selecionado)
    if not conta:
        return
    usuario_selecionado.realizar_transacao(conta, transacao)


def exibir_extrato(usuario):
    cpf = input("Informe o CPF do usuario: ")
    usuario_selecionado = filtrar_usuario(cpf, usuario)
    if not usuario_selecionado:
        operacao(400, "Usuário não encontrado.")
        return
    conta = recuperar_conta_usuario(usuario_selecionado)
    if not conta:
        operacao(400, "Conta não encontrada.")
        return
    transacoes = conta.historico.transacoes_por_tipo("Saque") + conta.historico.transacoes_por_tipo("Depósito")
    extrato = ""
    if not transacoes:
        extrato = "Não há registros de movimentação na conta."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\tR$ {transacao['valor']:.2f}"
    print(extrato)
    print(f"Saldo:\tR$ {conta.saldo}")

def criar_cliente(usuarios):
    cpf = input("Informe o CPF (somente número): ")
    usuario_existente = filtrar_usuario(cpf, usuarios)
    if usuario_existente:
        operacao(400, "Cpf já registrado.")
        return
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (rua, n° - bairro - cidade/estado): ")
    novo_usuario = pessoa_fisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    usuarios.append(novo_usuario)
    operacao(200)

def criar_conta(numero_conta, usuario, contas):
    cpf = input("Informe o CPF do usuario: ")
    usuario = filtrar_usuario(cpf, usuario)
    if not usuario:
        operacao(400, "Usuário não encontrado")
        return
    conta = conta_corrente.nova_conta(usuario=usuario, numero=numero_conta)
    contas.append(conta)
    usuario.contas.append(conta)
    operacao(200)

def listar_contas(contas):
    if contas:
        for conta in contas:
            print(conta)
        return
    return print("Não foi encontrado contas cadastradas.")

def main():
    usuarios = []
    contas = []

    while True:
        opcao = menu()
        if opcao == "d":
            depositar(usuarios)

        elif opcao == "s":
            sacar(usuarios)
            
        elif opcao == "e":
            exibir_extrato(usuarios)

        elif opcao == "c":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, usuarios, contas)

        elif opcao == "u":
            criar_cliente(usuarios)
        
        elif opcao == "lc":
            listar_contas(contas)
                
        elif opcao == "q":
            break
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

main()