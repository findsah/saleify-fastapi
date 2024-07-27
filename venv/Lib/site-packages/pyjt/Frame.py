""" Find and control a frame.
"""
import logging

from pyjt.Errors import ElementNotFoundError
from pyjt.ComponentFinder import Locator
from pyjt.Fixture import Fixture
from pyjt.Inspector import Inspector
from pyjt import Proxy

log = logging.getLogger(__name__)


class FrameFinder:
    """ Find a frame in the list of application frames.

        Example:

        .. code:: python

            frame = FrameFinder(title="Hello World")
            frame.find(JTextField, name="first name")
    """
    @staticmethod
    def find(locator=None, **kwargs):
        """Find a frame by a locator or frame attributes.

            Args:
                locator (Locator):  Locator to find a frame.
                **kwargs:           Search filters by keyword arguments.

            Raises:
                ElementNotFoundError:
                         No frame was found matching the given search criteria.

            Returns:
                Frame:
                    The first frame in the list of frames matching
                    the search criteria.
        """
        from java.awt import Window
        locator = locator if locator else Locator(**kwargs)
        wp = Proxy(Window)
        for window in wp.getWindows():
            if locator.matches(window):
                return Frame(window)
        raise ElementNotFoundError(f"Window {locator} not found!")

    @staticmethod
    def inspect():
        """ Inspect a component.

            Returns:
                dict:
                    A dicitionary tree of all ui components of all available
                    frames.
        """
        from java.awt import Window
        wp = Proxy(Window)
        result = []
        for window in wp.getWindows():
            result.append(Inspector.inspect(window))
        return result


class Frame(Fixture):
    """ Wrapper for controlling a frame. """
    def dispose(self):
        """ Dispose this frame. """
        self._control.dispose()

    def close(self):
        """ Close this frame by sending a close message. """
        from java.awt.event import WindowEvent
        self._control.object.dispatchEvent(WindowEvent(self._control.object, WindowEvent.WINDOW_CLOSING))
