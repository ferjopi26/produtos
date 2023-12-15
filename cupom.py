import gi
from data_access import DataAccess
from fpdf import FPDF
from date_utils import DateUtils

gi.require_version("Gtk", "4.0")
gi.require_version("GLib", "2.0")
gi.require_version('Poppler', '0.18')
#gi.require_version('Pango', '1.0')

from gi.repository import GLib
from gi.repository import Adw, Gio, GObject, Gtk
from gi.repository import Poppler
#from gi.repository import Pango

class Cupom(FPDF):
    def __init__(self, venda, nf, total_geral, parent):
        super(Cupom, self).__init__('P', 'pt', 'A4')
        
        self.parent = parent
        self.venda = venda
        self.nf = nf
        self.total_geral = total_geral
        self.current_page = 1

        self.alias_nb_pages()
        self.add_page()
        
        self.data = self.output('Cupom.pdf', 'S').encode("latin1")

        self.document = Poppler.Document.new_from_bytes(GLib.Bytes(self.data), None)
        self.n_pages = self.document.get_n_pages()
        self.current_page = self.document.get_page(0)       
        
        builder = Gtk.Builder()
        builder.add_from_file("cupom.ui")

        self.win_cupom = builder.get_object("win_cupom")

        btn_spin = builder.get_object("btn_spin")
        adjust = builder.get_object("adjust")

        btn_fechar = builder.get_object("btn_fechar")
        btn_fechar.connect("clicked", self.fechar)

        btn_print = builder.get_object("btn_print")
        btn_print.connect("clicked", self.print)

        self.dwg = builder.get_object("dwg")
        self.dwg.set_draw_func(self.draw, self)

    def fechar(self, widget):
        self.win_cupom.destroy()

    def print(self, widget):
        self.document = Poppler.Document.new_from_bytes(GLib.Bytes(self.data), None)
        po = Gtk.PrintOperation()
        po.set_show_progress(True)
        po.set_n_pages(self.document.get_n_pages())
        po.connect("draw_page", self.draw_page)
        po.run(Gtk.PrintOperationAction.PRINT_DIALOG, self.parent)

    def draw_page (self, operation, context, page_num):
        page = self.document.get_page(page_num)
        page.render_for_printing(context.get_cairo_context())
    
    def header(self):
        date_utils = DateUtils()
        date = date_utils.formatedCurrentDate()

        try:
            date = self.venda[0].data
        except:
            date = date_utils.formatedCurrentDate()

        self.set_font('Arial', '', 10)

        self.set_xy(20, 10)
        self.cell(500, 10, u'Papelaria Papel Branco', 0, 1, 'C')

        self.set_xy(20, 20)
        self.cell(500, 10, u"Comprovante de venda ao consumidor", 0, 1, 'C')

        self.set_xy(20, 30)
        self.cell(500, 10, u'Sem valor fiscal', 0, 1, 'C')
        
        self.dashed_line(10, 50, 570, 50, 5, 5)

        self.set_xy(20, 60)
        self.cell(100, 10, date, 0, 1,'L')

        self.set_xy(120, 60)
        self.cell(100, 10, f"Comprovante nº {self.nf}", 0, 1, 'L')

        self.dashed_line(10, 70, 570, 70, 5, 5)

        self.set_xy(20, 80)
        self.cell(50, 10, "Item", 0, 0, 'L')
        self.cell(200, 10, "Produto", 0, 0, 'L')
        self.cell(60, 10, "Quantidade", 0, 0, 'L')
        self.cell(60, 10, u"P. Unitário", 0, 0, 'L')
        self.cell(60, 10, "Total", 0, 1, 'L')

        self.dashed_line(10, 90, 570, 90, 5, 5)

        self.ln(5)

        self.current_y = 100

        self.body()

    def body(self):
        for i in range(len(self.venda)):
            self.set_xy(20, self.current_y)

            self.cell(50, 10, str(self.venda[i].idproduto), 0, 0, 'R')
            self.cell(200, 10, self.venda[i].produto, 0, 0, 'L')
            self.cell(60, 10, str(self.venda[i].quantidade), 0, 0, 'R')
            self.cell(50, 10, str(self.venda[i].punitario), 0, 0, 'R')
            self.cell(50, 10, str(self.venda[i].total), 0, 1, 'R')
            
            self.current_y += 10
        
        self.dashed_line(10, self.current_y, 570, self.current_y, 5, 5)

        self.cell(100, 10, "Total do Cupom: ", 0, 0, "l")
        self.cell(50, 10, "{:.{}f}".format(self.total_geral, 2), 0, 0, 'R')

        self.current_y += 10
        self.dashed_line(10, self.current_y, 570, self.current_y, 5, 5)

    def draw(self, dwg, context, width, height, data):
        context.set_source_rgb(1, 1, 1)
        context.paint()

        self.current_page.render(context)

        if self.current_page == 0:
            return
        