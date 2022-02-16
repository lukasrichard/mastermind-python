from random import randrange

from tkinter import BOTH, S, X
from tkinter import Canvas, Label, LabelFrame, PhotoImage
from tkinter.ttk import Button

from preferences import ALL_COLORS, SETTINGS


class GameArea(LabelFrame):

    EXTERNAL_OFFSET = 30
    OFFSET_X = 20
    OFFSET_Y = 20
    DIAMETER = 20
    SMALL_DIAMETER = 10

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.secret_code = None
        self.main_cv = None
        self.new_game_button = None
        self.active_row = 0
        self.selected_color = None
        self.victory_image = None
        self.failure_image = None
        self.new_game()

    def new_game(self):
        if self.main_cv is not None:
            self.main_cv.destroy()
        if self.new_game_button is not None:
            self.new_game_button.destroy()
        self.active_row = 0
        self.generate_fields()
        self.secret_code = self.make_secret()
        self.set_gameplay()

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


def set_gameplay(self):

        def interpret_click(event):
            selected_item = self.main_cv.find_closest(event.x, event.y)
            try:
                selected_tag, _ = self.main_cv.gettags(selected_item)
            except ValueError:
                return

            # The tags of the pickable colors are of the form "<color>_choice":
            if 'choice' in selected_tag:
                self.selected_color = selected_tag.split('_')[0]

            # The tags of the settable slots are of the form "<row_index>_<column_index>_guess":
            elif 'guess' in selected_tag:
                selected_row = int(selected_tag.split('_')[0])
                if selected_row == self.active_row and self.selected_color is not None:
                    self.main_cv.itemconfig(selected_item, fill=self.selected_color)
                    # Detect if the row is fully filled:
                    all_row_items = [self.main_cv.find_withtag('_'.join([str(selected_row), str(j), 'guess']))
                                     for j in range(SETTINGS['code_size'])]
                    all_row_colors = [self.main_cv.itemcget(item, 'fill') for item in all_row_items]
                    if 'white' not in all_row_colors:
                        all_scores = self.compute_scores(all_row_colors)
                        self.draw_scores(*all_scores)
                        self.active_row += 1
                        if all_scores[0] == SETTINGS['code_size']:
                            self.make_victory()
                        elif self.active_row == SETTINGS['n_tries']:
                            self.make_failure()

        self.main_cv.bind('<Button-1>', interpret_click)
@staticmethod
def make_secret():
        return [ALL_COLORS[randrange(0, SETTINGS['n_colors'])] for _ in range(SETTINGS['code_size'])]