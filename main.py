import sys
import numpy as np
import tensorflow as tf 
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import tensorflow as tf 

def model_forecast(model, series, window_size, batch_size):
    """Uses an input model to generate predictions on data windows

    Args:
      model (TF Keras Model) - model that accepts data windows
      series (array of float) - contains the values of the time series
      window_size (int) - the number of time steps to include in the window
      batch_size (int) - the batch size

    Returns:
      forecast (numpy array) - array containing predictions
    """

    # Generate a TF Dataset from the series values
    dataset = tf.data.Dataset.from_tensor_slices(series)

    # Window the data but only take those with the specified size
    dataset = dataset.window(window_size, shift=1, drop_remainder=True)

    # Flatten the windows by putting its elements in a single batch
    dataset = dataset.flat_map(lambda w: w.batch(window_size))
    
    # Create batches of windows
    dataset = dataset.batch(batch_size).prefetch(1)
    
    # Get predictions on the entire dataset
    forecast = model.predict(dataset)
    
    return forecast

class RealTimePlot(QMainWindow):
    def __init__(self):
        super().__init__()

        # Init
        self.window_size = 20
        self.batch_size = 32
        self.model = tf.keras.models.load_model("notebooks/model_lstm")


        self.setWindowTitle('Real-Time Plot')
        self.setGeometry(100, 100, 1000, 600)

        # Create the main widget and layout
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Create a Matplotlib figure and canvas
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Initialize data for the plot
        self.step = 0.01
        self.end_time = 100
        self.timesteps = int(self.end_time/self.step)
        self.x_data = np.arange(0, self.end_time, self.step)
        self.y_data = np.sin(self.x_data) + np.random.normal(0,0.2,self.timesteps)
        self.forecast = [0] * len(self.y_data)

        # Plot the initial data
        self.line, = self.ax.plot(self.x_data, self.y_data, label='real')
        self.line_forecast, = self.ax.plot(self.x_data, self.forecast,label = 'predict')
        self.ax.legend(loc='upper right')

        # Set up the animation
        self.animation = FuncAnimation(self.figure, self.update_plot, interval=1)

    def update_plot(self, frame):
        # Update the data for the plot
        self.x_data += 0.1
        self.forecast = model_forecast(self.model, self.y_data, self.window_size, self.batch_size)
        L = len(self.forecast)
        self.y_data = np.sin(self.x_data) + np.random.normal(0,0.2,self.timesteps)

        # Update the plot with the new data
        self.line.set_xdata(self.x_data[:L])
        self.line.set_ydata(self.y_data[:L])
        self.line_forecast.set_xdata(self.x_data[:L])
        self.line_forecast.set_ydata(np.squeeze(self.forecast))

        # Adjust the x-axis limits for scrolling effect
        self.ax.set_xlim(self.x_data.min(), self.x_data.max() + 1)

        # Redraw the plot
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = RealTimePlot()
    mainWindow.show()
    sys.exit(app.exec_())
