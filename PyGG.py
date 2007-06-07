#!/usr/bin/env python
# -*- coding: utf-8 -*-

#PyGG es una herramienta que facilita el desarrollo
#de aplicaciones utilizando python + glade + GladeConnect

#   Copyright © Juan R. Carrasco G. 
#               juacarra@gmail.com

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

from GladeConnect import *
import gtk
from os import system
import SimpleTree


class PyGG(GladeConnect):
    
    def __init__(self):
        GladeConnect.__init__(self, "glade/PyGG.glade","frmMain")
        self.frmMain.set_size_request(550,550)
        self.crea_columnas()
        self.lista = []
        self.archivo = ''
        #selector.hide()	
        
    def crea_columnas(self):
        modelo = self.lvwManejadores.get_model()
        if modelo:		
            return
        
        modelo = gtk.ListStore(bool, str, str)
        columnas = []
        columnas.append([0 ,'Escribir','bool'])
        columnas.append([1 ,'Manejador','str'])
        columnas.append([2 ,'Accion','str',None,True])
        SimpleTree.GenColsByModel(modelo, columnas, self.lvwManejadores)    

    def cargaList(self,path):
        modelo = self.lvwManejadores.get_model()
        self.archivo = Archivo(path)
        self.lista = self.archivo.leerArchivo()
        try:
            self.archivo.cerrarArchivo()
        except:
            return
        try:
            for item in self.lista:
                modelo.append([True,item,"pass"])
        except:
            return
        self.lvwManejadores.set_model(modelo)

    def on_Salir(self, objeto):
        gtk.main_quit()
    
    def on_cmdBuscar_clicked(self, btn):
        dlg = Selector(self.frmMain)
        response=dlg.dlgSelector.run()
        if response == gtk.RESPONSE_OK:
            path = dlg.dlgSelector.get_filename()
            if path.find('.') == -1:
                return
            self.cargaList(path)
            self.txtOrigen.set_text(path)
            self.txtArchivo.set_text(path.replace('.glade','.py'))
            self.txtClase.set_text('NuevaApp')
    
    def on_Generar(self, widget):
        o = self.txtOrigen.get_text()
        d = self.txtArchivo.get_text()
        c = self.txtClase.get_text()
        if o == '' or d == '' or c == '':
            return
        if self.archivo == '':
            return
        acciones = []
        modelo = self.lvwManejadores.get_model()
        #for i in range(0,len(modelo)):
        #    acciones.append(modelo[i][0])
        #print acciones
        self.archivo.creaArchivo(o,d,c,modelo)
        self.archivo.cerrarArchivo()

    def on_mnuAcerca_de_activate(self, btn):
        ad = AcercaDe()
        
    def on_lvwManejadores_toggle_cursor_row(self,*args):
        print 'si0'
        
class Selector(GladeConnect):
    def __init__ (self, padre = None):
        GladeConnect.__init__(self, "glade/PyGG.glade", "dlgSelector")
        self.dlgSelector.set_transient_for(padre)

    def on_cmdDlg_clicked(self, btn=None):
        self.dlgSelector.hide()
        
    
class AcercaDe(GladeConnect):
    def __init__(self):
        GladeConnect.__init__(self, "glade/AcercaDe.glade")

    def on_okbutton1_clicked(self, ventana):
        self.frmAcercaDe.destroy()

class Archivo:
    '''Clase Archivo se instancia recibiendo como parametro 
    la path de un archivo generado por glade'''
    
    def __init__(self, path):
        if path[path.find('.') + 1:] <> 'glade':
            aviso(None,"El archivo no es valido...")
            self.archivo = None
            return
        try:
            self.archivo = open(path,'r')
        except:
            self.archivo = None
            aviso(None,"El Archivo no se ha podido leer...")
    
    def leerArchivo(self):
        ''' lee el archivo *.glade y busca los manejadores de eventos
        para devolverlos en un arreglo'''
        
        if self.archivo == None:
            return
        devuelve, lista = [],[]
        for linea in self.archivo:
            lugar = linea.find('handler=')#busco la parte del manejador
            if  lugar <> -1:#si es igual a -1 es porque no lo encontro
                linea = linea[lugar + 9:]#al sumarle 9 le quito el 'handler="'
                lugar = linea.find(' ')#busco el espacio final del manejador
                lista.append(linea[:lugar - 1])#le quito 1 para eliminar el ultimo ' " '
        lista.sort()
        ant = ''
        for actual in lista:
            if ant <> actual:
                devuelve.append(actual)
                ant = actual
        return devuelve
    
    def cerrarArchivo(self):
        '''Cierra el archivo'''
        if self.archivo == None:
            return False
        self.archivo.close()
        
    def creaArchivo(self,pathOrigen,pathDestino,
                    nombreClase,manejadoresEventos=None,
                    acciones = None):
        '''Crea un archivo *.py con todos los manejadores de eventos 
        incluidos'''
        texImport = """from GladeConnect import *\nimport gtk\n"""
        texClase = """\nclass %s(GladeConnect):\n""" %(nombreClase)
        texInit = """    def __init__(self):\n        GladeConnect.__init__(self, '%s')\n\n""" %(pathOrigen)
        textIfMain = """\n\nif __name__ == '__main__':\n    app = %s()\n    gtk.main()""" %(nombreClase)
        try:
            self.archivo = open(pathDestino,'w')
            try:
                self.archivo.write(texImport + texClase + texInit)
                for dato in manejadoresEventos:
                    if dato[0] == True:
                        self.archivo.write("""    def %s(self,*args):\n        %s\n\n""" % (dato[1],dato[2]))
                self.archivo.write(textIfMain)
                self.archivo.close()
            finally:
                self.archivo.close()
        except:
            aviso(None,'Error de escritura...\nEl destino no es valido')
	self.copiarArchivo(pathDestino)
	
    def copiarArchivo(self,destino):
	cont = 0
	for caracter in destino:
	    if caracter == '/':
		lugar = cont
	    cont = cont + 1
	destinoGladeConnect = destino[:lugar] + '/GladeConnect.py'
	#aviso(None,destino)
	try:
	    archivoOrigen = open('GladeConnect.py','r')
	    archivoDestino = open(destinoGladeConnect ,'w')
	    for linea in archivoOrigen:
		archivoDestino.write(linea)
	    archivoDestino.close()
	    archivoOrigen.close()
	    
	    respuesta = aviso(None,'El archivo ha sido creado con exito\nDesea ejecutarlo?',gtk.BUTTONS_YES_NO)
	    if respuesta == -8:
		#system('gnome-terminal --working-directory=' + destino[:lugar] + ' -x python ' + destino[lugar +1:])
                system('gnome-terminal -x python ' + destino[lugar +1:])
        except:
	    aviso(None,'Error no se a podido copiar\nel archivo GladeConnect.py')
	    
	
def aviso(GtkWindow, mensaje,botones = gtk.BUTTONS_OK):
    '''parametros.....
            GtkWindow: 		
                objeto GtkWindow, ventana desde la cual se realiza
                la solicitud del mensaje
            mensaje:
                mensaje a ser presentado'''
    
    m = mensaje
    m = unicode(m,'latin-1')
    dialog = gtk.MessageDialog(GtkWindow, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,gtk.MESSAGE_INFO, botones, m.encode('utf-8'))
    dialog.show_all()
    response = dialog.run()
    dialog.destroy()
    return response
    
if __name__ == "__main__":
    ejecuta = PyGG()
    gtk.main()