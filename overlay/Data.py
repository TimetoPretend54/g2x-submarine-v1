import time


class Data:
    def __init__(self, secs_since_epoch, depth_chart, temperature_chart, frame_path):
        # general settings
        self.width = 1296
        self.height = 972
        self.padding = 5
        self.frame_path = frame_path

        # date/time settings
        self.time = time.localtime(secs_since_epoch)
        self.frame_date = time.strftime("%B %d, %Y", self.time)
        self.frame_time = time.strftime("%I:%M:%S %p", self.time)
        self.font_size = 22
        self.text_color = "rgb(255,255,255)"
        
        # charts
        self.depth_chart = depth_chart.to_svg()
        self.temperature_chart = temperature_chart.to_svg()

    @property
    def datetime_x(self):
        return self.width - self.padding

    @property
    def depth_background_y(self):
        return self.height - 3 * self.padding - self.depth_graph_height

    @property
    def depth_background_width(self):
        return self.depth_graph_width + 2 * self.padding

    @property
    def depth_background_height(self):
        return self.depth_graph_height + 2 * self.padding

    @property
    def depth_text_x(self):
        return self.depth_background_width * 0.5

    @property
    def depth_text_y(self):
        return self.depth_background_height - self.padding
