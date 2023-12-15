import gi
from data_access import DataAccess
from cupom import Cupom

gi.require_version("Adw", "1")
gi.require_version("Gtk", "4.0")
gi.require_version('Poppler', '0.18')
gi.require_version("GLib", "2.0")

from gi.repository import GLib
from gi.repository import Adw, Gio, GObject, Gtk
from gi.repository import Poppler

from class_vendas import Vendas

class ConsultaVendas():
    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file("consulta_vendas.ui")

        self.win_consulta_vendas = builder.get_object("win_consulta_vendas")
        
        self.btn_fechar = builder.get_object("btn_fechar")
        self.btn_fechar.connect("clicked", self.fechar)

        self.btn_buscar = builder.get_object("btn_buscar")
        self.btn_buscar.connect("clicked", self.buscar)

        self.btn_print = builder.get_object("btn_print")
        self.btn_print.connect("clicked", self.print)

        self.entry_num_cupom = builder.get_object("entry_num_cupom")
        self.entry_num_cupom.connect("activate", self.buscar)

        self.entry_total_venda = builder.get_object("entry_total_venda")

        self.btn_nova_consulta = builder.get_object("btn_nova_consulta")
        self.btn_nova_consulta.connect("clicked", self.nova_consulta)

        self.list_vendas = builder.get_object("list_vendas")
        self.list_vendas.set_show_row_separators(True)
        self.list_vendas.set_show_column_separators(True)
        
        self.factory = Gtk.SignalListItemFactory()
        self.factory.connect("setup", self._on_factory_setup)
        self.factory.connect("bind", self._on_factory_bind, "idvenda")
        
        self.factory1 = Gtk.SignalListItemFactory()
        self.factory1.connect("setup", self._on_factory_setup)
        self.factory1.connect("bind", self._on_factory_bind, "idproduto")
        
        self.factory2 = Gtk.SignalListItemFactory()
        self.factory2.connect("setup", self._on_factory_setup)
        self.factory2.connect("bind", self._on_factory_bind, "produto")

        self.factory3 = Gtk.SignalListItemFactory()
        self.factory3.connect("setup", self._on_factory_setup)
        self.factory3.connect("bind", self._on_factory_bind, "quantidade")

        self.factory4 = Gtk.SignalListItemFactory()
        self.factory4.connect("setup", self._on_factory_setup)
        self.factory4.connect("bind", self._on_factory_bind, "punitario")

        self.factory5 = Gtk.SignalListItemFactory()
        self.factory5.connect("setup", self._on_factory_setup)
        self.factory5.connect("bind", self._on_factory_bind, "total")

        self.factory6 = Gtk.SignalListItemFactory()
        self.factory6.connect("setup", self._on_factory_setup)
        self.factory6.connect("bind", self._on_factory_bind, "data")

        self.create_column_to_column_view()

    def create_column_to_column_view(self):
        col1 = Gtk.ColumnViewColumn(title="Venda", factory=self.factory)
        col1.props.expand = False
        col1.props.fixed_width = 50
        self.list_vendas.append_column(col1)

        col2 = Gtk.ColumnViewColumn(title="Id Produto", factory=self.factory1)
        col2.props.expand = False
        col2.props.fixed_width = 50
        self.list_vendas.append_column(col2)

        col3 = Gtk.ColumnViewColumn(title="Produto", factory=self.factory2)
        col3.props.expand = True
        self.list_vendas.append_column(col3)

        col4 = Gtk.ColumnViewColumn(title="Quantidade", factory=self.factory3)
        col4.props.expand = False
        col4.props.fixed_width = 50
        self.list_vendas.append_column(col4)
        
        col5 = Gtk.ColumnViewColumn(title="Preço Unitário", factory=self.factory4)
        col5.props.expand = False
        col5.props.fixed_width = 50
        self.list_vendas.append_column(col5)

        col6 = Gtk.ColumnViewColumn(title="Total", factory=self.factory5)
        col6.props.expand = False
        col6.props.fixed_width = 50
        self.list_vendas.append_column(col6)

        col7 = Gtk.ColumnViewColumn(title="Data", factory=self.factory6)
        col7.props.expand = True
        self.list_vendas.append_column(col7)

    def _on_factory_setup(self, factory, list_item):
        cell = Gtk.Inscription()
        cell._binding = None
        list_item.set_child(cell)
        
    def _on_factory_bind(self, factory, list_item, what):
        cell = list_item.get_child()
        produtos = list_item.get_item()
        cell._binding = produtos.bind_property(what, cell, "text", GObject.BindingFlags.SYNC_CREATE)

    def fechar(self, widget):
        self.win_consulta_vendas.destroy()

    def buscar(self, widget):
        self.nf = self.entry_num_cupom.get_text()
        self.venda = []
        data_access = DataAccess()
        result = data_access.getVendaByNf(self.nf)
        
        self.model = Gio.ListStore(item_type=Vendas)
        for row in result:
            self.model.append(Vendas(nf=row[7], idvenda=row[0], idproduto=row[1], produto=row[2], quantidade=row[3], punitario=row[4], total=row[5], data=row[6]))
            self.venda.append(Vendas(nf=row[7], idvenda=row[0], idproduto=row[1], produto=row[2], quantidade=row[3], punitario=row[4], total=row[5], data=row[6]))

        self.list_vendas.set_model(Gtk.NoSelection(model=self.model))

        item = self.list_vendas.get_model()
        n_itens = item.get_n_items()

        result = data_access.getTotalGeral(self.nf)

        for row in result:
            self.entry_total_venda.set_text(str(row[0]))
            self.total_geral = row[0]

    def print(self, widget):
        cupom = Cupom(self.venda, self.nf, self.total_geral, self.win_consulta_vendas)
        cupom.win_cupom.present()

    def nova_consulta(self, widget):
        self.entry_num_cupom.set_text("")

        self.entry_num_cupom.grab_focus()
