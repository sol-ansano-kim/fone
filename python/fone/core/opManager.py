import os
import re
import inspect
import importlib.util
from . import op


RE_PY = re.compile(r"\.py$", re.IGNORECASE)


class FoneOpManager(object):
    __INSTANCE = None

    def __new__(self):
        if FoneOpManager.__INSTANCE is None:
            FoneOpManager.__INSTANCE = super(FoneOpManager, self).__new__(self)
            FoneOpManager.__INSTANCE.__initialize()

        return FoneOpManager.__INSTANCE

    def __init__(self):
        super(FoneOpManager, self).__init__()

    def __initialize(self):
        self.__plugins = {}
        self.reloadPlugins()

    def reloadPlugins(self):
        for path in os.environ.get("FONE_PLUGIN_PATH", "").split(os.pathsep):
            if not path:
                continue

            path = os.path.normpath(os.path.abspath(path))

            if not os.path.isdir(path):
                continue

            for f in os.listdir(path):
                fp = os.path.join(path, f)
                fp = os.path.normpath(os.path.abspath(fp))
                if not os.path.isfile(fp):
                    continue

                if not RE_PY.search(f):
                    continue

                mdl = None
                try:
                    spec = importlib.util.spec_from_file_location(f"_fone_plugin{os.path.splitext(f)[0]}", fp)
                    mdl = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mdl)
                except Exception as e:
                    traceback.print_exc()
                    print(f"WARNING : Failed to load the file {fp}")

                if not mdl:
                    continue

                classes = inspect.getmembers(mdl, inspect.isclass)
                classes = [x[1] for x in classes if issubclass(x[1], op.FoneOp) and x[1] != op.FoneOp]
                for cls in classes:
                    if cls.type() in self.__plugins:
                        print(f"WARNING : {cls.type()} is registered already, ignore {fp}")
                        continue

                    self.__plugins[cls.type()] = cls
