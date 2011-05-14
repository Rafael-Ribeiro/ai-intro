#!/usr/bin/python
# -*- coding: utf-8 -*-

import brach

# program constants
GUI_FILENAME = "gui.xml"

try:
	import gtk
	import gtk.glade
except:
	print "You need to install pyGTK or GTK"
	sys.exit(1)

class BrachGUI:
	def __init__(self):
		self.builder = gtk.Builder()
		self.builder.add_from_file(GUI_FILENAME)
	
		self.builder.connect_signals(self)
		self.builder.get_object('window_main').show()

	def on_input_population_size_value_changed(self, widget, data=None):
		brach.POPULATION_MAX = widget.get_value_as_int()
		print brach.POPULATION_MAX
		return True

	def on_input_elitism_value_changed(self, widget, data=None):
		return True

	def on_input_selection_type_changed(self, widget, data=None):
		return True

	def on_input_points_max_value_changed(self, widget, data=None):
		return True

	def on_input_crossover_value_changed(self, widget, data=None):
		return True

	def on_input_crossover_size_value_changed(self, widget, data=None):
		return True

	def on_input_mutation_x_value_changed(self, widget, data=None):
		return True

	def on_input_mutation_y_value_changed(self, widget, data=None):
		return True

	def on_button_save_activate(self, widget, data=None):
		return True

	def on_button_start_stop_activate(self, widget, data=None):
		return True

	def on_window_destroy(self, widget, data=None):
		sys.exit(0)

if __name__ == '__main__':
	gtk.gdk.threads_init()

	app = BrachGUI()
	gtk.main()
