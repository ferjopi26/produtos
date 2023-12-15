import sys
import gi
from data_access import DataAccess

gi.require_version("Adw", "1")
gi.require_version("Gtk", "4.0")

from gi.repository import Adw, Gio, GObject, Gtk

from novo_produto import NovoProduto
from form_venda import FormVenda
from class_produtos import Produtos
from consulta_vendas import ConsultaVendas

class AppProdutos(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        builder = Gtk.Builder()
        builder.add_from_file("produtos.ui")
        
        self.btn_sair = builder.get_object("btn_sair")
        self.btn_sair.connect("clicked", self.sair)
        
        self.btn_novo = builder.get_object("btn_novo")
        self.btn_novo.connect("clicked", self.novo_produto)

        self.btn_venda = builder.get_object("btn_venda")
        self.btn_venda.connect("clicked", self.efetuar_venda)

        self.btn_consulta_vendas = builder.get_object("btn_consulta_vendas")
        self.btn_consulta_vendas.connect("clicked", self.consulta_vendas)

        self.win_produtos = builder.get_object("win_produtos")
        self.win_produtos.set_application(self)
        
        self.list_produtos = builder.get_object("list_produtos")
        self.list_produtos.set_show_row_separators(True)
        self.list_produtos.set_show_column_separators(True)
        self.list_produtos.set_single_click_activate(True)
        self.list_produtos.connect("activate", self.list_produtos_activate)

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

        #sm = app.get_style_manager()
        #sm.set_color_scheme(Adw.ColorScheme.PREFER_DARK)

        self.get_produtos()

        self.win_produtos.present()

    def get_produtos(self):
        data_access = DataAccess()
        result = data_access.getAll()
        
        self.model = Gio.ListStore(item_type=Produtos)
        for row in result:
            self.model.append(Produtos(idproduto=row[0], produto=row[1], quantidade=row[2], un=row[3], punitario=row[4], total=row[5]))

        self.list_produtos.set_model(Gtk.NoSelection(model=self.model))

    def create_column_to_column_view(self):
        col1 = Gtk.ColumnViewColumn(title="Id", factory=self.factory)
        col1.props.expand = False
        col1.props.fixed_width = 100
        self.list_produtos.append_column(col1)

        col2 = Gtk.ColumnViewColumn(title="Produto", factory=self.factory2)
        col2.props.expand = True
        self.list_produtos.append_column(col2)

        col3 = Gtk.ColumnViewColumn(title="Quantidade", factory=self.factory3)
        col3.props.expand = False
        col3.props.fixed_width = 100
        self.list_produtos.append_column(col3)

        col4 = Gtk.ColumnViewColumn(title="Un", factory=self.factory4)
        col4.props.expand = False
        self.list_produtos.append_column(col4)
        
        col5 = Gtk.ColumnViewColumn(title="Preço Unitário", factory=self.factory5)
        col5.props.expand = False
        col5.props.fixed_width = 100
        self.list_produtos.append_column(col5)

        col6 = Gtk.ColumnViewColumn(title="Total", factory=self.factory6)
        col6.props.expand = False
        col6.props.fixed_width = 100
        self.list_produtos.append_column(col6)

    def sair(self, button):
        self.win_produtos.destroy()

    def _on_factory_setup(self, factory, list_item):
        cell = Gtk.Inscription()
        cell._binding = None
        list_item.set_child(cell)
        
    def _on_factory_bind(self, factory, list_item, what):
        cell = list_item.get_child()
        produtos = list_item.get_item()
        cell._binding = produtos.bind_property(what, cell, "text", GObject.BindingFlags.SYNC_CREATE)

    def list_produtos_activate(self, data, position):
        item = data.get_model()
        produto = item.get_item(position)
        
        try:
            self.form_venda.venda(produto)
            self.form_venda.win_form_venda.present()
        except:
            self.form_venda = FormVenda(self)
            self.form_venda.venda(produto)
            self.form_venda.win_form_venda.present()
        
    def novo_produto(self, widget):
        novo_produto = NovoProduto(self)

    def on_win_produtos_activate_default(self, widget):
        self.get_produtos()
        print("activate-default")

    def efetuar_venda(self, widget):
        self.form_venda = FormVenda(self)
        self.form_venda.win_form_venda.present()

    def consulta_vendas(self, widget):
        form_consulta_vendas = ConsultaVendas()
        form_consulta_vendas.win_consulta_vendas.present()
        
app = AppProdutos(application_id="com.produtos.PapelariaPapelBranco")
app.run(sys.argv)
