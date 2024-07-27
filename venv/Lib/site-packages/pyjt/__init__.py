# flake8: noqa: F401
import os
import importlib
import jpype
import jpype.imports

def start(classpath=None):
    """ Start the JVM.

        Args:
            classpath (string):
                If set, use this classpath for the JVM, otherwise
                use CLASSPATH environment variable.

        Needs to be called before using pyjt. Only after starting
        the jvm you can import java classes using:

        .. code:: python
            import javax
            from java.awt import Component
    """
    cp = os.environ.get('CLASSPATH', '') if classpath is None else classpath
    jpype.startJVM(jpype.getDefaultJVMPath(), f"-Djava.class.path={cp}")

def stop():
    """ Stop the JVM. """
    jpype.shutdownJVM()



def run(app, args=[""]):
    """ Run the main function of **app**.

        This helper function will start the **app** by invoking it's
        "main" function.

        Args:
            app (string):      The application to be started, e.g. ``myapp.Application``
            args (string[]):   The arguments for the main function

        Note:

            You can as well start your application manually, assuming
            your application is in MyApplication.java, the could would look
            like:

            .. code:: python

                import MyApplication
                MyApplication.main()
    """
    module = importlib.import_module(app)
    module.main(args)

def shutdown():
    """ Shuts down pyjt and the JVM. """
    jpype.shutdownJVM()

from .Proxy import Proxy
from .Robot import Robot
from .Frame import Frame, FrameFinder
from .Fixture import Fixture, FillMode
from .Errors import ElementNotFoundError
from .ComponentFinder import Locator
from .Inspector import Inspector
from .Errors import ElementNotFoundError
