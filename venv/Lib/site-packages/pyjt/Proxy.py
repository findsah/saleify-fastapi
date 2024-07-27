import jpype
import logging

log = logging.getLogger(__name__)


class Proxy:
    """ Proxy calls to the java.awt and javax.swing libraries using
        the event thread to ensure thread-safety.

        This class is usually automatically instanciated and returned
        by the locate() and find() functions of pyjt.

        If the proxy detects that the return value of the call
        is a instance of java.awt.Component, a new proxy instance
        for this object is created and returned.

        Args:
            obj (java.awt.Component):
                The component to control with this Proxy.

        Example:

        .. code:: python

            proxy = Proxy(java.swing.JLabel())
            text = proxy.getText()
    """
    def __init__(self, obj):
        self._object = obj

    @property
    def object(self):
        """ Returns:
                java.awt.Component: The control object managed by this proxy.
        """
        return self._object

    def isinstance(self, classtype):
        """ Check if the object managed by this class is an instance of **classtype**.

            Args:
                classtype (Class): The class type.

            Returns:
                boolean:
                    True, if the object managed by this proxy
                    is a instance of class **classtype**
        """
        return isinstance(self._object, classtype)

    def __getattr__(self, name):
        import javax
        import java

        @jpype.JImplements(java.lang.Runnable)
        class _Launch:
            def __init__(self, func, *args, **kwargs):
                self._func = func
                self._args = args
                self._kwargs = kwargs
                self._ret = None

            @jpype.JOverride
            def run(self):
                try:
                    if callable(self._func):
                        self._ret = self._func(*self._args, **self._kwargs)
                    else:
                        self._ret = self._func
                except Exception as ee:
                    log.error(str(ee))
                    raise ee

        fnc = getattr(self._object, name)

        def _savecall(*args, **kwargs):
            # log.debug(f"proxying call: {name}({args}, {kwargs})")
            launcher = _Launch(fnc, *args, **kwargs)
            javax.swing.SwingUtilities.invokeAndWait(launcher)
            ret = launcher._ret
            # log.debug(f"\tret is {ret} {type(ret)}")
            if hasattr(ret, "__iter__"):
                # log.info("\tlist detected!")
                return [_proxitise(element) for element in ret]
            return _proxitise(ret)
        if not callable(fnc):
            return _savecall()
        return _savecall

    def __repr__(self):
        return f"{type(self._object)}: {self.getName()}"


def _proxitise(element):
    import java
    if isinstance(element, java.awt.Component):
        return Proxy(element)
    return element
