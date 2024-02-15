from enum import Enum
from registro import *

class Generos(Enum):
    ROMANCE = 'Romance'
    MISTERIO = 'Mistério'
    FANTASIA = 'Fantasia'
    FICCAO_CIENTIFICA = 'Ficção Ciêntífica'
    TERROR = 'Terror'
    SUSPENSE = 'Suspense'
    JOVEM_ADULTO = 'Jovem Adulto'

class Estados(Enum):
    EMPRESTADO = 'Emprestado'
    DEVOLVIDO = 'Devolvido'
    RENOVADO = 'Renovado'

# Herança
class Pessoa:
    def __init__(self, nome, nacionalidade):
        self._nome = nome
        self._nacionalidade = nacionalidade
    
class Autor(Pessoa):
    def __init__(self, nome, nacionalidade):
        super().__init__(nome, nacionalidade)

class Usuario(Pessoa):
    def __init__(self, nome, nacionalidade, telefone):
        super().__init__(nome, nacionalidade)
        self.telefone = telefone

class Exemplar():
    def __init__(self, id, is_disponivel, qtd_renovacoes):
        self.id = id
        self.disponivel = is_disponivel
        self.qtd_renovacoes = qtd_renovacoes  

class Livro():
    def __init__(self, titulo, editora, generos, autores, limite_de_renovacoes):
        self.titulo = titulo
        self.editora = editora
        self.generos = generos
        self.autores = autores
        self.limite_de_renovacoes = limite_de_renovacoes
        self.exemplares_disponiveis = []
        self.exemplares_emprestados = []

    # Transforma um metodo da classe numa propriedade
    @property
    def is_limitado(self):
        if self.limite_de_renovacoes:
            return True
        else:
            return False

    def adiciona_exemplar(self, id):
        exemplar = Exemplar(id, is_disponivel=True, qtd_renovacoes=0)
        self.exemplares_disponiveis.append(exemplar)
    
    def devolve_exemplar(self,exemplar):
        self.exemplares_disponiveis = exemplar

    def _retira_exemplar(self):
        if self.conta_exemplares_disponiveis() > 0:
            exemplar = self.exemplares_disponiveis.pop()
            self.exemplares_emprestados.append(exemplar)
            return exemplar
        else:
            return None
    
    def conta_exemplares_disponiveis(self):
        return len(self.exemplares_disponiveis)
    
    def define_limite_renovacao(self, limite):
        self.limitado = True
        self.limite_de_renovacoes = limite

class Biblioteca:
    def __init__(self):
        self.autores = {}
        self.livros = {}
        self.usuarios = {}
        self.registros = []
        self.numero_operacao = 0
    
    def adiciona_autor(self, id_autor, nome, nacionalidade):
        autor = Autor(nome, nacionalidade)
        self.autores[id_autor] = autor
            
    def adiciona_livro(self, id_livro, titulo, editora, generos, autores, limite_de_renovacoes=None):
        livro = Livro(titulo=titulo, editora=editora, generos=generos, autores=autores, limite_de_renovacoes=limite_de_renovacoes)
        self.livros[id_livro] = livro

    def adiciona_usuario(self, id_usuario, nome, nacionalidade, telefone):
        usuario = Usuario(nome, nacionalidade, telefone)
        self.usuarios[id_usuario] = usuario

    def busca_registro(self, numero):
        resultado = None
        for registro in self.registros:
            if registro.numero_operacao == numero:
                resultado = registro
        return resultado
    
    def empresta_livro(self, livro: Livro, usuario: Usuario):
        exemplar = livro._retira_exemplar()
        if exemplar is None:
            print('Não há exemplares disponíveis para empréstimo')
        else:
            print('Empréstimo realizado com sucesso!')
            self.numero_operacao += 1
            emprestimo = RegistroEmprestimo(self.numero_operacao, livro, usuario, Estados.EMPRESTADO.value, exemplar)
            self.registros.append(emprestimo)
            print(emprestimo)
            
    def devolve_livro(self, livro: Livro, usuario: Usuario, registro_emprestimo: Registro):
        exemplar = registro_emprestimo.exemplar
        
        if livro.is_limitado:
            exemplar.qtd_renovacoes = 0

        livro.devolve_exemplar(exemplar)
        print('Devolução realizada com sucesso!')
        self.numero_operacao += 1
        devolucao = RegistroDevolucao(self.numero_operacao, livro, usuario, Estados.DEVOLVIDO.value, exemplar, registro_emprestimo)
        self.registros.append(devolucao)
        print(devolucao)

    def renova_emprestimo(self, livro: Livro, usuario: Usuario, registro_anterior: Registro):
        exemplar = registro_anterior.exemplar

        if livro.is_limitado:
            if exemplar.qtd_renovacoes >= livro.limite_de_renovacoes:
                print('Limite de renovações atingido!')
            else:
                exemplar.qtd_renovacoes += 1
                self.numero_operacao += 1
                print(f'Renovação realizada com sucesso! Renovações: {exemplar.qtd_renovacoes}')
                renovacao = RegistroRenovacao(self.numero_operacao, livro, usuario, Estados.RENOVADO.value, exemplar, registro_anterior)
                self.registros.append(renovacao)
                print(renovacao)
        else:
            print('Renovação realizada com sucesso!')
            self.numero_operacao += 1
            renovacao = RegistroRenovacao(self.numero_operacao, livro, usuario, Estados.RENOVADO.value, exemplar, registro_anterior)
            self.registros.append(renovacao)
            print(renovacao)

biblioteca = Biblioteca()
biblioteca.adiciona_autor(1, 'Joseph Sheridan Le Fanu', 'Irlandês')
biblioteca.adiciona_livro(1, 'Carmilla', 'Pandorga', [Generos.ROMANCE.value, Generos.TERROR.value], [biblioteca.autores.get(1)], 2)
biblioteca.adiciona_usuario(1, 'Júlia', 'Brasileira', '98 989898998')

livro = biblioteca.livros.get(1)
livro.adiciona_exemplar(1)
usuario = biblioteca.usuarios.get(1)
biblioteca.empresta_livro(livro, usuario)
registro_anterior = biblioteca.busca_registro(1)
biblioteca.renova_emprestimo(livro, usuario, registro_anterior)
registro_anterior = biblioteca.busca_registro(2)
biblioteca.renova_emprestimo(livro, usuario, registro_anterior)
registro_anterior = biblioteca.busca_registro(3)
biblioteca.renova_emprestimo(livro, usuario, registro_anterior)
registro_anterior = biblioteca.busca_registro(3)
biblioteca.devolve_livro(livro, usuario, registro_anterior)

