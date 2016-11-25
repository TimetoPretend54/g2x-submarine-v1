import time


class Data:
    def __init__(self, secs_since_epoch, depth_text, depth_path_data, temperature_chart, frame_path):
        # general settings
        self.width = 1296
        self.height = 972
        self.padding = 5
        self.graph_background_color = "white"
        self.graph_background_opacity = 0.4
        self.frame_path = frame_path

        # date/time settings
        self.time = time.localtime(secs_since_epoch)
        self.frame_date = time.strftime("%B %d, %Y", self.time)
        self.frame_time = time.strftime("%I:%M:%S %p", self.time)
        self.font_size = 22
        self.text_color = "rgb(255,255,255)"
        
        # depth chart 
        self.depth_text = depth_text
        self.depth_font_size = 12
        self.depth_color = "rgb(0,192,0)"
        self.depth_text_color = "rgb(32,32,32)"
        self.depth_graph_width = 100
        self.depth_graph_height = 300
        self.depth_path_data = depth_path_data

        # temperature chart
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
