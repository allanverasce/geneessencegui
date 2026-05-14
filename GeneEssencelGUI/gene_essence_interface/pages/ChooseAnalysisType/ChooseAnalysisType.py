from tkinter import *

from gene_essence_interface.config.colors import COLORS
from gene_essence_interface.pages.components.CardOption import CardOption
from gene_essence_interface.pages.components.CustomButton import CustomButton
from gene_essence_interface.pages.components.NavigationSidebar import NavigationSidebar, STEPS_BY_TYPE, STEP_INDEX_BY_TYPE

_OPTIONS = {
    "Training": "Teach a model to identify essential genes from labeled genetic data. "
                "The algorithm learns patterns and relationships during this phase.",
    "Prediction": "Apply a previously trained model to new, unlabeled data. "
                  "Classify unknown genes using knowledge from the training phase.",
    "Ensemble": "Combine multiple classifiers to boost accuracy and reduce overfitting. "
                "Aggregates predictions from several models for a more robust result.",
}


class ChooseAnalysisType(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLORS['background_alt'])
        self.controller = controller
        self.radio_var = StringVar(value="Training")

        self._sidebar = NavigationSidebar(self)
        self._sidebar.pack(side=LEFT, fill=Y)
        self._sidebar.set_active_step(0)
        self.radio_var.trace_add('write', self._update_sidebar)

        content = Frame(self, bg=COLORS['background_alt'])
        content.pack(side=RIGHT, fill=BOTH, expand=True)

        # Bottom button row (packed first so it sticks to bottom)
        btn_frame = Frame(content, bg=COLORS['background_alt'])
        btn_frame.pack(side=BOTTOM, fill=X, padx=20, pady=12)
        Frame(content, bg=COLORS['border'], height=1).pack(side=BOTTOM, fill=X)

        CustomButton(btn_frame, text='NEXT →', variant='primary',
                     command=self._proceed).pack(side=RIGHT)
        CustomButton(btn_frame, text='← BACK', variant='secondary',
                     command=lambda: self.controller.show_page('StartPage')).pack(side=RIGHT, padx=(0, 8))

        # Title
        title_area = Frame(content, bg=COLORS['background_alt'])
        title_area.pack(fill=X, padx=20, pady=(20, 0))
        Label(title_area, text='Select the type of analysis',
              bg=COLORS['background_alt'], fg=COLORS['text'],
              font=('Arial', 16, 'bold')).pack(anchor=W)


        # Cards
        cards_area = Frame(content, bg=COLORS['background_alt'])
        cards_area.pack(fill=BOTH, expand=True, padx=20, pady=14)

        for title, desc in _OPTIONS.items():
            CardOption(cards_area, title=title, description=desc,
                       value=title, variable=self.radio_var,
                       ).pack(fill=X, pady=5)

    def _update_sidebar(self, *_):
        t = self.radio_var.get()
        self._sidebar.reset_steps(STEPS_BY_TYPE.get(t, STEPS_BY_TYPE['Training']))
        self._sidebar.set_active_step(STEP_INDEX_BY_TYPE.get(t, STEP_INDEX_BY_TYPE['Training'])['ChooseAnalysisType'])

    def on_show(self):
        self._update_sidebar()

    def _proceed(self):
        self.controller.set_analyse_type(self.radio_var.get())
        self.controller.show_page('InformationProject')