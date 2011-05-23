#!/usr/bin/python
# -*- coding: utf-8 -*-

import signal, os
from population import *

import sys
from threading import Thread

from datetime import datetime, timedelta

from matplotlib.pyplot import figure
from matplotlib.backends.backend_gtk import Figure, FigureCanvasGTK
import gobject

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
		self.lastUpdate = datetime.now()
		self.thread = None
		self.lastBest = None

		self.builder = gtk.Builder()
		self.builder.add_from_file(GUI_FILENAME)

		# init default values (due to Glade 3.7 bug)
		self.builder.get_object("input_Ax").set_value(config.A[0])
		self.builder.get_object("input_Ay").set_value(config.A[1])
		self.builder.get_object("input_Bx").set_value(config.B[0])
		self.builder.get_object("input_By").set_value(config.B[1])

		self.builder.get_object("input_population_size").set_value(config.POPULATION_SIZE)
		self.builder.get_object("input_elitism").set_value(config.ELITISM*100)
		self.builder.get_object("input_points").set_value(config.POINTS_INIT)
		self.builder.get_object("input_crossover").set_value(config.CROSSOVER*100)
		self.builder.get_object("input_crossover_len").set_value(config.CROSSOVER_LEN_MAX*100)
		self.builder.get_object("input_mutation").set_value(config.MUTATION_PROB*100)
		self.builder.get_object("input_mutation_burst").set_value(config.MUTATION_BURST*100)

		self.builder.get_object("button_save").set_sensitive(False)
		self.running = False

		# init the input_selection_type
		selection_model = gtk.ListStore(str)
		selection_model.append(["Tournament"])
		selection_model.append(["Roulette"])
		selection_model.append(["Rafael-Ribeiro"])

		selection_box = self.builder.get_object("input_selection_type")
		selection_box.set_model(selection_model)

		cell = gtk.CellRendererText()
		selection_box.pack_start(cell)
		selection_box.add_attribute(cell,'text',0)
		selection_box.set_active(0)

		# init the input_representation
		representation_model = gtk.ListStore(str)
		representation_model.append(["Even spacing"])
		representation_model.append(["Dynamic spacing"])

		representation_box = self.builder.get_object("input_representation")
		representation_box.set_model(representation_model)

		cell = gtk.CellRendererText()
		representation_box.pack_start(cell)
		representation_box.add_attribute(cell,'text',0)
		representation_box.set_active(0)

		# init graphs
		self.fig_best = Figure(figsize=(400, 400))
		self.fig_hist = Figure(figsize=(400, 200))
		
		self.canvas_best = FigureCanvasGTK(self.fig_best)
		self.canvas_hist = FigureCanvasGTK(self.fig_hist)
		self.canvas_best.show()
		self.canvas_hist.show()

		self.hbox_best = self.builder.get_object("hbox_graph_best")
		self.hbox_hist = self.builder.get_object("hbox_graph_hist")

		self.hbox_best.pack_start(self.canvas_best, True, True)
		self.hbox_hist.pack_start(self.canvas_hist, True, True)

		# show window
		self.builder.connect_signals(self)
		window = self.builder.get_object('window_main')
		window.set_title("Brachistochrone curve")
		window.show()

	def on_adjust_Ax_value_changed(self, widget, data=None):
		config.A[0] = widget.get_value()

		self.on_update_points()
		return True

	def on_adjust_Ay_value_changed(self, widget, data=None):
		config.A[1] = widget.get_value()

		self.on_update_points()
		return True

	def on_adjust_Bx_value_changed(self, widget, data=None):
		config.B[0] = widget.get_value()

		self.on_update_points()
		return True

	def on_adjust_By_value_changed(self, widget, data=None):
		config.B[1] = widget.get_value()

		self.on_update_points()
		return True

	def on_input_population_size_value_changed(self, widget, data=None):
		config.POPULATION_SIZE = widget.get_value_as_int()
		return True

	def on_input_elitism_value_changed(self, widget, data=None):
		config.ELITISM = widget.get_value()/100
		return True

	def on_input_selection_type_changed(self, widget, data=None):
		config.SELECTION_TYPE = widget.get_active_text()
		return True

	def on_input_representation_changed(self, widget, data=None):
		config.REPRESENTATION = widget.get_active_text()
		return True

	def on_input_points_value_changed(self, widget, data=None):
		config.POINTS_INIT = widget.get_value_as_int()
		return True

	def on_input_crossover_value_changed(self, widget, data=None):
		config.CROSSOVER = widget.get_value()/100
		return True

	def on_input_crossover_len_value_changed(self, widget, data=None):
		config.CROSSOVER_LEN_MAX = widget.get_value()/100
		return True

	def on_input_mutation_value_changed(self, widget, data=None):
		config.MUTATION_PROB = widget.get_value()/1005.0

		burst = self.builder.get_object("input_mutation_burst")
		m = 100-config.MUTATION_PROB*100

		if burst.get_value() > m:
			burst.set_value(m)

		burst.get_adjustment().set_upper(m)
		return True

	def on_input_mutation_burst_value_changed(self, widget, data=None):
		config.MUTATION_BURST = widget.get_value()/100
		return True

	def on_button_save_clicked(self, widget, data=None):
		dialog = gtk.FileChooserDialog("Choose a folder...",
			None,
			gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
			(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK)
		)
		dialog.set_default_response(gtk.RESPONSE_OK)

		response = dialog.run()
		if response == gtk.RESPONSE_OK:
			points = self.population.getBest().getPoints()

			f = open(dialog.get_filename() + '/data', 'w')
			f.write(str(self.iteration_list[-1])+"\n")
			f.write(str(self.best_list)+"\n")
			f.write(str(self.avg_list)+"\n")
			f.write(str(self.worst_list)+"\n")
			f.write(str(self.stddev_list)+"\n")
			f.write(str(points)+"\n")
			f.close()

			figureBest = figure(figsize=(3.0,3.0), dpi=72)
			graphBest = figureBest.add_axes([0, config.B[0], 0, config.A[1]])
			graphBest.plot(points[0], points[1], 'r-*')
			figureBest.savefig(dialog.get_filename() + '/best.png', format="png", transparent=True)

		dialog.destroy()
		return True

	def on_button_start_stop_clicked(self, widget, data=None):
		if not self.running and (config.A[1] <= config.B[1] or config.B[0] <= config.A[0]):
			md = gtk.MessageDialog(self.builder.get_object('window_main'), gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE, "Invalid start/end points!")
			md.run()
			md.destroy()

			return True

		self.running = not self.running
		
		if self.running:
			widget.set_label("STOP")
			
			self.best_list = []
			self.avg_list = []
			self.worst_list = []
			self.stddev_list = []
			self.iteration_list = []

			self.builder.get_object("input_Ax").set_sensitive(False)
			self.builder.get_object("input_Ay").set_sensitive(False)
			self.builder.get_object("input_Bx").set_sensitive(False)
			self.builder.get_object("input_By").set_sensitive(False)

			self.builder.get_object("input_population_size").set_sensitive(False)
			self.builder.get_object("input_elitism").set_sensitive(False)
			self.builder.get_object("input_selection_type").set_sensitive(False)
			self.builder.get_object("input_representation").set_sensitive(False)

			self.builder.get_object("input_points").set_sensitive(False)
			self.builder.get_object("input_crossover").set_sensitive(False)
			self.builder.get_object("input_crossover_len").set_sensitive(False)
			self.builder.get_object("input_mutation").set_sensitive(False)
			self.builder.get_object("input_mutation_burst").set_sensitive(False)
			
			self.builder.get_object("button_save").set_sensitive(False)

			self.population = Population.new(config.POPULATION_SIZE, config.REPRESENTATION)

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
			self.builder.get_object("input_representation").set_sensitive(True)

			self.builder.get_object("input_points").set_sensitive(True)
			self.builder.get_object("input_crossover").set_sensitive(True)
			self.builder.get_object("input_crossover_len").set_sensitive(True)
			self.builder.get_object("input_mutation").set_sensitive(True)
			self.builder.get_object("input_mutation_burst").set_sensitive(True)

			self.builder.get_object("button_save").set_sensitive(True)
			self.lastBest = None

		return True

	def on_update_points(self):
		config.DX = float(config.B[0] - config.A[0])
		config.DY = float(config.B[1] - config.A[1])
		config.MUTATION_X_STDEV = (config.A[0] - config.B[0])/10	# standard deviation
		config.MUTATION_Y_STDEV = (config.A[1] - config.B[1])/10	# standard deviation

	def on_window_main_destroy(self, widget, data=None):
		app.running = False
		if app.thread != None:
			app.thread.join()
		sys.exit(0)

	def evolve(self):
		i = 0
		while self.running:
			self.population.evolve()

			stats = self.population.getStatistics()
			print "Iteration", i, stats

			self.best_list.append(stats[0])
			self.avg_list.append(stats[1])
			self.worst_list.append(stats[2])
			self.stddev_list.append(stats[3])
			self.iteration_list.append(i)

			if datetime.now() > self.lastUpdate + timedelta(seconds=5):
				gobject.idle_add(self.plot)

			i += 1

	def plot(self):
		self.lastUpdate = datetime.now()

		points = self.population.getBest().getPoints()

		self.fig_best.clf()
		self.fig_hist.clf()

		graph_best = self.fig_best.add_subplot(111)
		graph_best.plot(points[0], points[1], 'r-*')
		graph_best.axis([0, config.B[0], 0, config.A[1]])

		graph_hist = self.fig_hist.add_subplot(111)
		graph_hist.plot(self.iteration_list[-100:], self.best_list[-100:], 'b', self.iteration_list[-100:], self.avg_list[-100:], 'g', self.iteration_list[-100:], self.worst_list[-100:], 'r')
		graph_hist.axis([max(0, self.iteration_list[-1]-100), self.iteration_list[-1], 0, 4.0])

		self.fig_best.canvas.draw()
		self.fig_hist.canvas.draw()

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
