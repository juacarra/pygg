#!/usr/bin/env python
# -*- coding: utf-8 -*-
# GladeConnect -- Clase base para conectar glade y python

# This file is part of Gestor.
#
# Gestor is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# pyGestor is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Foobar; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

# Copyright Benjamin POUSSIN < bpoussin@free.fr >, 
# Sebastien REGNIER < seb.regnier@free.fr >
# Benoit CLOUET < b.clouet@free.fr > 

import pygtk
pygtk.require('2.0')

import gtk.glade
import gtk
import sys
import os
import inspect
import time

class PrefixActions:
    def __init__(self):
        self.mandatories = []
    
    def prefix_ent(self, widget):
        def validate(widget):
            text = widget.get_text().strip()
            self.set_error_status(widget, len(text) < 1)
        def complete(widget, event):
            text = widget.get_text().strip()
            widget.set_text(text.upper())
        widget.connect("changed", validate)
        widget.connect("focus-out-event", complete)
        
    def prefix_Ent(self, widget):
        self.prefix_ent(widget)
        self.add_mandatory(widget)
    
    def prefix_name(self, widget):
        def validate(widget):
            text = widget.get_text()
            self.set_error_status(widget, len(text) < 1 or len(text) > 16)
        def complete(widget, event):
            text = widget.get_text()
            cap = lambda s: s.capitalize()
            tokens = text.split()
            tokens = map(cap, tokens)
            text = " ".join(tokens)
            widget.set_text(text)
        widget.connect("changed", validate)
        widget.connect("focus-out-event", complete)
    
    def prefix_Name(self, widget):
        self.prefix_name(widget)
        self.add_mandatory(widget)
    
    def prefix_date(self, widget):
        def parse_date(text):
            (cY,cm,cd) = time.localtime()[0:3]
            try:
                (d,) = time.strptime(text, "%d")[2:3]
                m,Y = cm,cY
            except ValueError:
                try:    
                    (m,d) = time.strptime(text, "%d/%m")[1:3]
                    Y = cY
                except:
                    (Y,m,d) = time.strptime(text, "%d/%m/%Y")[0:3]
            return (Y,m,d)
        def validate(widget):
            text = widget.get_text()
            try:
                parse_date(text)
                error = False
            except ValueError:
                error = True
            self.set_error_status(widget,error)
        def complete(widget, event):
            text = widget.get_text()
            try:
                (Y,m,d) = parse_date(text)
                text = "%02d/%02d/%d" % (d,m,Y)
                widget.set_text(text)
                error = False
            except ValueError:
                error = True
            self.set_error_status(widget,error)
        widget.connect("changed", validate)
        widget.connect("focus-out-event", complete)
        
    def prefix_Date(self, widget):
        self.prefix_date(widget)
        self.add_mandatory(widget)
    
    def prefix_age(self, widget):
        def validate(widget):
            text = widget.get_text()
            try:
                age = int(text)
                if age < 16 or age > 99:
                    raise ValueError
                error = False
            except ValueError:
                error = True
            self.set_error_status(widget,error)
        widget.connect("changed", validate)

    def prefix_Age(self, widget):
        self.prefix_age(widget)
        self.add_mandatory(widget)

    def prefix_cash(self, widget):
        def validate(widget):
            text = widget.get_text()
            try:
                cash = float(text)
                if cash < 0:
                    raise ValueError
                error = False
            except ValueError:
                error = True
            self.set_error_status(widget,error)
        self.add_mandatory(widget)
        widget.connect("changed", validate)
    
    def prefix_Cash(self, widget):
        self.prefix_cash(widget)
        self.add_mandatory(widget)
        
    def prefix_rut(self,widget):
        def Format_Rut(widget, event):
            rut = widget.get_text()
            if rut == "":
                return rut
        
            rut = rut.replace(".","")
            rut = rut.replace("-","")
            rut = "0000000000"+ rut
            l = len(rut)
            rut_aux = "-" + rut[l-1:l]
            l = l-1
            while 2 < l:
                rut_aux = "."+ rut[l-3:l] +rut_aux
                l = l-3
        
            rut_aux = rut[0:l] +rut_aux
            l = len(rut_aux)
            rut_aux = rut_aux[l-12:l]
            widget.set_text(rut_aux)
            
        def es_rut(rut=None):
            if not rut: return 0
            es_rut = False
            cadena = "234567234567"
            dig_rut = rut[-1]
            rut = rut.replace(".", "")
            rut = rut[:rut.find("-")]
            rut = rut.replace(" ", '0')
            j, suma, i = 0, 0, len(rut) -1
            while i >= 0:
                    try:
                            suma = suma + (int(rut[i]) * int(cadena[j]))
            
                    except:
                            return 0
            
                    i = i - 1
                    j = j + 1
                
            divid = int(suma/11)
            mult = int(divid*11)
            dife = suma - mult
            digito = 11 - dife
            if digito == 10:
                    caract = "K"
        
            elif digito == 11:
                    caract = "0"
        
            else:
                    caract = str(digito).replace(" ", "")
        
            if caract == dig_rut: 
                    es_rut = True
        
            return es_rut
        
        def validate(widget):
            text = widget.get_text()
            try:
                cash = not es_rut(text)
                if cash :
                    raise ValueError
                error = False
            except ValueError:
                error = True
            self.set_error_status(widget,error)
        widget.connect("changed", validate)
        widget.connect("focus-out-event", Format_Rut)
    
    def prefix_Rut(self, widget):
        self.prefix_rut(widget)
        self.add_mandatory(widget)
        
    def add_mandatory(self, widget):
        self.mandatories.append(widget)
        label_prefix = '<b><span color="red">*</span></b>'
        eid = widget.get_name()[3: ]
        label = getattr(self,"lbl%s" % eid)
        markup = label_prefix + label.get_label()
        label.set_markup(markup)

    def set_error_status(self, widget, error_status):
        if error_status:
            color_s = "#FF6B6B"
            widget.set_data("is-valid", None)
        else:
            widget.set_data("is-valid", True)
            color_s = "#FFFFFF"
        color = gtk.gdk.color_parse(color_s)
        widget.modify_base(gtk.STATE_NORMAL, color)
        can_apply = True
        for mandatory in self.mandatories:
            if not mandatory.get_data("is-valid"):
                can_apply = False
        self.btnAceptar.set_sensitive(can_apply)   

class GladeConnect(dict, PrefixActions):
    """
    Permite usar ficheros glade de manera automática. Modo de uso
    GladeConnect.__init__(self, "nombre_fichero.glade").

    Los widgets pueden ser tratados de la siguiente manera:
    self.nomnbre_widget
    
    Los callbacks de las señales se autoconectan directamente, utilize
    la nomeclatura:
    def callback_declare(self, source=None, event=None):
    """

    def __init__(self, filename, root=None):
        """
        root vous permet de specifier une fenetre particuliere du fichier
        .glade. Cela est util si vous avez mis plusieurs fen�tres dans le
        m�me fichier.
        """
        dirname = os.path.dirname(sys.argv[0])
        if dirname != '':
            dirname = dirname + os.sep

        self.ui = gtk.glade.XML(dirname+filename, root)
        self.connect()
        PrefixActions.__init__(self)
        self.add_prefix_actions()
        
    def cree_dico (self):
        dico = {} ## dico vide pour commencer
        self.cree_dico_pour_classe (self.__class__, dico)
        return dico

    def cree_dico_pour_classe (self, une_classe, dico):
        bases = une_classe.__bases__
        for iteration in bases:
            self.cree_dico_pour_classe (iteration, dico) ## Appel recursif
        for iteration in dir(une_classe):
            dico[iteration]=getattr(self,iteration)

    def connect(self):
        self.ui.signal_autoconnect(self) 

    def __getattr__(self, name):
		if name in self:
			data = self[name]
			return data
		else:
			widget = self.ui.get_widget(name)
			if widget != None:
				self[name] = widget
				return widget
			else:
				raise AttributeError, name

    def on_exit(self, source=None, event=None):
        try:
            gtk.main_quit()
        except:
            pass
            
    def run(self):
        gtk.main()
    
    def quit(self):
        self.on_exit()
        
    def clear_form(self):
        for i in self.keys():
            if type(self[i]) == type(gtk.Entry()):
                self[i].set_text("")
            elif type(self[i]) == type(gtk.SpinButton()):
                min, max = self[i].get_range()
                self[i].set_value(min)

    def add_prefix_actions(self, prefix_actions_proxy=None):
        if not prefix_actions_proxy is None:
            actions = prefix_actions_proxy
        else:
            actions = self
        prefix_s = "prefix_"
        prefix_pos = len(prefix_s)

        is_method = lambda t : callable( t[1] )
        is_prefix_action = lambda t : t[0].startswith(prefix_s)
        drop_prefix = lambda (k,w): (k[prefix_pos:],w)
        
        members_t = inspect.getmembers(actions)
        methods_t = filter(is_method, members_t)
        prefix_actions_t = filter(is_prefix_action, methods_t)
        prefix_actions_d = dict(map(drop_prefix, prefix_actions_t) )

        for widget in self.ui.get_widget_prefix(""):
            widget_name = widget.get_name()
            prefixes_name_l = widget_name.split(":")
            prefixes = prefixes_name_l[ : -1]
            widget_api_name = prefixes_name_l[-1]
            widget.set_name(widget_api_name)
            self[widget_api_name] = widget
            if prefixes:
                widget.set_data("prefix", prefixes)
                for prefix in prefixes:
                    if prefix in prefix_actions_d:
                        prefix_action = prefix_actions_d[prefix]
                        prefix_action(widget)

