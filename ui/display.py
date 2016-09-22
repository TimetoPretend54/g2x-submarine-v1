import curses


class Display:
    def __init__(self, screen):
        self.screen = screen
        self.windows = []
        self.current_index = 0

    def add_window(self, window):
        self.windows.append(window)

    def render(self):
        if 0 <= self.current_index < len(self.windows):
            self.screen.move(1, 0)
            self.screen.clrtoeol()
            self.screen.border()
            self.screen.hline(2, 1, curses.ACS_HLINE, curses.COLS - 2)
            self.windows[self.current_index].render(self.screen)
            self.screen.addstr(1, 1, "<-")
            self.screen.addstr(1, curses.COLS - 3, "->")
            self.screen.hline(curses.LINES - 3, 1, curses.ACS_HLINE, curses.COLS - 2)
            self.screen.move(curses.LINES - 2, 1)

    def process_key(self):
        ch = self.screen.getch()

        if ch == -1:
            return True
        elif ch == ord('q'):
            return False
        # elif ch == 410:
        #     # resize
        #     self.screen.clear()
        #     self.render()
        elif ch == 260:
            # left
            if self.current_index == 0:
                self.current_index = len(self.windows) - 1
            else:
                self.current_index -= 1
            self.render()
            return True
        elif ch == 261:
            # right
            if self.current_index == len(self.windows) - 1:
                self.current_index = 0
            else:
                self.current_index += 1
            self.render()
            return True
        else:
            self.screen.addstr(1, 0, "key = " + str(ch) + "," + chr(ch))
            return True
