"""Load a PEP 517 backend from inside the source tree.
"""
import importlib
import os
import pytoml
import sys

__version__ = '1.0'

# Ensure that the cwd is on sys.path
if sys.path[:1] != ['']:
    sys.path.insert(0, '')

def _module_from_cwd(modname):
    mod = importlib.import_module(modname)
    mod_file = os.path.realpath(mod)
    if not mod_file.startswith(os.path.realpath(os.getcwd())):
        raise ImportError('{} not found in working directory', modname)
    return mod


def _load_real_backend():
    with open('pyproject.toml') as f:
        proj = pytoml.load(f)

    ref = proj['tool']['intreehooks']['build-backend']

    modname, separator, qualname = ref.partition(':')
    obj = _module_from_cwd(modname)
    if separator:
        for attr in qualname.split('.'):
            obj = getattr(obj, attr)

    return obj

def build_wheel(wheel_directory, config_settings=None, metadata_directory=None):
    return _load_real_backend().build_wheel(
        wheel_directory, config_settings, metadata_directory)

def get_requires_for_build_wheel(config_settings=None):
    return _load_real_backend().get_requires_for_build_sdist(config_settings)

def prepare_metadata_for_build_wheel(metadata_directory, config_settings=None):
    return _load_real_backend().prepare_metadata_for_build_wheel(
        metadata_directory, config_settings)

def build_sdist(sdist_directory, config_settings=None):
    return _load_real_backend().build_sdist(sdist_directory, config_settings)

def get_requires_for_build_sdist(config_settings=None):
    return _load_real_backend().get_requires_for_build_sdist(config_settings)
