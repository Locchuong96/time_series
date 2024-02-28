import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvas

class RealTimePlot(QMainWindow):
    def __init__(self):
        
        super().__init__()
        
        # Set Title
        self.setWindowTitle('Real-Time Plot')
        
        # Set Geometry
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
        self.time_step = 100
        self.x_data = np.arange(0,self.time_step,1)
        self.y_data = [np.random.randint(0, 10) for i in range(self.time_step)] 
        
        # Plot the initial data
        self.line, = self.ax.plot(self.x_data, self.y_data)
        
        # Set up the animation
        self.interval = 200
        self.animation = FuncAnimation(self.figure, self.update_plot, interval=self.interval)

    def update_plot(self,frame):
        
        # Update the x data for the plot
        self.time_step +=1
        self.x_data = np.delete(self.x_data, 0)
        self.x_data = np.append(self.x_data, self.time_step)
        
        # Update the y data for the plot
        self.y_data.pop(0)
        self.y_data.append(np.random.randint(0, 10))
        
        # Update the plot with new data
        self.line.set_xdata(self.x_data)
        self.line.set_ydata(self.y_data)
        
        # Adjust the x-axis limits for scrolling effect
        self.ax.set_xlim(self.x_data.min(), self.x_data.max() +1)
        # Adjust the y-axis limits for scrolling effect
        self.ax.set_ylim(min(self.y_data), max(self.y_data) +1)
        
        # Redraw the plot
        self.canvas.draw()

        
if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    mainWindow = RealTimePlot()
    mainWindow.show()
    sys.exit(app.exec_())