import platform
from multiprocessing import freeze_support
from tkinter import *

from gene_essence_interface.database import initialize_database
from gene_essence_interface.pages.PageManager import PageManager
from gene_essence_interface.utils import resource_path


class GeneEssenceGUI(Tk):
    def __init__(self):
        super().__init__()
        self.withdraw()
        self.title('GeneEssenceGUI')

        window_height = 680
        window_width = 1000

        self.update_idletasks()
        # wm_maxsize retorna a área útil real descontando barra de menus / barra de tarefas
        usable_width, usable_height = self.wm_maxsize()
        x_position = (usable_width - window_width) // 2
        y_position = (usable_height - window_height) // 2

        self.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        self.resizable(False, False)

        try:
            icon = PhotoImage(file=resource_path("assets/genne_essence.png"))
            self.iconphoto(False, icon)
        except Exception as e:
            print(f"Error loading icon: {e}")

        initialize_database()

        self.page_manager = PageManager(self)
        self.page_manager.pack(fill=BOTH, expand=True)
        self.deiconify()


if __name__ == "__main__":
    freeze_support()
    app = GeneEssenceGUI()
    app.mainloop()