class Label:
    def __init__(self, position, size, text, alignment="left"):
        self.position = position
        self.size = size
        self.text = text
        self.alignment = alignment

    def render(self, screen):
        x = self.position.x
        y = self.position.y
        text_length = len(self.text)

        if self.alignment == "center":
            x = (self.size.width - text_length) // 2
        elif self.alignment == "right":
            x = self.size.width - text_length
        screen.addstr(y, x, self.text)
