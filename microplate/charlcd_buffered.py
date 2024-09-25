import time


class CharLCD(object):
    def __init__(self, width, height, driver, cursor_visible=1, cursor_blink=1):
        self.width = width
        self.height = height
        self.driver = driver
        self.current_pos = {
            'x': 0,
            'y': 0
        }
        self.cursor_blink = cursor_blink
        self.cursor_visible = cursor_visible
        self.twin_lcd = False  # are we using 40x4 = 2* 20x4 lcd ?
        if self.driver.pins['E2'] is not None:
            self.twin_lcd = True
        self.screen = []
        self.buffer = []
        self.initialized = False
        self.dirty = False

    def init(self):
        """Inits lcd display, send commands"""
        self.driver.init()
        self._init(0)
        if self.is_twin():
            self._init(1)
        self.screen = [" " * self.width] * self.height
        self.buffer = [" " * self.width] * self.height
        self.initialized = True

    def _init(self, enable):
        """subroutine to init lcd"""
        self.driver.cmd(3, enable)
        time.sleep(0.05)
        self.driver.cmd(3, enable)
        time.sleep(0.05)
        self.driver.cmd(3, enable)
        time.sleep(0.05)
        self.driver.cmd(2, enable)
        self.driver.set_mode(4)
        self.driver.cmd(0x28, enable)
        self.driver.cmd(0x08, enable)
        self.driver.cmd(0x01, enable)
        self.driver.cmd(0x06, enable)
        self.driver.cmd(12 +
                        (self.cursor_visible * 2) +
                        (self.cursor_blink * 1), enable)

    def is_twin(self):
        """returns true if we are using twin lcd"""
        return self.twin_lcd

    def get_width(self):
        """returns lcd width"""
        return self.width


    def get_height(self):
        """return lcd height"""
        return self.height

    def get_display_mode(self):
        """return display mode, direct or buffered"""
        return 'buffered'

    def shutdown(self):
        """call shutdown on driver"""
        self.driver.shutdown()

    def write(self, content, pos_x=None, pos_y=None):
        """Writes content into buffer at position(x,y) or current
        Will change internal position marker to reflect string write
        Args:
            content: content to write
            pos_x: x position
            pos_y: y position
        """
        if pos_x is None:
            pos_x = self.current_pos['x']
        if pos_y is None:
            pos_y = self.current_pos['y']

        if pos_x >= self.width:
            raise IndexError
        if pos_y >= self.height:
            raise IndexError

        line = self.buffer[pos_y]
        new_line = line[0:pos_x] + content + line[pos_x + len(content):]
        line = new_line[:self.width]
        self.buffer[pos_y] = line
        self.current_pos = {
            'x': pos_x + len(content),
            'y': pos_y
        }
        self.dirty = True

    def buffer_clear(self, from_x=None, from_y=None, width=None, height=None):
        """Clears buffer. Its not recommended to use parameters.
        Args:
            from_x: x position
            from_y: y position
            width: width of area
            height: height of area
        """
        if from_x is None and from_y is None:
            self.buffer = [" " * self.width] * self.height
        else:
            if height is None:
                height = self.height - from_y
            if width is None:
                width = self.width - from_x

            for pos_y in range(from_y, from_y + height):
                line = self.buffer[pos_y]
                self.buffer[pos_y] = line[0:from_x] + (" " * width) \
                    + line[from_x + width:]
        self.dirty = True

    def flush(self, redraw_all=False):
        """Flush buffer to screen, skips chars that didn't change"""
        if not self.dirty:
            return
        # if issubclass(type(self.driver), FlushEvent):
        #     self.driver.pre_flush(self.buffer)

        bag = list(
            zip(list(range(0, self.get_height())), self.buffer, self.screen)
        )
        for line, line_new, line_current in bag:
            if line_new != line_current or redraw_all:
                i = 0
                last_i = -1
                for char_new, char_current in zip(line_new, line_current):
                    if char_new != char_current or redraw_all:
                        if last_i != i:
                            self.driver.cmd(
                                self.get_line_address(line) + i,
                                self._get_enable(line)
                            )
                            last_i = i
                        self.driver.char(
                            char_new,
                            self._get_enable(line)
                        )
                        last_i += 1
                    i += 1
                self.screen[line] = line_new
        self.dirty = False
        # if issubclass(type(self.driver), FlushEvent):
        #     self.driver.post_flush(self.buffer)

    def stream(self, string):
        """Stream string - use stream_char
        Args:
            string: string to display
        """
        for char in string:
            self._stream_char(char)

    def _stream_char(self, char):
        """Stream char on screen, following chars are put one after another.
        Restart from beginning after reaching end
        Args:
            char: char to display
        """
        self.write(char)
        self._next_cursor_position()

    def _next_cursor_position(self):
        """calculate next cursor position"""
        if self.current_pos['x'] >= self.width:
            self.current_pos['x'] = 0
            self.current_pos['y'] += 1
            if self.current_pos['y'] >= self.height:
                self.current_pos['y'] = 0
            self.set_xy(0, self.current_pos['y'])

    def set_xy(self, pos_x, pos_y):
        """Set cursor position to (x, y)
        Args:
            pos_x: x position
            pos_y: y position
        """
        if pos_x >= self.width or pos_x < 0:
            raise IndexError
        if pos_y >= self.height or pos_y < 0:
            raise IndexError
        self.current_pos['x'] = pos_x
        self.current_pos['y'] = pos_y

    def get_xy(self):
        """return current cursor position"""
        return self.current_pos

    def get_line_address(self, pos_y=None):
        """Return start hex address for line
        Args:
            pos_y: line number
        """
        if pos_y is None:
            pos_y = self.current_pos['y']

        if pos_y >= self.height or pos_y < 0:
            raise IndexError

        if not self.is_twin() or pos_y < 2:
            return self.driver.get_line_address(pos_y)

        return self.driver.get_line_address(pos_y - 2)

    def _get_enable(self, pos_y=None):
        """get proper enable line
        Args:
            pos_y: line number
        """
        if pos_y is None:
            pos_y = self.current_pos['y']
        if self.is_twin() and pos_y > 1:
            enable = 1
        else:
            enable = 0

        return enable

    def add_custom_char(self, pos, bytes):
        pos = 0x40 + (0x08 * pos)
        self.driver.cmd(pos)
        for data in bytes:
            self.driver.char(chr(data))
        self.driver.cmd(0x01)
