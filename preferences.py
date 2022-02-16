from tkinter import Button, IntVar, Label, Radiobutton, Spinbox, Toplevel
from tkinter.ttk import Combobox


ALL_COLORS = ['red', 'blue', 'yellow', 'black', 'green', 'purple', 'orange', 'cyan']


SETTINGS = {
    'n_colors': 4,
    'n_tries': 8,
    'code_size': 4
}


class SettingsWindow(Toplevel):

    def __init__(self, game_area):
        super().__init__()
        self.bg_color = 'wheat'
        self.config(bg=self.bg_color)
        self.title("Préférences")
        self.resizable(False, False)
        self.game_area = game_area

        paddings = {'padx': (12, 12), 'pady': (12, 12)}

        Label(self, text="Nombre de couleurs en jeu :", bg=self.bg_color) \
            .grid(row=0, column=0, columnspan=2, sticky='nws', **paddings)
        self.n_colors_box = Spinbox(self, from_=4, to=8)
        self.n_colors_box.grid(row=0, column=2, columnspan=2, sticky='nes', **paddings)

        Label(self, text="Nombre maximum d'essais :", bg=self.bg_color) \
            .grid(row=1, column=0, sticky='nws', **paddings)
        self.n_tries_box = Combobox(self, values=[8, 10, 12, 14])
        self.n_tries_box.grid(row=1, column=2, columnspan=2, sticky='nes', **paddings)
        self.n_tries_box.current(0)

        Label(self, text="Taille du code à trouver :", bg=self.bg_color) \
            .grid(row=2, column=0, columnspan=2, sticky='nws', **paddings)
        self.code_size_var = IntVar(value=SETTINGS['code_size'])
        Radiobutton(self, text="Facile (4)", variable=self.code_size_var, value=4, bg=self.bg_color) \
            .grid(row=2, column=1, **paddings)
        Radiobutton(self, text="Moyen (6)", variable=self.code_size_var, value=6, bg=self.bg_color) \
            .grid(row=2, column=2, **paddings)
        Radiobutton(self, text="Difficile (8)", variable=self.code_size_var, value=8, bg=self.bg_color) \
            .grid(row=2, column=3, **paddings)

        Button(self, text="Annuler", command=self.destroy, bg=self.bg_color) \
            .grid(row=3, column=0, columnspan=2, sticky='nesw', **paddings)
        Button(self, text="Appliquer", command=self.apply, bg=self.bg_color) \
            .grid(row=3, column=2, columnspan=2, sticky='nesw', **paddings)

        self.bind("<Escape>", lambda _event: self.destroy())

    def apply(self):
        global SETTINGS
        SETTINGS['n_colors'] = int(self.n_colors_box.get())
        SETTINGS['n_tries'] = int(self.n_tries_box.get())
        SETTINGS['code_size'] = int(self.code_size_var.get())
        self.game_area.new_game()
        self.destroy()