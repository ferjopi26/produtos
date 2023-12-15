import gi
from data_access import DataAccess

gi.require_version("Gtk", "4.0")

from gi.repository import Adw, Gio, GObject, Gtk

class NovoProduto():
    def __init__(self, parent):
        self.parent = parent
        
        builder = Gtk.Builder()
        builder.add_from_file("novo_produto.ui")

        self.win_novo_produto = builder.get_object("win_novo_produto")

        self.btn_fechar = builder.get_object("btn_fechar")
        self.btn_fechar.connect("clicked", self.fechar)

        self.btn_salvar = builder.get_object("btn_salvar")
        self.btn_salvar.connect("clicked", self.salvar)

        self.btn_limpar = builder.get_object("btn_limpar")
        self.btn_limpar.connect("clicked", self.limpar)

        self.entry_produto = builder.get_object("entry_produto")
        self.entry_quantidade = builder.get_object("entry_quantidade")
        self.entry_un = builder.get_object("entry_un")
        self.entry_p_unit = builder.get_object("entry_p_unit")

        self.win_novo_produto.present()

    def fechar(self, widget):
        self.win_novo_produto.destroy()

    def salvar(self, widget):
        list_produto = []

        produto = self.entry_produto.get_text()
        quantidade = self.entry_quantidade.get_text()
        un = self.entry_un.get_text()
        punitario = self.entry_p_unit.get_text()
        
        list_produto.append([produto, quantidade, un, punitario])
        
        data_access = DataAccess()
        last_row_id = data_access.insertNovoItem(list_produto)

        print(f"Inserido 1 registro com Id {last_row_id}")

        self.parent.get_produtos()
        
    def limpar(self, widget):
        self.entry_produto.set_text("")
        self.entry_quantidade.set_text("")
        self.entry_p_unit.set_text("")

        self.entry_produto.grab_focus()