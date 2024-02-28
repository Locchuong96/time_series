import sys

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class RealTimePlot(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Real-Time Plot with PyQt')
        self.setGeometry(100, 100, 800, 600)

        # Create the main widget and layout
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Create a Matplotlib figure and canvas
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Initialize data for the plot
        self.x_data = np.arange(0, 10, 0.1)
        self.y_data = np.sin(self.x_data)

        # Plot the initial data
        self.line, = self.ax.plot(self.x_data, self.y_data)

        # Set up the animation
        self.animation = FuncAnimation(self.figure, self.update_plot, interval=100)

    def update_plot(self, frame):
        # Update the data for the plot
        self.x_data += 0.1
        self.y_data = np.sin(self.x_data)

        # Update the plot with the new data
        self.line.set_xdata(self.x_data)
        self.line.set_ydata(self.y_data)

        # Adjust the x-axis limits for scrolling effect
        self.ax.set_xlim(self.x_data.min(), self.x_data.max() + 1)

        # Redraw the plot
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = RealTimePlot()
    mainWindow.show()
    sys.exit(app.exec_())
