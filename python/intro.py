"""
File: intro.py
Author: Chuncheng Zhang
Date: 2024-05-21
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Amazing things

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2024-05-21 ------------------------
# Requirements and constants
import time
import random
import numpy as np
import gradio as gr

from PIL import Image
from threading import Thread

from psychopy import visual, core, event
from psychopy.hardware import keyboard

from util import logger


# %% ---- 2024-05-21 ------------------------
# Function and class
def random_color():
    rgb = [random.randint(0, 256) for _ in range(3)]
    return '#' + ''.join(hex(e).replace('x', '')[-2:] for e in rgb)


class MainWindow(object):
    # Options
    size = [800, 600]
    d_phase = 0.05

    # create a window
    win = visual.Window(
        size, monitor="testMonitor", units="deg")

    # create some stimuli
    msg = visual.TextStim(
        win, text=u"\u00A1Hola mundo!", pos=[0, -3])

    grating = visual.GratingStim(
        win=win, mask='circle', size=3, pos=[-4, 0], sf=3, color='white')

    fixation = visual.GratingStim(
        win=win, size=0.2, pos=[0, 0], sf=0, color='red')

    # Variables
    screenshot_img = None
    screenshot_countdown = False

    def __init__(self):
        for e in [self.msg, self.grating, self.fixation]:
            e.autoDraw = True
            logger.info(f'Auto drawing {e}')

    def change_position(self, pos):
        self.grating.pos = pos
        logger.debug(f'Changed grating position {pos}')

    def update_frame(self):
        self.msg.text = f'Phase: {self.d_phase:.2f}'
        self.advance_phase()

        self.win.flip()

        if self.screenshot_countdown > 0:
            self.screenshot_countdown -= 1
            if self.screenshot_countdown == 1:
                self.screenshot()

    def advance_phase(self):
        d_phase = self.d_phase
        # Example: grating.setPhase(0.05, '+')  # advance phase by 0.05 of a cycle
        self.grating.setPhase(d_phase, '+')

    def increase_d_phase(self):
        self.d_phase += 0.01
        logger.debug(f'Changed d_phase: {self.d_phase:.2f}')

    def decrease_d_phase(self):
        self.d_phase -= 0.01
        logger.debug(f'Changed d_phase: {self.d_phase:.2f}')

    def change_color(self):
        color = random_color()
        self.fixation.color = color
        logger.debug(f'Changed color: {color}')
        print(self.screenshot())

    def screenshot(self):
        # ! It only works in THIS class.
        img = self.win.screenshot
        self.screenshot_img = img
        return img


class Controller(object):
    kb = keyboard.Keyboard()
    keys = []

    def __init__(self):
        pass

    def update_frame(self):
        self.keys = self.kb.getKeys()
        event.clearEvents()
        for key in self.keys:
            logger.debug(f'Key pressed: {key.name}')

    def check_key(self, name=None):
        return any(key == name for key in self.keys)


# %% ---- 2024-05-21 ------------------------
# Play ground
main_window = MainWindow()
controller = Controller()

# --------------------


class GradioEventHandler:
    def slider_d_phase(self, value):
        main_window.d_phase = value
        return self.summary_output()

    def slider_sf(self, value):
        main_window.grating.sf = value
        return self.summary_output()

    def slider_ori(self, value):
        main_window.grating.ori = value
        return self.summary_output()

    def colorPicker_grating(self, value):
        main_window.grating.color = value
        return self.summary_output()

    def summary_output(self):
        main_window.screenshot_countdown = 5
        while main_window.screenshot_countdown > 0:
            time.sleep(0.001)
        return main_window.screenshot_img

    def image_screenshot_onclick(self, img, evt: gr.SelectData):
        x = evt.index[0]
        y = evt.index[1]
        width, height = main_window.size
        deg_x = (x - width / 2) / (width/2) * 12
        deg_y = - (y - height / 2) / (height/2) * 12 * (height / width)
        main_window.grating.pos = [deg_x, deg_y]
        return self.summary_output()


event_handler = GradioEventHandler()

with gr.Blocks() as demo:
    # --------------------
    # Layout
    slider_d_phase = gr.Slider(
        label='d_phase', minimum=-0.2, maximum=0.2, value=main_window.d_phase)

    slider_sf = gr.Slider(
        label='sf', minimum=1.0, maximum=5.0, value=main_window.grating.sf[0])

    slider_ori = gr.Slider(
        label='ori', minimum=0, maximum=360, value=main_window.grating.ori)

    colorPicker_grating = gr.ColorPicker(value=main_window.grating.color)

    image_screenshot = gr.Image(label='screenshot', value=None)

    txt = gr.Textbox('textbox')

    # --------------------
    # Handlers
    image_screenshot.select(
        fn=event_handler.image_screenshot_onclick, inputs=[image_screenshot], outputs=[image_screenshot])

    slider_d_phase.change(
        fn=event_handler.slider_d_phase, inputs=[slider_d_phase], outputs=[image_screenshot])

    slider_sf.change(
        fn=event_handler.slider_sf, inputs=[slider_sf], outputs=[image_screenshot])

    slider_ori.change(
        fn=event_handler.slider_ori, inputs=[slider_ori], outputs=[image_screenshot])

    colorPicker_grating.change(
        fn=event_handler.colorPicker_grating, inputs=[colorPicker_grating], outputs=[image_screenshot])


Thread(target=demo.launch, kwargs=dict(), daemon=True).start()

# --------------------
# Display loop
# Draw the stimuli and update the window
while True:  # this creates a never-ending loop
    main_window.update_frame()

    controller.update_frame()

    # if controller.check_key('space'):
    #     main_window.change_color()

    # if controller.check_key('left'):
    #     main_window.change_position([-4, 0])

    # if controller.check_key('right'):
    #     main_window.change_position([4, 0])

    # if controller.check_key('up'):
    #     main_window.increase_d_phase()

    # if controller.check_key('down'):
    #     main_window.decrease_d_phase()

    if controller.check_key('escape'):
        break

# cleanup
main_window.win.close()
core.quit()

# %% ---- 2024-05-21 ------------------------
# Pending


# %% ---- 2024-05-21 ------------------------
# Pending
