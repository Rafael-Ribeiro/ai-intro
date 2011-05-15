#!/usr/bin/python
# -*- coding: utf-8 -*-

import signal, os

import brach
import sys
from threading import Thread

from datetime import datetime, timedelta

import matplotlib.pyplot as plot
from matplotlib.backends.backend_gtk import Figure, FigureCanvasGTK

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

		dialog = gtk.FileChooserDialog("Choose a folder..",
			None,
			gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
			(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK)
		)
		dialog.set_default_response(gtk.RESPONSE_OK)

		response = dialog.run()
		if response == gtk.RESPONSE_OK:
			points = self.population.getBest().getPlotData()

			f = open(dialog.get_filename() + '/data', 'w')
			f.write(str(self.iteration_list[-1])+"\n")
			f.write(str(self.best_list)+"\n")
			f.write(str(self.avg_list)+"\n")
			f.write(str(self.worst_list)+"\n")
			f.write(str(self.stddev_list)+"\n")
			f.write(str(points)+"\n")
			f.close()

			figureBest = plot.Figure(figsize=(400,400), dpi=72)
			graphBest = figureBest.add_subplot(111)
			graphBest.plot(points[0], points[1], 'r-*')
			graphBest.axis([0, brach.B[0], 0, brach.A[1]])
			figureBest.savefig(dialog.get_filename() + '/best.png')

		dialog.destroy()
		return True

	def on_button_start_stop_clicked(self, widget, data=None):
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
	
			stats = self.population.getStatistics()
			print "Iteration", i, stats

			self.best_list.append(stats[0])
			self.avg_list.append(stats[1])
			self.worst_list.append(stats[2])
			self.stddev_list.append(stats[3])
			self.iteration_list.append(i)

			if datetime.now() > self.lastUpdate + timedelta(seconds=5):
				self.lastUpdate = datetime.now()

				# best solution
				points = self.population.getBest().getPlotData()

				self.fig_best.clf()
				self.fig_hist.clf()

				graph_best = self.fig_best.add_subplot(111)
				graph_best.plot(points[0], points[1], 'r-*')
				graph_best.axis([0, brach.B[0], 0, brach.A[1]])

				graph_hist = self.fig_hist.add_subplot(111)
				graph_hist.plot(self.iteration_list[-100:], self.best_list[-100:], 'b', self.iteration_list[-100:], self.avg_list[-100:], 'g', self.iteration_list[-100:], self.worst_list[-100:], 'r')

				self.fig_best.canvas.draw()
				self.fig_hist.canvas.draw()

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
