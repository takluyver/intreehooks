"""Load a PEP 517 backend from inside the source tree.
"""
from contextlib import contextmanager
import importlib
import os
import pytoml
import sys

__version__ = '1.0'

@contextmanager
def prepended_to_syspath(directory):
    sys.path.insert(0, directory)
    try:
        yield
    finally:
        sys.path.pop(0)

class HooksLoader(object):
    def __init__(self, directory):
        self.directory = directory

    def _module_from_dir(self, modname):
        with prepended_to_syspath(self.directory):
            mod = importlib.import_module(modname)
        mod_file = os.path.realpath(mod.__file__)
        if not mod_file.startswith(self.directory):
            raise ImportError('{} not found in working directory', modname)
        return mod

    @property
    def _backend(self):
        with open(os.path.join(self.directory, 'pyproject.toml')) as f:
            proj = pytoml.load(f)
        ref = proj['tool']['intreehooks']['build-backend']

        modname, separator, qualname = ref.partition(':')
        obj = self._module_from_dir(modname)
        if separator:
            for attr in qualname.split('.'):
                obj = getattr(obj, attr)

        return obj

    # Hook wrappers -----

    def build_wheel(self, wheel_directory, config_settings=None,
                    metadata_directory=None):
        return self._backend.build_wheel(
            wheel_directory, config_settings, metadata_directory)

    def get_requires_for_build_wheel(self, config_settings=None):
        return self._backend.get_requires_for_build_sdist(config_settings)

    def prepare_metadata_for_build_wheel(self, metadata_directory,
                                         config_settings=None):
        return self._backend.prepare_metadata_for_build_wheel(
            metadata_directory, config_settings)

    def build_sdist(self, sdist_directory, config_settings=None):
        return self._backend.build_sdist(sdist_directory, config_settings)

    def get_requires_for_build_sdist(self, config_settings=None):
        return self._backend.get_requires_for_build_sdist(config_settings)

loader = HooksLoader(os.path.realpath(os.getcwd()))
