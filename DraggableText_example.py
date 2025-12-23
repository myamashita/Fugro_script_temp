import matplotlib.pyplot as plt
import numpy as np


class DraggableText:
    def __init__(self, text):
        self.text = text
        self.press = None
        self.text.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.text.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.text.figure.canvas.mpl_connect('button_release_event', self.on_release)

    def on_press(self, event):
        if event.inaxes != self.text.axes: return
        contains, _ = self.text.contains(event)
        if not contains: return
        # Save the position and mouse click location
        self.press = (self.text.get_position(), event.xdata, event.ydata)

    def on_motion(self, event):
        if self.press is None: return
        if event.inaxes != self.text.axes: return
        # Calculate the offset and update text position
        position, xpress, ypress = self.press
        dx = event.xdata - xpress
        dy = event.ydata - ypress
        new_position = (position[0] + dx, position[1] + dy)
        self.text.set_position(new_position)
        self.text.figure.canvas.draw()

    def on_release(self, event):
        self.press = None
        self.text.figure.canvas.draw()



# Sample data
x, y = 0.5, 0.5
offset = 0.05
name = "Drag me!"


# Data for plotting
t = np.arange(0.0, 2.0, 0.01)
s = 1 + np.sin(2 * np.pi * t)

fig, ax = plt.subplots()
ax.plot(t, s)

ax.set(xlabel='time (s)', ylabel='voltage (mV)',
       title='About as simple as it gets, folks')
ax.grid()

# Adding text annotation to the plot
if name:
    text = ax.text(x + offset, y + offset, name, color='k', size=11,
                   bbox=dict(boxstyle="round", ec='#121212', fc='#fadede', alpha=0.7))
    draggable_text = DraggableText(text)  # Make the text draggable

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
plt.show()
