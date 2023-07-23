import threading
import time
import tkinter as tk
import tkinter.filedialog as fd
from enum import Enum

from bruteforce import BruteForceSolver
from preloadedpuzzles import PreloadedPuzzle
from csp import CSP

DEFAULT_DROP_OPTION = "Please choose a puzzle size..."

"""
First attempt at OOP/TKinter programming. Basing general structure off of an online tutorial on 
configuring a class that extends tk.TK
"""


class Gui(tk.Tk):

    def __init__(self, *args, **kwargs):
        """
        Initialize the instance of the GUI master window.
        This is the window that will hold the frames for the program.

        :param args: arguments needed to pass to the super
        :param kwargs: arguments needed to pass to the super
        """
        tk.Tk.__init__(self, *args, **kwargs)
        self.frame_dictionary = {}
        self.wm_title("Sudoku Solver")
        self.geometry("950x950")
        self.event = threading.Event()
        # This var represents the ROW x COL dimensions of the sudoku game
        self.menu_options = ["9x9", "12x12", "16x16", "25x25", "100x100"]
        self.game_size = None

        # Create the containers for the buttons, puzzle frames
        self.button_container = tk.Frame(self, height=200, width=1000)
        self.button_container.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.button_container.rowconfigure(0, weight=1)
        self.button_container.columnconfigure(0, weight=1)
        self.frame_container = tk.Frame(self, height=800, width=1000)
        self.frame_container.pack(fill=tk.BOTH, expand=True)  # packs parent container Frame into window
        self.frame_container.grid_rowconfigure(0, weight=1)
        self.frame_container.grid_columnconfigure(0, weight=1)

        # Create the navigation buttons
        self.brute_force_button = tk.Button(self.button_container,
                                            text=ButtonActions.BRUTE_FORCE.value,
                                            command=lambda: SudokuPage.replace_with_brute_force_solved(),
                                            border=10,
                                            state=tk.DISABLED,
                                            width=10)
        self.csp_button = tk.Button(self.button_container,
                                    text=ButtonActions.CSP.value,
                                    border=10,
                                    state=tk.DISABLED,
                                    width=10)
        self.clear_button = tk.Button(self.button_container,
                                      text=ButtonActions.CLEAR.value,
                                      border=10,
                                      state=tk.DISABLED,
                                      width=10)
        self.exit_button = tk.Button(self.button_container,
                                     text=ButtonActions.EXIT.value,
                                     command=lambda: exit(),
                                     border=10,
                                     width=10
                                     )

        # Place buttons along top row
        self.brute_force_button.pack(side="left", fill="x", expand=True, anchor=tk.N, pady=(25, 0))
        self.csp_button.pack(side="left", fill="x", expand=True, anchor=tk.N, pady=(25, 0))
        self.clear_button.pack(side="left", fill="x", expand=True, anchor=tk.N, pady=(25, 0))
        self.exit_button.pack(side="left", fill="x", expand=True, anchor=tk.N, pady=(25, 0))

        for frame in (WelcomePage, SudokuPage):
            f = frame(self.frame_container, self)
            self.frame_dictionary[frame] = f
            f.grid(row=0, column=0, sticky='nsew')

        self.switch_frame(WelcomePage)

    def switch_frame(self, page):
        """
        Switch the page from the Welcome page to Sudoku page and back.
        Disable the main buttons depending on which page is visible.

        :param page: a Frame Object
        :return: None
        """
        print(self.event)
        self.event.set()  # set event in case threads are still running
        print(self.event)
        time.sleep(1)  # allow time for thread to ping our event
        self.event.clear()  # rest event
        print(self.event)

        frame = self.frame_dictionary[page]  # Grab frame from dictionary
        frame.tkraise()  # change frame

        # enable/disable the master window buttons
        if page == SudokuPage:
            self.brute_force_button.config(state=tk.NORMAL)
            self.csp_button.config(state=tk.NORMAL)
            self.clear_button.config(state=tk.NORMAL)
            SudokuPage.puzzle_board = []
        else:
            self.brute_force_button.config(state=tk.DISABLED)
            self.csp_button.config(state=tk.DISABLED)
            self.clear_button.config(state=tk.DISABLED)

        # update instance of frame
        self.frame_dictionary[page].refresh(self)

    def placeholder(self):
        """
        placeholder function.

        :return: None
        """
        pass

    def clear_window(self):
        """
        Clears the window and returns to the main screen.
        Resets variables in the Sudoku Page.

        :return: None
        """
        print("Clearing window")
        self.frame_dictionary[SudokuPage].set_puzzle_board([])
        for widgets in self.frame_dictionary[SudokuPage].sudoku_frame.winfo_children():
            widgets.destroy()
        self.frame_dictionary[WelcomePage].load_from_file_button.config(text=ButtonActions.LOAD_FILE.value)
        self.frame_dictionary[WelcomePage].menu.set(DEFAULT_DROP_OPTION)
        self.frame_dictionary[WelcomePage].play_button.config(state=tk.DISABLED)
        self.frame_dictionary[WelcomePage].load_path_lbl.config(text="")
        self.frame_dictionary[SudokuPage].reset_button_pressed()
        self.frame_dictionary[SudokuPage].reset_time()
        self.frame_dictionary[SudokuPage].reset_successful()
        self.switch_frame(WelcomePage)

    def thread_runner(self, button_action):
        """
        Runs a new thread for certain processes.

        :param button_action: an Enum value
        :return: None
        """
        action_mapper = {
            ButtonActions.LOAD_FILE: self.load_from_file,
            ButtonActions.BRUTE_FORCE: self.placeholder,
            ButtonActions.CSP: self.placeholder,
            ButtonActions.CLEAR: self.clear_window
        }
        new_thread = threading.Thread(target=action_mapper[button_action])
        x = time.time()
        new_thread.start()
        y = time.time()
        print(y - x)

    def load_from_file(self):
        """
        Opens a new window to load a file

        :return:
        """
        if not self.event.is_set():
            print(self.event)
            self.event.set()
            path = fd.askopenfilename()
            input_puzzle = None
            if path != '':
                with open(path, mode='r', encoding='utf-8') as file:
                    data_input = file.read().splitlines()
                    input_puzzle = [list(map(int, line.split(","))) for line in data_input]
                    print(input_puzzle)
            # Validate puzzle size of input file
            size = len(input_puzzle)
            if f"{size}x{size}" not in self.menu_options:
                self.frame_dictionary[WelcomePage].file_loaded = False
                self.frame_dictionary[WelcomePage].update_selected_menu_option(DEFAULT_DROP_OPTION)
                self.frame_dictionary[WelcomePage].load_path_lbl.config(
                    text=f"File contains an invalid puzzle size."
                         f"\nChoose another file or select a size from the drop down for a preloaded puzzle")
            else:
                self.frame_dictionary[SudokuPage].set_puzzle_board(input_puzzle)
                self.frame_dictionary[WelcomePage].file_loaded = True
                self.frame_dictionary[WelcomePage].update_selected_menu_option(f"{size}x{size}")
                self.frame_dictionary[WelcomePage].load_path_lbl.config(text=path)
            time.sleep(1)  # allow time for thread to ping our event
            self.event.clear()  # reset event
            # Change to new frame once loaded

    def set_grid_size(self, size):
        """
        Sets the grid size to be used for the sudoku board.

        :param size: a String
        :return: None
        """
        self.game_size = size

    def get_grid_size(self):
        """
        Gets the grid size.

        :return: a String
        """
        return self.game_size

    def get_container(self):
        """
        Gets the frame containing the current frame.

        :return: A frame
        """
        return self.frame_container

    def del_from_frame_dictionary(self, frame_name):
        """
        Deletes a frame from the frame dictionary.

        :param frame_name: a String
        :return: None
        """
        del self.frame_dictionary[frame_name]

    def add_to_frame_dictionary(self, frame_name, frame_obj):
        """
        Adds a frame to the frame dictionary.

        :param frame_name: a String
        :param frame_obj: a Frame
        :return: None
        """
        self.frame_dictionary[frame_name] = frame_obj


class WelcomePage(tk.Frame):
    """
    Creates the Welcome Page for the GUI.
    """
    def __init__(self, parent_container, master_window):
        """
        Initializes the Welcome Page frame and its content.

        :param parent_container: a Frame Object
        :param master_window: a Frame Object, the topmost GUI window.
        """
        tk.Frame.__init__(self, parent_container)
        self.file_loaded = False
        self.menu = tk.StringVar()

        # Create the drop-down menu
        self.menu.set(DEFAULT_DROP_OPTION)
        self.drop = tk.OptionMenu(self, self.menu, *master_window.menu_options)

        # lock the option menu width so stuff doesn't shift around
        self.drop.config(width=23)

        # Create buttons
        self.play_button = tk.Button(self,
                                     text=ButtonActions.PLAY.value,
                                     command=lambda: [
                                         master_window.set_grid_size(self.menu.get()),
                                         master_window.switch_frame(SudokuPage)],
                                     border=10,
                                     state=tk.DISABLED
                                     )

        self.load_from_file_button = tk.Button(self,
                                               text=ButtonActions.LOAD_FILE.value,
                                               command=lambda: master_window.thread_runner(ButtonActions.LOAD_FILE),
                                               border=10
                                               )

        self.exit_button = tk.Button(self,
                                     text=ButtonActions.EXIT.value,
                                     command=lambda: exit(),
                                     border=10
                                     )

        # Set listener for Play button to update status once dropdown menu no longer set to default
        self.menu.trace('w', self.on_drop_change)

        # Populate frame with objects
        self.greeting_lbl = tk.Label(self, text="Welcome, User!", fg=Colours.BLUE.value, border=10)
        self.greeting_lbl.grid(row=0, column=1)
        self.greeting_lbl.grid_columnconfigure(1, weight=1)
        self.greeting_lbl.grid_rowconfigure(0, weight=1)
        self.greeting_lbl.config(font=('Arial Bold', 26))
        self.load_from_file_button.grid(row=3, column=0, padx=(245, 0), sticky="nswe")
        self.drop.grid(row=3, column=1, sticky="w")
        self.play_button.grid(row=3, column=2, sticky="nswe")
        self.load_path_lbl = tk.Label(self, text="")
        self.load_path_lbl.grid(row=4, column=0, columnspan=5, padx=(245, 0))

    def on_drop_change(self, *args):
        """
        Unlocks the play button and sets the label when the dropdown menu is selected.

        :param args: args passed through to the exterior frames.
        :return: None
        """
        if self.menu.get() != DEFAULT_DROP_OPTION:
            self.play_button.config(state=tk.NORMAL)
        else:
            self.play_button.config(state=tk.DISABLED)
        if not self.file_loaded:
            self.load_path_lbl.config(text="A preloaded puzzle will be used for the chosen size.")

    def update_selected_menu_option(self, option):
        """
        Sets the selected menu option.

        :param option: a String
        :return: None
        """
        self.menu.set(option)

    def refresh(self, master_window):
        """
        Placeholder function.

        :param master_window: a Frame, exteriormost GUI window.
        :return: None
        """
        pass
        # new_sudoku_frame = SudokuPage(master_window.get_container(), master_window)
        # master_window.del_from_frame_dictionary(SudokuPage)
        # master_window.add_to_frame_dictionary(SudokuPage, new_sudoku_frame)
        # for frame in (WelcomePage, SudokuPage):
        #     f = frame(container, self)
        #     self.frame_dictionary[frame] = f
        #     f.grid(row=0, column=0, sticky='nsew')


class SudokuPage(tk.Frame):
    """
    Creates the Sudoku Page and its contents including the sudoku board.
    """
    puzzle_board = []

    BOARD_SIZES = {"9x9": {"sub_sq_row": 3, "sub_sq_col": 3, "cell_row": 3, "cell_col": 3},
                   "12x12": {"sub_sq_row": 3, "sub_sq_col": 4, "cell_row": 4, "cell_col": 3},
                   "16x16": {"sub_sq_row": 4, "sub_sq_col": 4, "cell_row": 4, "cell_col": 4},
                   "25x25": {"sub_sq_row": 5, "sub_sq_col": 5, "cell_row": 5, "cell_col": 5},
                   "100x100": {"sub_sq_row": 10, "sub_sq_col": 10, "cell_row": 10, "cell_col": 10}}

    def __init__(self, parent_container, master_window):
        """
        Initializes the frames, necessary variables, buttons, and scrollbar widgets.

        :param parent_container: a Frame, the container frame for switching pages.
        :param master_window: a Frame, the exteriormost GUI window
        """
        tk.Frame.__init__(self, parent_container)
        self.puzzle_size = None
        self.brute_force_button_pressed = False
        self.csp_button_pressed = False
        self.brute_force_time = 0
        self.csp_time = 0
        self.brute_force_successful = False
        self.csp_successful = False
        self.solved_by = None

        # Create the outside frame of the SudokuPage
        self.sudoku_page_frame = tk.Frame(self)
        self.sudoku_page_frame.grid(row=0, column=0, sticky="nsew")
        self.sudoku_page_frame.rowconfigure(0, weight=1)
        self.sudoku_page_frame.columnconfigure(0, weight=1)

        # Creates the Canvas for the scrollbars to exist in
        self.sudoku_canvas = tk.Canvas(self.sudoku_page_frame, height=700, width=900)
        self.sudoku_canvas.grid(row=0, column=0, sticky="nsew")

        # Creates the scrollbars
        self.y_scrollbar = tk.Scrollbar(self.sudoku_page_frame, orient=tk.VERTICAL, command=self.sudoku_canvas.yview)
        self.y_scrollbar.grid(row=0, column=1, padx=20, sticky="ns")
        self.x_scrollbar = tk.Scrollbar(self.sudoku_page_frame, orient=tk.HORIZONTAL, command=self.sudoku_canvas.xview)
        self.x_scrollbar.grid(row=1, column=0, sticky="ew")

        # Configure and bind scroll bars
        self.sudoku_canvas.configure(yscrollcommand=self.y_scrollbar.set, xscrollcommand=self.x_scrollbar.set)
        self.sudoku_canvas.bind('<Configure>', lambda e: self.sudoku_canvas.configure(
            scrollregion=self.sudoku_canvas.bbox('all') if self.sudoku_canvas.bbox('all') else (0, 0, 1, 1)))

        # Creates frame to contain the grid canvas
        self.sudoku_frame = tk.Frame(self.sudoku_canvas, padx=20)
        # Bind the frame to the scrollable region
        self.sudoku_frame.bind('<Configure>', lambda e: self.sudoku_canvas.configure(
            scrollregion=self.sudoku_canvas.bbox('all') if self.sudoku_canvas.bbox('all') else (0, 0, 1, 1)))
        # Creates a window in the canvas to sho the frame
        self.sudoku_canvas.create_window((0, 0), anchor="nw", window=self.sudoku_frame)

        # activate master_window button commands
        master_window.brute_force_button.config(command=lambda: [
            self.replace_with_brute_force_solved(),
            self.set_brute_force_button_pressed(True)
        ])
        master_window.csp_button.config(command=lambda: [
            self.replace_with_csp_solved(),
            self.set_csp_button_pressed(True)
        ])
        master_window.clear_button.config(command=lambda: master_window.thread_runner(ButtonActions.CLEAR))

    def draw_puzzle(self, puzzle=None, solved=False):
        """
        Draws the sudoku grid based on the puzzle size and 2D that was input in the Welcome Page.

        :param puzzle: a 2D list of ints
        :param solved: a Boolean, is the puzzle solved.
        :return: None
        """
        # load default board sizes if needed
        if puzzle is None:
            puzzle = self.load_default_puzzle_board()
        selected_board = self.BOARD_SIZES[self.puzzle_size]

        # get the total number of columns and rows
        cell_col_count = selected_board["sub_sq_col"] * selected_board["cell_col"]
        cell_row_count = selected_board["sub_sq_row"] * selected_board["cell_row"]

        # create frames to hold each solved puzzle and label and place them accurately
        if self.puzzle_size != "100x100":
            # create a new frame to hold the canvases and labels
            puzzle_frame = tk.Frame(self.sudoku_frame)
            puzzle_frame.pack(side=tk.LEFT, padx=20, pady=5)

            # create placeholder label for the solved puzzles
            self.solved_by = tk.Label(puzzle_frame, text="", fg=Colours.BLUE.value, border=10)
            self.solved_by.pack(side=tk.TOP)

            # Create a canvas for drawing the grid
            board_canvas = tk.Canvas(puzzle_frame, width=20 * cell_col_count, height=20 * cell_row_count)
            board_canvas.pack(fill="both", expand=True)
        else:
            # create placeholder label for the solved puzzles
            self.solved_by = tk.Label(self.sudoku_frame, text="", fg=Colours.BLUE.value, border=10)
            self.solved_by.pack(side=tk.TOP)

            # Create a canvas for drawing the grid
            board_canvas = tk.Canvas(self.sudoku_frame, width=20 * cell_col_count, height=20 * cell_row_count)
            board_canvas.pack(fill="both", expand=True)

        # Shades sub-squares
        w = selected_board["cell_col"] * 20
        h = selected_board["cell_row"] * 20
        sub_sq_colours = [Colours.DARK_SHADE.value, Colours.LIGHT_SHADE.value]
        shade = True
        for r in range(0, selected_board["sub_sq_row"]):
            if selected_board["sub_sq_col"] % 2 == 0:
                shade = not shade
            for c in range(0, selected_board["sub_sq_col"]):
                shade = not shade
                x1 = r * h
                y1 = c * w
                x2 = x1 + h
                y2 = y1 + w
                board_canvas.create_rectangle(x1, y1, x2, y2, fill=sub_sq_colours[int(shade)])

        # generate the grid of rectangles
        for board_r in range(0, cell_row_count):  # row
            for board_c in range(0, cell_col_count):  # column
                text_color = Colours.BLACK.value
                if solved and self.puzzle_board[board_r][board_c] == 0:
                    text_color = Colours.BLUE.value

                # find the cell value in the list of strings:
                # board_r should be index in list, board_c should be index in string
                cell_value = puzzle[board_r][board_c]

                # draw each cell border on the canvas
                horiz_line_one = board_c * 20  # 20 is pixels
                vert_line_one = board_r * 20
                horiz_line_two = (board_c + 1) * 20
                vert_line_two = (board_r + 1) * 20

                # draw the rectangle and fill colour
                board_canvas.create_rectangle(horiz_line_one, vert_line_one, horiz_line_two, vert_line_two,
                                              outline="black")

                # if the string index of the list index is 0 (ie list index 0, string index 3), empty cell
                if cell_value != 0:
                    # add the text for the cell value
                    board_canvas.create_text((horiz_line_one + horiz_line_two) / 2,
                                             (vert_line_one + vert_line_two) / 2,
                                             text=cell_value, fill=text_color)

    def load_default_puzzle_board(self):
        """
        Loads a default puzzle board.

        :return: a 2D list of ints
        """
        self.set_puzzle_board(self.get_puzzle_from_preloaded(self.puzzle_size))
        return self.puzzle_board

    def set_puzzle_board(self, puzzle):
        """
        Sets the puzzle board.

        :param puzzle: a 2d list of ints
        :return: None
        """
        self.puzzle_board = puzzle

    def get_puzzle_board_copy(self):
        """
        Copies the set puzzle board.

        :return: a 2d list of ints
        """
        return [row[:] for row in self.puzzle_board]

    def get_puzzle_from_preloaded(self, size):
        """
        Returns the preloaded puzzle array of specified size
        :param size: String of puzzle dimensions
        """
        return PreloadedPuzzle().get_puzzle(size)

    def refresh(self, master_window):
        """
        This class method is called from the GUI classes switch frame method. The welcome and sudoku frames are created
        on program start, meaning that key data for their functionality is missing.
        The refresh method passes this data from the active instance of GUI to the already-create instance of the
        sudoku frame. It also triggers the creation of the sudoku grid chosen by the user.

        :param master_window: a Frame object
        :return: None
        """
        self.puzzle_size = master_window.get_grid_size()
        master_window.brute_force_button.config(state=tk.NORMAL if self.puzzle_size != "100x100" else tk.DISABLED)
        self.draw_puzzle()

    # These are just a bunch of methods for the popup box to work
    def set_brute_force_button_pressed(self, pressed):
        """
        Sets the Boolean brute force button pressed variable to true.

        :param pressed: a Boolean
        :return: None
        """
        self.brute_force_button_pressed = pressed

    def set_brute_force_successful(self, success):
        """
        Sets the Boolean brute force successful variable to true.

        :param success: a Boolean
        :return: None
        """
        self.brute_force_successful = success

    def set_csp_button_pressed(self, pressed):
        """
        Sets the Boolean csp button pressed variable to true.

        :param pressed: a Boolean
        :return: None
        """
        self.csp_button_pressed = pressed

    def set_csp_successful(self, success):
        """
        Sets the csp successful variable to true.

        :param success: a Boolean
        :return: None
        """
        self.csp_successful = success

    # methods for the clear_window method to reset everything
    def reset_button_pressed(self):
        """
        Used to reset the button pressed variables to false.

        :return: None
        """
        self.set_brute_force_button_pressed(False)
        self.set_csp_button_pressed(False)

    def reset_successful(self):
        """
        Resets the successful variables to false.

        :return: None
        """
        self.set_brute_force_successful(False)
        self.set_csp_successful(False)

    def reset_time(self):
        """
        Resets the calculated time.

        :return: None
        """
        self.brute_force_time = 0
        self.csp_time = 0

    def get_message(self, bf_button_pressed, csp_button_pressed, bf_success, csp_success):
        """
        Gets a specific message based on input boolean variables.

        :param bf_button_pressed: a Boolean
        :param csp_button_pressed: a Boolean
        :param bf_success: a Boolean
        :param csp_success: a Boolean
        :return: None
        """
        if bf_button_pressed and not csp_button_pressed:
            if bf_success:
                return f"Brute force solved: {self.brute_force_time:.5f} seconds"
            else:
                return "Brute force unable to solve :("

        if bf_button_pressed and csp_button_pressed:
            if bf_success and not csp_success:
                return f"Brute force solved: {self.brute_force_time:.5f} seconds\nCSP unable to be solved :( "
            elif not bf_success and csp_success:
                return f"Brute force unable to be solved\nCSP solved: {self.csp_time:.5f} seconds"
            else:
                return f"Brute Force solved: {self.brute_force_time:.5f} seconds \nCSP solved: {self.csp_time:.5f} seconds"

        if not bf_button_pressed and csp_button_pressed:
            if csp_success:
                return f"CSP solved: {self.csp_time:.5f} seconds"
            else:
                return "CSP unable to solve :("

    def replace_with_brute_force_solved(self):
        """
        Replaces the existing unsolved puzzle board with a new puzzle grid of the same puzzle, but solved by Brute Force.
        Will draw a second board if the first board is already solved by CSP.

        :return: None.
        """
        puzzle = [row[:] for row in self.puzzle_board]
        bfs = BruteForceSolver(puzzle)
        start_brute_force_time = time.perf_counter()  # start a timer
        solved_brute_force = bfs.solve()
        if solved_brute_force:
            self.set_brute_force_successful(True)
        end_brute_force_time = time.perf_counter()  # end timer
        self.brute_force_time = end_brute_force_time - start_brute_force_time

        if not self.csp_button_pressed:
            # Clear the canvas
            self.sudoku_frame.destroy()
            self.sudoku_frame = tk.Frame(self.sudoku_canvas)
            self.sudoku_canvas.create_window((20, 0), anchor="nw", window=self.sudoku_frame)

        # draw the new puzzle
        if self.brute_force_successful:
            self.draw_puzzle(solved_brute_force, solved=True)

        # set the popup menu
        self.show_messagebox(self.get_message(True,
                                              self.csp_button_pressed, self.brute_force_successful,
                                              self.csp_successful))

        self.solved_by.configure(text=f"BFS: {self.brute_force_time:.5f} seconds")

    def replace_with_csp_solved(self):
        """
        Replaces the existing unsolved puzzle board with a new puzzle grid of the same puzzle, but solved by CSP.
        Will draw a second board if the first board is already solved by Brute Force.

        :return: None
        """
        puzzle = [row[:] for row in self.puzzle_board]
        csp_solver = CSP(puzzle)
        start_csp_time = time.perf_counter()  # start a timer
        solved_csp = csp_solver.solve()
        if solved_csp:
            self.set_csp_successful(True)
        end_csp_time = time.perf_counter()  # end timer
        self.csp_time = end_csp_time - start_csp_time

        if not self.brute_force_button_pressed:
            # Clear the canvas
            self.sudoku_frame.destroy()
            self.sudoku_frame = tk.Frame(self.sudoku_canvas)
            self.sudoku_canvas.create_window((20, 0), anchor="nw", window=self.sudoku_frame)

        # draw the new puzzle
        if self.csp_successful:
            self.draw_puzzle(solved_csp, solved=True)

        # set the popup menu
        self.show_messagebox(self.get_message(self.brute_force_button_pressed,
                                              True, self.brute_force_successful,
                                              self.csp_successful))

        # update label
        self.solved_by.configure(text=f"CSP: {self.csp_time:.5f} seconds")

    def show_messagebox(self, message):
        """
        Creates a popup message box with the designated message.

        :param message: a String
        :return: None
        """
        popup = tk.Toplevel()
        tk.Label(popup, text=message).pack()
        tk.Button(popup, text="OK", command=popup.destroy).pack()


class ButtonActions(Enum):
    """
    Sets the button events to a specific string.
    """
    CLEAR = "Clear"
    LOAD_FILE = "Load File"
    PLAY = "Go Solve"
    BRUTE_FORCE = "Solve (Brute Force)"
    CSP = "Solve (CSP)"
    EXIT = "Exit"


class Colours(Enum):
    """
    Sets the colours to a specific string.
    """
    BLUE = "#5881A5"
    BLACK = "#222222"
    DARK_SHADE = "#DFECEC"
    LIGHT_SHADE = "#FAF8F1"


if __name__ == "__main__":
    test = Gui()
    test.mainloop()
