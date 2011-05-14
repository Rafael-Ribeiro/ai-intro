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
		self.builder.get_object("input_elitism").set_value(brach.ELITISM*100)
		self.builder.get_object("input_points").set_value(brach.POINTS_INIT)
		self.builder.get_object("input_crossover").set_value(brach.CROSSOVER*100)
		self.builder.get_object("input_crossover_len").set_value(brach.CROSSOVER_LEN_MAX*100)
		self.builder.get_object("input_mutation_x").set_value(brach.MUTATION_X*100)
		self.builder.get_object("input_mutation_y").set_value(brach.MUTATION_Y*100)
		self.builder.get_object("input_mutation_burst").set_value(brach.MUTATION_BURST*100)

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

		self.builder.get_object("button_save").set_sensitive(False)
		self.running = False

		# show window
		self.builder.connect_signals(self)
		window = self.builder.get_object('window_main')
		window.set_title("Brachistochrone curve")
		window.show()

	def on_adjust_Ax_value_changed(self, widget, data=None):
		brach.A[0] = widget.get_value()

		if brach.A[0] >= brach.B[0]:
			widget.set_value(brach.A[0]-0.1)

		return True

	def on_adjust_Ay_value_changed(self, widget, data=None):
		brach.A[1] = widget.get_value()

		if brach.A[1] < brach.B[1]:
			widget.set_value(brach.A[1] + 0.1)

		return True

	def on_adjust_Bx_value_changed(self, widget, data=None):
		brach.B[0] = widget.get_value()

		if brach.B[0] <= brach.A[0]:
			widget.set_value(brach.B[0] + 0.1)

		return True

	def on_adjust_By_value_changed(self, widget, data=None):
		brach.A[1] = widget.get_value()

		if brach.B[1] > brach.A[1]:
			widget.set_value(brach.B[1] - 0.1)

		return True

	def on_input_population_size_value_changed(self, widget, data=None):
		brach.POPULATION_MAX = widget.get_value_as_int()
		return True

	def on_input_elitism_value_changed(self, widget, data=None):
		brach.ELITISM = widget.get_value()/100
		return True

	def on_input_selection_type_changed(self, widget, data=None):
		brach.SELECTION_TYPE = widget.get_active_text()
		return True

	def on_input_points_value_changed(self, widget, data=None):
		brach.POINTS_INIT = widget.get_value_as_int()
		return True

	def on_input_crossover_value_changed(self, widget, data=None):
		brach.CROSSOVER = widget.get_value()/100
		return True

	def on_input_crossover_len_value_changed(self, widget, data=None):
		brach.CROSSOVER_LEN_MAX = widget.get_value()/100
		return True

	def on_input_mutation_x_value_changed(self, widget, data=None):
		brach.MUTATION_X = widget.get_value()/100
		return True

	def on_input_mutation_y_value_changed(self, widget, data=None):
		brach.MUTATION_Y = widget.get_value()/100
		return True

	def on_input_mutation_burst_value_changed(self, widget, data=None):
		brach.MUTATION_BURST = widget.get_value()/100
		return True

	def on_button_save_clicked(self, widget, data=None):
		return True

	def on_button_start_stop_clicked(self, widget, data=None):
		self.running = not self.running
		
		if self.running:
			widget.set_label("STOP")
			
			self.builder.get_object("input_Ax").set_sensitive(False)
			self.builder.get_object("input_Ay").set_sensitive(False)
			self.builder.get_object("input_Bx").set_sensitive(False)
			self.builder.get_object("input_By").set_sensitive(False)

			self.builder.get_object("input_population_size").set_sensitive(False)
			self.builder.get_object("input_elitism").set_sensitive(False)
			self.builder.get_object("input_selection_type").set_sensitive(False)

			self.builder.get_object("input_points").set_sensitive(False)
			self.builder.get_object("input_crossover").set_sensitive(False)
			self.builder.get_object("input_crossover_len").set_sensitive(False)
			self.builder.get_object("input_mutation_x").set_sensitive(False)
			self.builder.get_object("input_mutation_y").set_sensitive(False)
			self.builder.get_object("input_mutation_burst").set_sensitive(False)
			
			self.builder.get_object("button_save").set_sensitive(False)

		else:
			widget.set_label("START")

			self.builder.get_object("input_Ax").set_sensitive(True)
			self.builder.get_object("input_Ay").set_sensitive(True)
			self.builder.get_object("input_Bx").set_sensitive(True)
			self.builder.get_object("input_By").set_sensitive(True)

			self.builder.get_object("input_population_size").set_sensitive(True)
			self.builder.get_object("input_elitism").set_sensitive(True)
			self.builder.get_object("input_selection_type").set_sensitive(True)

			self.builder.get_object("input_points").set_sensitive(True)
			self.builder.get_object("input_crossover").set_sensitive(True)
			self.builder.get_object("input_crossover_len").set_sensitive(True)
			self.builder.get_object("input_mutation_x").set_sensitive(True)
			self.builder.get_object("input_mutation_y").set_sensitive(True)
			self.builder.get_object("input_mutation_burst").set_sensitive(True)

			self.builder.get_object("button_save").set_sensitive(True)

		return True

	def on_window_main_destroy(self, widget, data=None):
		sys.exit(0)

if __name__ == '__main__':
	gtk.gdk.threads_init()

	app = BrachGUI()
	gtk.main()
