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
import random
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
        win=win, mask='circle', size=3, pos=[-4, 0], sf=3)
    fixation = visual.GratingStim(
        win=win, size=0.2, pos=[0, 0], sf=0, color='red')

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

    def advance_phase(self):
        d_phase = self.d_phase
        # Example: grating.setPhase(0.05, '+')  # advance phase by 0.05 of a cycle
        self.grating.setPhase(d_phase, '+')

    def increase_d_phase(self):
        self.d_phase += 0.01
        logger.debug(f'Changed d_phase: {self.d_phase}')

    def decrease_d_phase(self):
        self.d_phase -= 0.01
        logger.debug(f'Changed d_phase: {self.d_phase}')

    def change_color(self):
        color = random_color()
        self.fixation.color = color
        logger.debug(f'Changed color: {color}')


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

# create a keyboard component
# kb = keyboard.Keyboard()

# draw the stimuli and update the window
while True:  # this creates a never-ending loop
    main_window.update_frame()
    main_window.win.flip()

    controller.update_frame()

    if controller.check_key('space'):
        main_window.change_color()

    if controller.check_key('left'):
        main_window.change_position([-4, 0])

    if controller.check_key('right'):
        main_window.change_position([4, 0])

    if controller.check_key('up'):
        main_window.increase_d_phase()

    if controller.check_key('down'):
        main_window.decrease_d_phase()

    if controller.check_key('escape'):
        break

    # keys = kb.getKeys()
    # if len(keys) > 0:
    #     for key in keys:
    #         print(key.name)

    #     if any(key == 'space' for key in keys):
    #         main_window.change_color()

    #     if any(key == 'left' for key in keys):
    #         main_window.change_position([-4, 0])

    #     if any(key == 'right' for key in keys):
    #         main_window.change_position([4, 0])

    #     if any(key == 'up' for key in keys):
    #         main_window.increase_d_phase()

    #     if any(key == 'down' for key in keys):
    #         main_window.decrease_d_phase()

    #     if any(key == 'escape' for key in keys):
    #         break

    # event.clearEvents()

# cleanup
main_window.win.close()
core.quit()

# %% ---- 2024-05-21 ------------------------
# Pending


# %% ---- 2024-05-21 ------------------------
# Pending
