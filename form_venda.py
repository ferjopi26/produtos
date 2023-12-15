import gi
from data_access import DataAccess
from class_produtos import Produtos
from cupom import Cupom

gi.require_version("Adw", "1")
gi.require_version("Gtk", "4.0")

from gi.repository import Adw, Gio, GObject, Gtk

class FormVenda():
    def __init__(self, parent):
        self.i = 0
        self.total_geral = 0
        
        self.parent = parent
        
        builder = Gtk.Builder()
        builder.add_from_file("form_venda.ui")
        
        self.win_form_venda = builder.get_object("win_form_venda")

        self.entry_quantidade = builder.get_object("entry_quantidade")
        self.entry_punitario =builder.get_object("entry_punitario")
        self.entry_total_item = builder.get_object("entry_total_item")
        self.entry_total = builder.get_object("entry_total")

        self.btn_fechar = builder.get_object("btn_fechar")
        self.btn_fechar.connect("clicked", self.fechar)

        self.btn_efetuar_venda = builder.get_object("btn_efetuar_venda")
        self.btn_efetuar_venda.connect("clicked", self.efetuar_venda)

        self.entry_quantidade.connect("activate", self.entry_quantidade_activate)
        
        self.list_venda = builder.get_object("list_venda")
        self.list_venda.set_show_row_separators(True)
        self.list_venda.set_show_column_separators(True)
        self.model = Gio.ListStore(item_type=Produtos)

        self.factory = Gtk.SignalListItemFactory()
        self.factory.connect("setup", self._on_factory_setup)
        self.factory.connect("bind", self._on_factory_bind, "idproduto")
        
        self.factory2 = Gtk.SignalListItemFactory()
        self.factory2.connect("setup", self._on_factory_setup)
        self.factory2.connect("bind", self._on_factory_bind, "produto")

        self.factory3 = Gtk.SignalListItemFactory()
        self.factory3.connect("setup", self._on_factory_setup)
        self.factory3.connect("bind", self._on_factory_bind, "quantidade")

        self.factory4 = Gtk.SignalListItemFactory()
        self.factory4.connect("setup", self._on_factory_setup)
        self.factory4.connect("bind", self._on_factory_bind, "un")

        self.factory5 = Gtk.SignalListItemFactory()
        self.factory5.connect("setup", self._on_factory_setup)
        self.factory5.connect("bind", self._on_factory_bind, "punitario")

        self.factory6 = Gtk.SignalListItemFactory()
        self.factory6.connect("setup", self._on_factory_setup)
        self.factory6.connect("bind", self._on_factory_bind, "total")

        self.create_column_to_column_view()

        self.win_form_venda.present()

    def _on_factory_setup(self, factory, list_item):
        cell = Gtk.Inscription()
        cell._binding = None
        list_item.set_child(cell)
        
    def _on_factory_bind(self, factory, list_item, what):
        cell = list_item.get_child()
        produtos = list_item.get_item()
        cell._binding = produtos.bind_property(what, cell, "text", GObject.BindingFlags.SYNC_CREATE)

    def create_column_to_column_view(self):
        col1 = Gtk.ColumnViewColumn(title="Id", factory=self.factory)
        col1.props.expand = False
        col1.props.fixed_width = 100
        self.list_venda.append_column(col1)

        col2 = Gtk.ColumnViewColumn(title="Produto", factory=self.factory2)
        col2.props.expand = True
        self.list_venda.append_column(col2)

        col3 = Gtk.ColumnViewColumn(title="Quantidade", factory=self.factory3)
        col3.props.expand = False
        col3.props.fixed_width = 100
        self.list_venda.append_column(col3)

        col4 = Gtk.ColumnViewColumn(title="Un", factory=self.factory4)
        col4.props.expand = False
        self.list_venda.append_column(col4)
        
        col5 = Gtk.ColumnViewColumn(title="Preço Unitário", factory=self.factory5)
        col5.props.expand = False
        col5.props.fixed_width = 100
        self.list_venda.append_column(col5)

        col6 = Gtk.ColumnViewColumn(title="Total", factory=self.factory6)
        col6.props.expand = False
        col6.props.fixed_width = 100
        self.list_venda.append_column(col6)

    def venda(self, produto):
        self.entry_quantidade.set_text("")
        self.entry_total_item.set_text("")
        
        self.produto = produto
        
        self.list_venda.set_model(Gtk.NoSelection(model=self.model))
        self.model.append(Produtos(idproduto=produto.idproduto, produto=produto.produto, quantidade="0", un=produto.un, punitario=produto.punitario, total="0"))
        
        self.entry_punitario.set_text(produto.punitario)

        self.entry_quantidade.set_can_focus(True)
        
    def entry_quantidade_activate(self, widget):
        quantidade = float(self.entry_quantidade.get_text())
        punitario = float(self.produto.punitario)
        total = quantidade * punitario
        
        quantidade = "{:.{}f}".format(quantidade, 2)
        _total = "{:.{}f}".format(total, 2)

        self.produto.quantidade = quantidade
        self.produto.total = total
        
        self.model.remove(self.i)
        self.model.insert(self.i, Produtos(idproduto=self.produto.idproduto, produto=self.produto.produto, quantidade=quantidade, un=self.produto.un, 
                                   punitario=self.produto.punitario, total=_total))
        
        self.entry_total_item.set_text(f"{total}")

        self.i += 1
        
        self.total_geral += total
        
        total_geral = "{:.{}f}".format(self.total_geral, 2)
        self.entry_total.set_text(f"{total_geral}")

    def fechar(self, widget):
        self.win_form_venda.destroy()

    def efetuar_venda(self, widget):
        data_access = DataAccess()
        self.venda = []
        
        result = data_access.getMaxNfNumber()
        
        for row in result:
            self.nf = row[0]
        
        if self.nf == None:
            self.nf = 0
        
        self.nf += 1

        item = self.list_venda.get_model()
        n_itens = item.get_n_items()

        for i in range(n_itens):
            self.venda.append(item.get_item(i))
        
        if data_access.finalizar_venda(self.venda, self.nf) == True:
            dialog = Gtk.MessageDialog(text="Venda efetuada com sucesso.", buttons=Gtk.ButtonsType.OK)

            dialog.set_title("Produtos")
            dialog.set_transient_for(self.win_form_venda)
            dialog.set_destroy_with_parent(True)
            dialog.connect("response", self.response_dialog)
            dialog.show()
            
    def response_dialog(self, dialog, response_id):
        dialog.destroy()
        self.parent.get_produtos()
        self.win_form_venda.destroy()

        cupom = Cupom(self.venda, self.nf, self.total_geral, self.win_form_venda)
        cupom.win_cupom.present()
