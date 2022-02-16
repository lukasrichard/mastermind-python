from tkinter import Tk
from tkinter import BOTH, N, S, X
from tkinter import Label, Menu
from tkinter.ttk import Button
from tkinter.messagebox import showinfo

from game_area import GameArea
from preferences import SettingsWindow


def about():
    """
    Display an informative window.
    """
    showinfo('À propos',
             message="Bienvenue dans cette demo de Mastermind avec Tkinter.\n\n"
                     "Ce jeu consiste à trouver un code secret composé de plusieurs couleurs, sachant que "
                     "chaque couleur peut apparaître plusieurs fois.\n\n"
                     "Vous pouvez configurer le nombre de couleurs différentes, la taille du code secret "
                     "et le nombre de tentatives que vous pouvez effectuer dans le menu Préférences.")


# Instantiate the global window:
root = Tk()
root.title('Mastermind')
root.resizable(True, True)


# Create canvas in which to draw the pickable pegs, the playing field and the guess results:
Label(root,
      text='[F1] À propos - [F2] Préférences - [F5] Nouvelle partie - [ESC] Quitter',
      foreground="white",
      background="blue").pack(anchor=N, fill=X)


# Create the game area:
game_area = GameArea(text="Aire de jeu")
game_area.pack(anchor=N, expand=True, fill=BOTH)


# Create and populate the main menu:
root_menu = Menu(root)
root['menu'] = root_menu
main_cascade = Menu(root_menu)
root_menu.add_cascade(label='Mastermind', menu=main_cascade)
main_cascade.add_command(label='Préférences', command=lambda: SettingsWindow(game_area))
main_cascade.add_separator()
main_cascade.add_command(label='À propos', command=about)


# Menu shortcuts:
root.bind("<F1>", lambda _event: about())
root.bind("<F2>", lambda _event: SettingsWindow(game_area))


# Add a last button for quitting the game:
Button(text='Quitter [ESC]', command=root.destroy).pack(anchor=S, fill=X)
root.bind('<Escape>', lambda _event: root.destroy())


# Launch the main loop that catches all user interactions:
root.mainloop()

def generate_fields(self):
        n_colors = SETTINGS['n_colors']
        code_size = SETTINGS['code_size']
        n_tries = SETTINGS['n_tries']
        colors = ALL_COLORS[:n_colors]

        # Create the canvas in which the game takes place:
        self.main_cv = Canvas(self, bg="sienna", cursor="hand")
        self.main_cv.pack(expand=True, fill=BOTH)

        # Draw the field of choices, a white rectangle with the pegs of all colors that can be picked:
        band_width = self.OFFSET_X+self.DIAMETER
        self.main_cv.create_rectangle(self.EXTERNAL_OFFSET, self.EXTERNAL_OFFSET,
                                      self.EXTERNAL_OFFSET+self.OFFSET_X+band_width,
                                      self.EXTERNAL_OFFSET+self.OFFSET_Y+n_colors*(self.DIAMETER+self.OFFSET_Y),
                                      fill="white")
        offsets = (self.EXTERNAL_OFFSET+self.OFFSET_X, self.EXTERNAL_OFFSET+self.OFFSET_Y,
                   self.EXTERNAL_OFFSET+self.OFFSET_X+self.DIAMETER, self.EXTERNAL_OFFSET+self.OFFSET_Y+self.DIAMETER)
        for color in colors:
            self.main_cv.create_oval(*offsets, fill=color, tags=color+'_choice')
            offsets = (offsets[0], offsets[1]+self.OFFSET_Y+self.DIAMETER,
                       offsets[2], offsets[3]+self.OFFSET_Y+self.DIAMETER)

        # Draw the field of guesses, a white rectangle with initially empty (white) slots:
        left_offset = 2*self.EXTERNAL_OFFSET + band_width + self.OFFSET_X
        self.main_cv.create_rectangle(left_offset, self.EXTERNAL_OFFSET,
                                      left_offset+code_size*band_width+self.OFFSET_X,
                                      self.EXTERNAL_OFFSET+self.OFFSET_Y+n_tries*(self.DIAMETER+self.OFFSET_Y),
                                      fill="white")
        for j in range(code_size):
            offsets = (left_offset + self.OFFSET_X + j*(self.DIAMETER+self.OFFSET_X),
                       self.EXTERNAL_OFFSET + self.OFFSET_Y,
                       left_offset + (j+1)*(self.DIAMETER+self.OFFSET_X),
                       self.EXTERNAL_OFFSET + self.OFFSET_Y + self.DIAMETER)
            for i in range(n_tries):
                self.main_cv.create_oval(*offsets, fill='white', tags='_'.join([str(i), str(j), 'guess']))
                offsets = (offsets[0], offsets[1] + self.OFFSET_Y + self.DIAMETER, offsets[2],
                           offsets[3] + self.OFFSET_Y + self.DIAMETER)

        # Restart:
        self.new_game_button = Button(self, text='Nouvelle partie [F5]', command=self.new_game)
        self.new_game_button.pack(anchor=S, fill=X)
        self.master.bind("<F5>", lambda _x: self.new_game())
