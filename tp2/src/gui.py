#!/usr/bin/python
# -*- coding: utf-8 -*-

import signal, os

import brach
import sys
from threading import Thread

import matplotlib.pyplot as plot
from matplotlib.backends.backend_gtk import FigureCanvasGTK

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
		self.thread = None
		self.canvasBest = None
		self.canvasHist = None
		self.lastBest = None

		self.builder = gtk.Builder()
		self.builder.add_from_file(GUI_FILENAME)

		# init default values (due to Glade 3.7 bug)
		self.builder.get_object("input_Ax").set_value(brach.A[0])
		self.builder.get_object("input_Ay").set_value(brach.A[1])
		self.builder.get_object("input_Bx").set_value(brach.B[0])
		self.builder.get_object("input_By").set_value(brach.B[1])

		self.builder.get_object("input_population_size").set_value(brach.POPULATION_MAX)
		self.builder.get_object("input_elitism").set_value(brach.ELITISM*100)
		self.builder.get_object("input_points").set_value(brach.POINTS_INIT)
		self.builder.get_object("input_crossover").set_value(brach.CROSSOVER*100)
		self.builder.get_object("input_crossover_len").set_value(brach.CROSSOVER_LEN_MAX*100)
		self.builder.get_object("input_mutation").set_value(brach.MUTATION*100)
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

	def on_input_mutation_value_changed(self, widget, data=None):
		brach.MUTATION = widget.get_value()/100
		return True

	def on_input_mutation_y_value_changed(self, widget, data=None):
		brach.MUTATION_Y = widget.get_value()/100
		return True

	def on_input_mutation_burst_value_changed(self, widget, data=None):
		brach.MUTATION_BURST = widget.get_value()/100
		return True

	def on_button_save_clicked(self, widget, data=None):
		# TODO: http://www.pygtk.org/pygtk2tutorial/sec-FileChoosers.html
		# chooser.set_action(gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER)
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
			self.builder.get_object("input_mutation").set_sensitive(False)
			self.builder.get_object("input_mutation_y").set_sensitive(False)
			self.builder.get_object("input_mutation_burst").set_sensitive(False)
			
			self.builder.get_object("button_save").set_sensitive(False)

			self.population = brach.Population.new(brach.POPULATION_MAX)

			self.thread = Thread(target=self.evolve)
			self.thread.start()

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
			self.builder.get_object("input_mutation").set_sensitive(True)
			self.builder.get_object("input_mutation_y").set_sensitive(True)
			self.builder.get_object("input_mutation_burst").set_sensitive(True)

			self.builder.get_object("button_save").set_sensitive(True)
			self.lastBest = None

		return True

	def on_window_main_destroy(self, widget, data=None):
		app.running = False
		if app.thread != None:
			app.thread.join()
		sys.exit(0)

	def evolve(self):
		i = 0
		while self.running:
			self.population.evolve()
	
			print "Iteration", i, self.population.getStatistics()

			if self.lastBest == None or self.population.getBest().fitness() != self.lastBest.fitness():
				self.lastBest = self.population.getBest()
				points = self.lastBest.getPlotData()
			
				figureBest = plot.Figure(figsize=(400,400), dpi=72)
				graphBest = figureBest.add_subplot(111)
				graphBest.fill_between(points[0], points[1], color = 'r')
				graphBest.axis([0, brach.B[0], 0, brach.A[1]])
				
				vbox = self.builder.get_object("vbox_graphs")  

				if self.canvasBest != None:
					vbox.remove(self.canvasBest)
			
				self.canvasBest = FigureCanvasGTK(figureBest)
				self.canvasBest.show()
				import time
				time.sleep(0.01)
				vbox.pack_start(self.canvasBest, True, True)

			if self.canvasHist != None:
				vbox.remove(self.canvasHist)

			i += 1

if __name__ == '__main__':
	gtk.gdk.threads_init()

	app = BrachGUI()

	try:
		gtk.main()

	except KeyboardInterrupt:
		app.running = False
		if app.thread != None:
			app.thread.join()
		sys.exit(0)
