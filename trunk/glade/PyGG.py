from GladeConnect import *
import gtk

class NuevaApp(GladeConnect):
    def __init__(self):
        GladeConnect.__init__(self, '/home/juacarra/Desktop/Generador PyGG/glade/PyGG.glade')

    def on_Generar(self,*args):
        pass

    def on_Salir(self,*args):
        gtk.main_quit()

    def on_cmdBuscar_clicked(self,*args):
        pass

    def on_cmdDlg_clicked(self,*args):
        pass

    def on_mnuAbrir_activate(self,*args):
        pass

    def on_mnuAcerca_de_activate(self,*args):
        pass



if __name__ == '__main__':
    app = NuevaApp()
    gtk.main()