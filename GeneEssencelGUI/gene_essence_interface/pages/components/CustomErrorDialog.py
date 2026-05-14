import os
from tkinter import Toplevel, Label, Frame
from PIL import Image, ImageTk
from gene_essence_interface.utils.resource_path import resource_path
from gene_essence_interface.pages.components.CustomButton import CustomButton


class CustomErrorDialog(Toplevel):
    """
    Custom error dialog with white background, black text, and centered logo.
    Opens as a smaller dialog within the parent window context.
    """

    def __init__(self, parent, title, message):
        super().__init__(parent)

        self.withdraw()

        self.title(title)
        self.configure(bg='#FFFFFF')
        self.resizable(False, False)

        self.transient(parent)

        width = 400
        height = 300

        self.update_idletasks()

        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()

        x = parent_x + (parent_width // 2) - (width // 2)
        y = parent_y + (parent_height // 2) - (height // 2)

        self.geometry(f'{width}x{height}+{x}+{y}')

        main_frame = Frame(self, bg='#FFFFFF')
        main_frame.pack(fill='both', expand=True, padx=15, pady=15)

        self.create_logo(main_frame)

        title_label = Label(
            main_frame,
            text=title,
            font=(os.getenv('FONT_PRIMARY', 'Arial'), 13, 'bold'),
            fg='#000000',
            bg='#FFFFFF'
        )
        title_label.pack(pady=(5, 8))

        message_label = Label(
            main_frame,
            text=message,
            font=(os.getenv('FONT_PRIMARY', 'Arial'), 10),
            fg='#000000',
            bg='#FFFFFF',
            wraplength=350,
            justify='left'
        )
        message_label.pack(pady=(0, 15))

        button_frame = Frame(main_frame, bg='#FFFFFF')
        button_frame.pack(side='bottom', pady=(5, 0))

        ok_button = CustomButton(
            button_frame,
            text="OK",
            font_size=11,
            command=self.destroy,
            width=80
        )
        ok_button.pack()

        self.deiconify()

        self.grab_set()

        self.focus_set()

        self.wait_window()

    def create_logo(self, parent):
        """Create and display the centered logo."""
        try:
            logo_path = resource_path('assets/gene_essence_logo.png')

            if os.path.exists(logo_path):
                logo_image = Image.open(logo_path)

                max_width = 60
                aspect_ratio = logo_image.height / logo_image.width
                new_width = min(max_width, logo_image.width)
                new_height = int(new_width * aspect_ratio)

                logo_image = logo_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                logo_photo = ImageTk.PhotoImage(logo_image)

                logo_label = Label(parent, image=logo_photo, bg='#FFFFFF')
                logo_label.image = logo_photo
                logo_label.pack(pady=(0, 10))
        except Exception as e:
            print(f"Could not load logo: {e}")


def show_error_dialog(parent, title, message):
    """
    Show a custom error dialog.

    Args:
        parent: Parent widget
        title: Dialog title
        message: Error message to display
    """
    CustomErrorDialog(parent, title, message)