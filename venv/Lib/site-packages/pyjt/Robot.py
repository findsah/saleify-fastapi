import time
import logging

from pyjt import Proxy

log = logging.getLogger(__name__)


class Robot:
    """ Smart robot features for controlling the application.

        Args:
            robot (java.awt.Robot):
                Use the given java.awt.Robot() object
                If **robot** is None, create a own instance of the robot class.
            typespeed (int):
                The speed to type text in number of keystrokes per second.
    """
    _robot = None

    @property
    def Events(self):
        from java.awt.event import KeyEvent
        return KeyEvent

    def __init__(self, robot=None, typespeed=20):
        import java
        from java.awt.event import KeyEvent

        self._robot = Proxy(robot) if robot else Robot._robot
        if not self._robot:
            Robot._robot = Proxy(java.awt.Robot())
            self._robot = Robot._robot

        self._typespeed = typespeed

        self._KeyCodes = {
                'a': [KeyEvent.VK_A],
                'b': [KeyEvent.VK_B],
                'c': [KeyEvent.VK_C],
                'd': [KeyEvent.VK_D],
                'e': [KeyEvent.VK_E],
                'f': [KeyEvent.VK_F],
                'g': [KeyEvent.VK_G],
                'h': [KeyEvent.VK_H],
                'i': [KeyEvent.VK_I],
                'j': [KeyEvent.VK_J],
                'k': [KeyEvent.VK_K],
                'l': [KeyEvent.VK_L],
                'm': [KeyEvent.VK_M],
                'n': [KeyEvent.VK_N],
                'o': [KeyEvent.VK_O],
                'p': [KeyEvent.VK_P],
                'q': [KeyEvent.VK_Q],
                'r': [KeyEvent.VK_R],
                's': [KeyEvent.VK_S],
                't': [KeyEvent.VK_T],
                'u': [KeyEvent.VK_U],
                'v': [KeyEvent.VK_V],
                'w': [KeyEvent.VK_W],
                'x': [KeyEvent.VK_X],
                'y': [KeyEvent.VK_Y],
                'z': [KeyEvent.VK_Z],
                'A': [KeyEvent.VK_SHIFT, KeyEvent.VK_A],
                'B': [KeyEvent.VK_SHIFT, KeyEvent.VK_B],
                'C': [KeyEvent.VK_SHIFT, KeyEvent.VK_C],
                'D': [KeyEvent.VK_SHIFT, KeyEvent.VK_D],
                'E': [KeyEvent.VK_SHIFT, KeyEvent.VK_E],
                'F': [KeyEvent.VK_SHIFT, KeyEvent.VK_F],
                'G': [KeyEvent.VK_SHIFT, KeyEvent.VK_G],
                'H': [KeyEvent.VK_SHIFT, KeyEvent.VK_H],
                'I': [KeyEvent.VK_SHIFT, KeyEvent.VK_I],
                'J': [KeyEvent.VK_SHIFT, KeyEvent.VK_J],
                'K': [KeyEvent.VK_SHIFT, KeyEvent.VK_K],
                'L': [KeyEvent.VK_SHIFT, KeyEvent.VK_L],
                'M': [KeyEvent.VK_SHIFT, KeyEvent.VK_M],
                'N': [KeyEvent.VK_SHIFT, KeyEvent.VK_N],
                'O': [KeyEvent.VK_SHIFT, KeyEvent.VK_O],
                'P': [KeyEvent.VK_SHIFT, KeyEvent.VK_P],
                'Q': [KeyEvent.VK_SHIFT, KeyEvent.VK_Q],
                'R': [KeyEvent.VK_SHIFT, KeyEvent.VK_R],
                'S': [KeyEvent.VK_SHIFT, KeyEvent.VK_S],
                'T': [KeyEvent.VK_SHIFT, KeyEvent.VK_T],
                'U': [KeyEvent.VK_SHIFT, KeyEvent.VK_U],
                'V': [KeyEvent.VK_SHIFT, KeyEvent.VK_V],
                'W': [KeyEvent.VK_SHIFT, KeyEvent.VK_W],
                'X': [KeyEvent.VK_SHIFT, KeyEvent.VK_X],
                'Y': [KeyEvent.VK_SHIFT, KeyEvent.VK_Y],
                'Z': [KeyEvent.VK_SHIFT, KeyEvent.VK_Z],
                '`': [KeyEvent.VK_BACK_QUOTE],
                '0': [KeyEvent.VK_0],
                '1': [KeyEvent.VK_1],
                '2': [KeyEvent.VK_2],
                '3': [KeyEvent.VK_3],
                '4': [KeyEvent.VK_4],
                '5': [KeyEvent.VK_5],
                '6': [KeyEvent.VK_6],
                '7': [KeyEvent.VK_7],
                '8': [KeyEvent.VK_8],
                '9': [KeyEvent.VK_9],
                '-': [KeyEvent.VK_MINUS],
                '=': [KeyEvent.VK_EQUALS],
                '~': [KeyEvent.VK_SHIFT, KeyEvent.VK_BACK_QUOTE],
                '!': [KeyEvent.VK_SHIFT, KeyEvent.VK_1],
                '@': [KeyEvent.VK_SHIFT, KeyEvent.VK_2],
                '#': [KeyEvent.VK_SHIFT, KeyEvent.VK_NUMBER_SIGN],
                '$': [KeyEvent.VK_SHIFT, KeyEvent.VK_4],
                '%': [KeyEvent.VK_SHIFT, KeyEvent.VK_5],
                '^': [KeyEvent.VK_SHIFT, KeyEvent.VK_CIRCUMFLEX],
                '&': [KeyEvent.VK_SHIFT, KeyEvent.VK_AMPERSAND],
                '*': [KeyEvent.VK_SHIFT, KeyEvent.VK_ASTERISK],
                '(': [KeyEvent.VK_LEFT_PARENTHESIS],
                ')': [KeyEvent.VK_RIGHT_PARENTHESIS],
                '_': [KeyEvent.VK_SHIFT, KeyEvent.VK_UNDERSCORE],
                '+': [KeyEvent.VK_PLUS],
                '\t': [KeyEvent.VK_TAB],
                '\n': [KeyEvent.VK_ENTER],
                '[': [KeyEvent.VK_OPEN_BRACKET],
                ']': [KeyEvent.VK_CLOSE_BRACKET],
                '\\': [KeyEvent.VK_BACK_SLASH],
                '{': [KeyEvent.VK_SHIFT, KeyEvent.VK_OPEN_BRACKET],
                '}': [KeyEvent.VK_SHIFT, KeyEvent.VK_CLOSE_BRACKET],
                '|': [KeyEvent.VK_SHIFT, KeyEvent.VK_BACK_SLASH],
                ';': [KeyEvent.VK_SEMICOLON],
                ':': [KeyEvent.VK_COLON],
                '\'': [KeyEvent.VK_QUOTE],
                '"': [KeyEvent.VK_SHIFT, KeyEvent.VK_QUOTEDBL],
                ',': [KeyEvent.VK_COMMA],
                '<': [KeyEvent.VK_SHIFT, KeyEvent.VK_COMMA],
                '.': [KeyEvent.VK_PERIOD],
                '>': [KeyEvent.VK_SHIFT, KeyEvent.VK_PERIOD],
                '/': [KeyEvent.VK_SLASH],
                '?': [KeyEvent.VK_SHIFT, KeyEvent.VK_SLASH],
                ' ': [KeyEvent.VK_SPACE],
        }

    def move(self, control):
        """ Move the mouse pointer to the position of a **control**.

            :param control: The control to move the mouse pointer to.
        """
        position = control.getLocationOnScreen()
        self._robot.mouseMove(position.x + 2, position.y + 2)

    def click(self):
        """ Execute a click of the left mouse. """
        import java
        btn = java.awt.event.InputEvent.getMaskForButton(1)
        self._robot.mousePress(btn)
        time.sleep(1 / self._typespeed)
        self._robot.mouseRelease(btn)

    def selectAll(self):
        """ Emulate selecting all text in the current context by pressing CTRL-A. """
        from java.awt.event import KeyEvent
        self.typeVirtualKeys([KeyEvent.VK_CONTROL, KeyEvent.VK_A])

    def type(self, text):
        """ Emulate user typing the given text.

            Typing is emulated by generating VK_* events. The type speed
            (delay between each keystroke) is configured in the
            Robot's constructor's `typespeed` argument.

            Args:
                text (string):    Text to type.

            Note:
                Currently, this function assumes that a english keyboard layout
                is used.
        """
        for char in text:
            if char not in self._KeyCodes:
                raise Exception("Unknown character to type: '{char}'")
            self.typeVirtualKeys(self._KeyCodes[char])

    def typeVirtualKeys(self, vks):
        if type(vks) is not list:
            vks = [vks]
        vks = vks.copy()
        for vk in vks:
            time.sleep(1 / self._typespeed)
            self._robot.keyPress(vk)
        vks.reverse()
        for vk in vks:
            time.sleep(1 / self._typespeed)
            self._robot.keyRelease(vk)
