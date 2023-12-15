import gi

from gi.repository import GObject

class Vendas(GObject.Object):
    __gtype_name__ = "Vendas"

    def __init__(self, idvenda, nf, idproduto, produto, quantidade, punitario, total, data):
        super().__init__()

        self._idvenda = idvenda
        self._nf = nf
        self._idproduto = idproduto
        self._produto = produto
        self._quantidade = quantidade
        self._punitario = punitario
        self._total = total
        self._data = data

    @GObject.Property(type=str)
    def idvenda(self):
        return self._idvenda
    
    @GObject.Property(type=str)
    def nf(self):
        return self._nf
    
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
    def punitario(self):
        return self._punitario

    @GObject.Property(type=str)
    def total(self):
        return self._total

    @GObject.Property(type=str)
    def data(self):
        return self._data
