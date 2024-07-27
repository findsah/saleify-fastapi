import logging
from enum import Enum
from lxml import etree

from pyjt.Robot import Robot
from pyjt.ComponentFinder import ComponentFinder, Locator
from pyjt.Errors import ElementNotFoundError
from pyjt.Inspector import Inspector

log = logging.getLogger(__name__)

FillMode = Enum('FillMode', ['TYPE', 'SET', 'PASTE'])


class Fixture:
    """ Wrapper class to control a specific UI element.
    """
    def __init__(self, control):
        self._control = control
        self.robot = Robot()

    def locate(self, locator=None, **kwargs):
        """ Search a control as a sub-element of the control
            managed by this fixture.

            Args:
                locator (Locator):  A locator object to find the sub-control
                **kwargs:           Additional search parameters.

            Returns:
                Fixture:
                    A fixture pointing to the first component
                    matching the search criteria.

            Raises:
                ElementNotFoundError:
                    No element was found matching the search criteria
        """
        log.debug(f"frame.find({locator}, {kwargs})")
        locator = locator if locator else Locator(**kwargs)
        control = ComponentFinder.findIn(self._control.getComponents, locator)
        if not control:
            raise ElementNotFoundError(f"Control({kwargs}) not found!")
        return Fixture(control)

    def find(self, role, **kwargs):
        """ Search a control of type **role** as a sub-control of this control.

            Args:
                role (Class):
                    The class type of the component to look for, e.g.
                    javax.swing.JTextField
                **kwargs:
                    Search criteria for the component.

            Returns:
                Fixture:
                    A fixture pointing to the first component
                    matching the search criteria.

            Raises:
                ElementNotFoundError:
                    No element was found matching the search criteria
        """
        kwargs['role'] = role
        return self.locate(**kwargs)

    def find_by_xpath(self, xpath):
        """ Locate a component by xpath.

            This function searches the component tree using an xpath-expression
            to locate an element.

            Args:
                xpath (string): The xpath used for searching

            Returns:
                Fixture:
                    A fixture reference to the first component
                    matching the given xpath expression.

            Raises:
                ElementNotFoundError:
                    If no element was found matching the given xpath

            Example:

            .. code:: python

                    # search for a JTextField inside a Container which also contains
                    # a label with the text "Name"
                    textfield = frame.find_by_xpath('//Container[//JLabel[@text="Name"]]/JTextField')
        """
        fixture = ComponentFinder.find_by_xpath(self, xpath)
        if not fixture:
            raise ElementNotFoundError(f"No element found matching xpath: '{xpath}'")
        return fixture

    def click(self):
        """ Move the mouse over this control and execute a click. """
        log.debug(f"click({self._control})")
        self.robot.move(self._control)
        log.debug(f"executing click({self._control})")
        self.robot.click()

    def fill(self, text, mode=FillMode.TYPE, clear=True):
        """ Fill this control with the given **text**.

            Args:
                text:   Text to fill this control with.
                mode:   FillMode - Choose the mode to fill the control with the given text.
                        See the table below.
                clear:  If set to True, select all text in the given control
                        before typing.

            FillMode:

                FillMode.TYPE:
                  - Fill the control by emulating keystrokes.
                  - Only supports US keyboard layout at this time.
                FillMode.SET:
                  -   Just set the text of the  component using the component.setText() function.
                  -   The existing text is always overwritten ignoring the **clear** argument
                FillMode.PASTE:
                  - Fill the control by pasting the text from the clipboard
                  - **Not implemented yet**

        """
        if mode == FillMode.TYPE:
            self.click()
            if clear:
                self.robot.selectAll()
                self.robot.typeVirtualKeys(self.robot.Events.VK_DELETE)
            self.robot.type(text)
        if mode == FillMode.SET:
            self._control.setText(text)

    def components(self):
        """ Returns:
                Fixture[]:
                    An array of Fixture references of all child
                    components of this component.
        """
        return [Fixture(el) for el in self.getComponents()]

    def dump(self, encoding="utf-8"):
        """ Returns:
                string: A xml-representation of the component tree of this component.

            Args:
                encoding (string):
                    The encoding to use to convert the component to xml
        """
        return etree.tostring(self.etree(), pretty_print=True, encoding=encoding)

    @property
    def control(self):
        """ Returns:
                Proxy:  A reference to the control managed by this fixture.
        """
        return self._control

    @property
    def type(self):
        """ Returns:
                ClassType: The type of class of this component
        """
        return type(self._control.object)

    def etree(self):
        return Inspector.etree(self)

    def __getattr__(self, name):
        return getattr(self._control, name)

    def __repr__(self):
        return str(self._control)
