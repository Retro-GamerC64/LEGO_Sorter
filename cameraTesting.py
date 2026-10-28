import requests
import os
import json
import heapq
import time
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import colorDetect as Color
import PartCategorize as PC
from pathlib import Path
from cv2 import *
import cv2
import threading

class camera:
    def __init__(self):
        # Open the default camera
        self.cam = cv2.VideoCapture(0)

        # Get the default frame width and height
        frame_width = int(self.cam.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.lock = threading.Lock()
        self.latestFrame = None
        self.stopped = threading.Event()

        self.displayThread = threading.Thread(
            target=self.displayLoop,
            daemon=True,
        )
    def displayLoop(self):
        while not self.stopped.is_set():
            success, frame = self.cam.read()
            if not success or frame is None:
                time.sleep(0.01)
                continue
            with self.lock:
                self.latestFrame = frame.copy()

            cv2.imshow("Camera", frame)
            cv2.waitKey(1)
        cv2.destroyWindow("Camera")

    def grabImage(self):
        with self.lock:
            if self.latestFrame is None:
                raise RuntimeError("No camera frame is available yet.")
            frame = self.latestFrame.copy()

        return Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)) 
    
    def close(self):
        self.stopped.set()
        self.displayThread.join()
        self.cam.release()