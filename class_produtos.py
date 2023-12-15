import gi

from gi.repository import GObject

class Produtos(GObject.Object):
    __gtype_name__ = "Produtos"

    def __init__(self, idproduto, produto, quantidade, un, punitario, total):
        super().__init__()

        self._idproduto = idproduto
        self._produto = produto
        self._quantidade = quantidade
        self._un = un
        self._punitario = punitario
        self._total = total

    @GObject.Property(type=str)
    def idproduto(self):
        return self._idproduto

    @GObject.Property(type=str)
    def produto(self):
        return self._produto

    @GObject.Property(type=str)
    def quantidade(self):
        return self._quantidade

    @GObject.Property(type=str)
    def un(self):
        return self._un

    @GObject.Property(type=str)
    def punitario(self):
        return self._punitario

    @GObject.Property(type=str)
    def total(self):
        return self._total
