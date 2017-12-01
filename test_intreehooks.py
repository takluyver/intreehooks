import os.path as osp
import pytest

from intreehooks import HooksLoader

EXAMPLES = osp.join(osp.dirname(osp.abspath(__file__)), 'examples')

def test_good():
    loader = HooksLoader(osp.join(EXAMPLES, 'good'))
    assert loader.build_wheel('') == 'itsalie'

def test_bad():
    loader = HooksLoader(osp.join(EXAMPLES, 'bad'))
    with pytest.raises(ImportError):
        loader.build_wheel('')
