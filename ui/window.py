import curses
from label import Label
from point import Point
from size import Size


class Window:
    def __init__(self, title, position=None, size=None):
        # determine window position
        if position is None:
            x = 0
            y = 0
        else:
            x, y = position

        # determin window size
        if size is None:
            width = curses.COLS
            height = curses.LINES
        else:
            width, height = size

        position = Point(0, 1)
        size = Size(curses.COLS, 1)
        self.window = curses.newwin(height, width, y, x)
        self.title = Label(position, size, title, "center")

    def render(self, screen):
        self.window.border()
        self.window.refresh()
        # self.title.render(screen)
