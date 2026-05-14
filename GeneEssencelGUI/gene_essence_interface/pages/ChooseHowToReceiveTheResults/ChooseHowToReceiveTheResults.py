from tkinter import *

from gene_essence_interface.config.colors import COLORS
from gene_essence_interface.pages.ChooseHowToReceiveTheResults.DeliveryOptionFrame import DeliveryOptionFrame
from gene_essence_interface.pages.components.NavigationSidebar import NavigationSidebar, STEPS_BY_TYPE, STEP_INDEX_BY_TYPE

BG = COLORS['background_alt']


class ChooseHowToReceiveTheResults(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller

        self._sidebar = NavigationSidebar(self)
        self._sidebar.pack(side=LEFT, fill=Y)
        self._sidebar.set_active_step(4)

        DeliveryOptionFrame(self, controller).pack(side=RIGHT, fill=BOTH, expand=True)

    def on_show(self):
        t = self.controller.get_analyse_type() or 'Training'
        self._sidebar.reset_steps(STEPS_BY_TYPE[t])
        self._sidebar.set_active_step(STEP_INDEX_BY_TYPE[t]['ChooseHowToReceiveTheResults'])