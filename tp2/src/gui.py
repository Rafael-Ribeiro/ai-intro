#!/usr/bin/python
# -*- coding: utf-8 -*-

import brach
import sys

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

		# init default values (due to Glade 3.7 bug)
		self.builder.get_object("input_Ax").set_value(brach.A[0])
		self.builder.get_object("input_Ay").set_value(brach.A[1])
		self.builder.get_object("input_Bx").set_value(brach.B[0])
		self.builder.get_object("input_By").set_value(brach.A[1])

		self.builder.get_object("input_population_size").set_value(brach.POPULATION_MAX)
		self.builder.get_object("input_elitism").set_value(brach.ELITISM)
		self.builder.get_object("input_points").set_value(brach.POINTS_INIT)
		self.builder.get_object("input_crossover").set_value(brach.CROSSOVER)
		self.builder.get_object("input_crossover_len").set_value(brach.CROSSOVER_LEN)
		self.builder.get_object("input_mutation_x").set_value(brach.MUTATION_X)
		self.builder.get_object("input_mutation_y").set_value(brach.MUTATION_Y)
		self.builder.get_object("input_mutation_burst").set_value(brach.MUTATION_BURST)

		# init the input_selection_type
		selection_model = gtk.ListStore(str)
		selection_model.append(["Tournament"])
		selection_model.append(["Roulette"])

		selection_box = self.builder.get_object("input_selection_type")
		selection_box.set_model(selection_model)

		cell = gtk.CellRendererText()
		selection_box.pack_start(cell)
		selection_box.add_attribute(cell,'text',0)
		selection_box.set_active(0)

		# show window
		self.builder.connect_signals(self)
		self.builder.get_object('window_main').show()

	def on_adjust_Ax_value_changed(self, widget, data=None):
		brach.A[0] = widget.get_value()

		if branch.A[0] >= branch.B[0]:
			widget.set_value(branch.A[0]-0.1)

		return True

	def on_adjust_Ay_value_changed(self, widget, data=None):
		brach.A[1] = widget.get_value()

		if branch.A[1] < branch.B[1]:
			widget.set_value(branch.A[1] + 0.1)

		return True

	def on_adjust_Bx_value_changed(self, widget, data=None):
		brach.B[0] = widget.get_value()

		if branch.B[0] <= branch.A[0]:
			widget.set_value(branch.B[0] + 0.1)

		return True

	def on_adjust_By_value_changed(self, widget, data=None):
		brach.A[1] = widget.get_value()

		if branch.B[1] > branch.A[1]:
			widget.set_value(branch.B[1] - 0.1)

		return True

	def on_input_population_size_value_changed(self, widget, data=None):
		brach.POPULATION_MAX = widget.get_value_as_int()
		return True

	def on_input_elitism_value_changed(self, widget, data=None):
		brach.ELITISM = widget.get_value()
		return True

	def on_input_selection_type_changed(self, widget, data=None):
		brach.SELECTION_TYPE = widget.get_active_text()
		return True

	def on_input_points_value_changed(self, widget, data=None):
		brach.POINTS_INIT = widget.get_value_as_int()
		return True

	def on_input_crossover_value_changed(self, widget, data=None):
		brach.CROSSOVER = widget.get_value()
		return True

	def on_input_crossover_len_value_changed(self, widget, data=None):
		brach.CROSSOVER_LEN_MAX = widget.get_value()
		return True

	def on_input_mutation_x_value_changed(self, widget, data=None):
		brach.MUTATION_X = widget.get_value()
		return True

	def on_input_mutation_y_value_changed(self, widget, data=None):
		brach.MUTATION_Y = widget.get_value()
		return True

	def on_input_mutation_burst_value_changed(self, widget, data=None):
		brach.MUTATION_BURST = widget.get_value()
		return True

	def on_button_save_activate(self, widget, data=None):
		return True

	def on_button_start_stop_activate(self, widget, data=None):
		return True

	def on_window_main_destroy(self, widget, data=None):
		sys.exit(0)

if __name__ == '__main__':
	gtk.gdk.threads_init()

	app = BrachGUI()
	gtk.main()
