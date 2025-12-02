import numpy as np
from psychopy import visual, event, core

class PhotodiodeFlash:
    def __init__(self, stim, duration=0.05):
        """
        stim: Psychopy visual stimulus (e.g. Rect)
        duration: desired flash duration in seconds
        """
        self.stim = stim
        self.duration = duration
        self.off_time = None

    def trigger(self):
        """Call this when you want to start a flash."""
        now = core.getTime()
        self.off_time = now + self.duration
        self.stim.autoDraw = True  # will be drawn on the NEXT flip

    def update(self):
        """Call this once before a win.flip() whenever possible."""
        if self.off_time is None:
            return
        now = core.getTime()
        if now >= self.off_time:
            self.stim.autoDraw = False
            self.off_time = None