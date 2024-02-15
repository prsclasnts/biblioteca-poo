from abc import ABC
from datetime import date, timedelta
# Classe base
class Registro(ABC):
    def __init__(self, numero_operacao, livro, usuario, estado, exemplar):
        self.numero_operacao = numero_operacao
        self.livro = livro
        self.usuario = usuario
        self.estado = estado
        self.exemplar = exemplar

    def __str__(self):
        return f'----- REGISTRO {self.numero_operacao}-----\nLivro: {self.livro.titulo}\tID: {self.exemplar.id}\nEstado: {self.estado}\nUsuario: {self.usuario._nome}'

class RegistroEmprestimo(Registro):
    def __init__(self, numero_operacao, livro, usuario, estado, exemplar):
        super().__init__(numero_operacao, livro, usuario, estado, exemplar)

    @property
    def data_de_emprestimo(self):
        return date.today()
    
    @property
    def data_de_devolucao(self):
        prazo = timedelta(7)
        return self.data_de_emprestimo + prazo
        

class RegistroDevolucao(Registro):
    def __init__(self, numero_operacao, livro, usuario, estado, exemplar, registro_emprestimo):
        super().__init__(numero_operacao, livro, usuario, estado, exemplar)
        self.registro_emprestimo = registro_emprestimo

    @property
    def data_de_emprestimo(self):
        return self.registro_emprestimo.data_de_emprestimo
    
    @property
    def data_de_devolucao(self):
        return date.today()

class RegistroRenovacao(Registro):
    def __init__(self, numero_operacao, livro, usuario, estado, exemplar, registro_emprestimo):
        super().__init__(numero_operacao, livro, usuario, estado, exemplar)
        self.registro_emprestimo = registro_emprestimo

    @property
    def data_de_emprestimo(self):
        return self.registro_emprestimo.data_de_emprestimo
    
    @property
    def data_de_devolucao(self):
        prazo = timedelta(7)
        return self.data_de_emprestimo + prazo