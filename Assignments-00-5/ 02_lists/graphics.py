"""Simple graphics library for the eraser assignment."""

import tkinter as tk
from tkinter import messagebox
import time
import sys

class Canvas:
    def __init__(self, width, height):
        self.root = tk.Tk()
        self.root.title("Canvas")
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
        self.canvas = tk.Canvas(self.root, width=width, height=height, bg="white")
        self.canvas.pack()
        self.width = width
        self.height = height
        self.objects = {}
        self.object_id = 0
        self.mouse_x = 0
        self.mouse_y = 0
        self.last_click_x = 0
        self.last_click_y = 0
        self.clicked = False
        
        self.canvas.bind("<Motion>", self._update_mouse_pos)
        self.canvas.bind("<Button-1>", self._handle_click)
        self.root.update()
        
    def _on_closing(self):
        self.root.destroy()
        sys.exit(0)
        
    def _update_mouse_pos(self, event):
        self.mouse_x = event.x
        self.mouse_y = event.y
        
    def _handle_click(self, event):
        self.last_click_x = event.x
        self.last_click_y = event.y
        self.clicked = True
    
    def create_rectangle(self, x1, y1, x2, y2, color):
        obj_id = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")
        self.object_id += 1
        self.objects[self.object_id] = obj_id
        self.root.update()
        return self.object_id
    
    def set_color(self, object_id, color):
        if object_id in self.objects:
            tk_id = self.objects[object_id]
            self.canvas.itemconfig(tk_id, fill=color)
        self.root.update()
    
    def find_overlapping(self, x1, y1, x2, y2):
        # Check if the canvas still exists
        try:
            tk_ids = self.canvas.find_overlapping(x1, y1, x2, y2)
            result = []
            for object_id, tk_id in self.objects.items():
                if tk_id in tk_ids:
                    result.append(object_id)
            return result
        except tk.TclError:
            # Canvas was closed
            sys.exit(0)
    
    def get_mouse_x(self):
        self.root.update()
        return self.mouse_x
    
    def get_mouse_y(self):
        self.root.update()
        return self.mouse_y
    
    def get_last_click(self):
        self.root.update()
        return (self.last_click_x, self.last_click_y)
    
    def wait_for_click(self):
        self.clicked = False
        # Show a message box to instruct the user
        self.root.update()
        messagebox.showinfo("Canvas", "Click anywhere on the canvas to start erasing.")
        # Wait for the user to click
        while not self.clicked:
            self.root.update()
            time.sleep(0.05)
    
    def moveto(self, object_id, x, y):
        try:
            if object_id in self.objects:
                tk_id = self.objects[object_id]
                coords = self.canvas.coords(tk_id)
                if len(coords) == 4:  # Rectangle
                    width = coords[2] - coords[0]
                    height = coords[3] - coords[1]
                    self.canvas.coords(tk_id, x, y, x + width, y + height)
            self.root.update()
        except tk.TclError:
            # Canvas was closed
            sys.exit(0) 