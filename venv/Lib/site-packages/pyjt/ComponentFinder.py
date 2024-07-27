import time
import logging
from lxml import etree

from pyjt.Proxy import Proxy
from pyjt.Inspector import Inspector

log = logging.getLogger(__name__)


class Locator:
    """ The Locator determines if a component matches specific search
        criteria.

        Args:
            **kwargs:   Search parameters as keyword arguments.

        Search criteria:
            The locator constructor receives a list of <name>:<value>
            keyword arguments and stores them.

            For each argument, the locator will call the component's
            get<Name>() function and compares it's return value to <value>.
            Only if the values are equal, the component matches this
            search criteria.
    """
    def __init__(self, **kwargs):
        self._filters = kwargs
        self._contains = []
        self._has = []

    def update(self, **kwargs):
        """ Add more search criteria's to this locator.

            Args:
                **kwargs:   The search criteria's to add.
                            Any existing search criteria will be overwritten.

            Returns:
                A reference to this locator object (self)
        """
        self._filters.update(**kwargs)
        return self

    def contains(self, **kwargs):
        """ Ensure the control has a sub-component with the given attributes
            somewhere in the tree.

            Args:
                **kwargs:   The search criteria for the sub-component
                            that has to be a part of the component candiate.

            Returns:
                A reference to this locator object (self)
        """
        self._contains.append(Locator(**kwargs))
        return self

    def has(self, **kwargs):
        """ Ensure the control has a direct sub-component with the given
            attributes.
        """
        self._has.append(Locator(**kwargs))
        return self

    def matches(self, component):
        """ The matches function determines wether the given component matches
            matches the search criteria.

            You can implement your own matcher by deriving a class from this
            Locator and implement this function.

            Args:
                component:  The component that should match this search
                            criteria.
            Returns:
                True, if the component matches this search criteria, otherwise False.
        """

        if not _matches(component, **self._filters):
            return False

        log.debug(f"found {component}, checking childs...")
        for locator in self._contains:
            log.debug(f"contains {locator}")
            if ComponentFinder._locate(window=component, locator=locator) is None:
                return False

        for locator in self._has:
            log.debug(f"has {locator}")
            if not _child_matches(component, locator):
                return False
        return True

    def __repr__(self):
        return f"Locator({self._filters})"


def _child_matches(component, locator):
    log.debug(f"_child_matches({component}, {locator}")
    for subcontrol in component.getComponents():
        if locator.matches(subcontrol):
            log.debug(f"_child_matches({component}, {locator}: found {subcontrol}")
            return True
    log.debug(f"_child_matches({component}, {locator}: FAILED")
    return False


class Timer:
    def __init__(self, timeout=None, cycle=None):
        self._timeout = timeout
        self._cycle = cycle
        self._first = True

    def start(self):
        self._started = time.time()
        return self

    def elapsed(self, seconds=None):
        if not self._first:
            time.sleep(self._cycle)
        self._first = False
        now = time.time()
        timeout = seconds if seconds else self._timeout
        return self._started + timeout <= now


class ComponentFinder:
    DEFAULT_TIMEOUT = 1
    DEFAULT_DELAY = 1

    @staticmethod
    def find(window, locator=None, timeout=None, **kwargs):
        timeout = timeout if timeout else ComponentFinder.DEFAULT_TIMEOUT
        timer = Timer(timeout, ComponentFinder.DEFAULT_DELAY).start()
        locator = locator if locator else Locator(**kwargs)

        while not timer.elapsed():
            log.debug(f"retry({locator})")
            hit = ComponentFinder._locate(window, locator)
            if hit is not None:
                return hit
        return None

    @staticmethod
    def find_by_xpath(control, xpath, timeout=None):
        timeout = timeout if timeout else ComponentFinder.DEFAULT_TIMEOUT
        timer = Timer(timeout, ComponentFinder.DEFAULT_DELAY).start()
        xp = etree.XPath(xpath)

        while not timer.elapsed():
            log.debug(f"retry({xpath})")
            (tree, mapping) = Inspector.etreemap(control)
            el = xp(tree)
            if not el:
                continue
            _id = el[0].get("_id")
            log.warning(_id)
            return mapping[int(_id)]

    @staticmethod
    def findIn(func, locator=None, timeout=None):
        timeout = timeout if timeout else ComponentFinder.DEFAULT_TIMEOUT
        timer = Timer(timeout, ComponentFinder.DEFAULT_DELAY).start()

        while not timer.elapsed():
            log.debug(f"retry({locator})")
            windows = func()
            for window in windows:
                hit = ComponentFinder._locate(window, locator)
                if hit is not None:
                    return hit
        return None

    @staticmethod
    def _locate(window, locator):
        log.debug(f"locate({locator})")
        if locator.matches(window):
            return window
        components = window.getComponents()
        for cmpt in components:
            log.debug(f"found component: {cmpt.getName()} {type(cmpt)}")
            hit = ComponentFinder._locate(cmpt, locator)
            if hit:
                return hit
        return None


@staticmethod
def _matches(cmpt, **kwargs):
    # log.debug(f"_matches({cmpt}, name={name}, text={text})")
    for name, value in kwargs.items():
        if name == 'role':
            cc = cmpt.object if isinstance(cmpt, Proxy) else cmpt
            log.debug(f"\tcheck01 {name} {type(cc)}={value}")
            check = isinstance(cc, value)
            log.debug(f"\t\tcheck01: {check}")
            if not check:
                return False
            continue
        fname = f"get{name[0].capitalize()}{name[1:]}"
        log.debug(f"check({name}, {value}) -> {fname}: {cmpt}")
        if not hasattr(cmpt, fname):
            log.debug(f"\tcheck({name}) component has no attr {fname}")
            return False
        fnc = getattr(cmpt, fname)
        _value = fnc()
        log.debug(f"\tcheck {value} == {_value}")
        if value is None and _value is None:
            continue
        if not _value:
            return False
        if value not in _value:
            return False
    if not cmpt.isShowing():
        log.debug("\tcheck9")
        return False
    log.debug("\tcheck10")
    return True
