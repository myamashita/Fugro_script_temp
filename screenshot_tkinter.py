import tkinter as tk
from tkinter import ttk
import win32gui
import win32ui
import win32con
import win32api

class ScreenshotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Screenshot App")

        # Create a sample UI
        self.label = ttk.Label(root, text="This is a label")
        self.label.pack(pady=10)

        self.button = ttk.Button(root, text="Take Screenshot", command=self.take_screenshot)
        self.button.pack(pady=10)

        self.message = tk.StringVar()
        self.message.set("Ready")
        self.status = ttk.Label(root, textvariable=self.message)
        self.status.pack(pady=10)

    def take_screenshot(self):
        # Get the position and size of the root window
        x = self.root.winfo_rootx()
        y = self.root.winfo_rooty()
        width = self.root.winfo_width()
        height = self.root.winfo_height()

        # Capture the image from the specified region using win32 APIs
        hwin = win32gui.GetDesktopWindow()
        hwindc = win32gui.GetWindowDC(hwin)
        srcdc = win32ui.CreateDCFromHandle(hwindc)
        memdc = srcdc.CreateCompatibleDC()
        bmp = win32ui.CreateBitmap()
        bmp.CreateCompatibleBitmap(srcdc, width, height)
        memdc.SelectObject(bmp)
        memdc.BitBlt((0, 0), (width, height), srcdc, (x, y), win32con.SRCCOPY)
        bmp.SaveBitmapFile(memdc, 'screenshot.bmp')

        # Clean up
        memdc.DeleteDC()
        win32gui.DeleteObject(bmp.GetHandle())

        # Update the message to indicate that the screenshot has been taken
        self.message.set("Screenshot taken and saved as screenshot.bmp")

# Create the main window
root = tk.Tk()
app = ScreenshotApp(root)
root.mainloop()
