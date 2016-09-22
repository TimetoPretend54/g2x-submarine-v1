import curses


class Window:
    def __init__(self, title):
        self.title = title

    def render(self, screen):
        title_len = len(self.title)
        screen_width = curses.COLS

        if title_len < screen_width - 4:
            left = (screen_width - title_len) // 2
            screen.addstr(1, left, self.title)
