'''
Tests core functionality for dumping and loading sliced pickles.
'''

import pickleslicer
import pytest

def test_simple(tmp_path):
    test_base_filename = tmp_path / 'test.pickle'

    obj = []
    pickleslicer.dump(obj, test_base_filename)
    unpickled = pickleslicer.load(test_base_filename)
    assert obj == unpickled

    obj = [i for i in range(1000)]
    pickleslicer.dump(obj, test_base_filename, max_size=32)
    unpickled = pickleslicer.load(test_base_filename)
    assert obj == unpickled

def test_dump_errors(tmp_path):
    test_base_filename = tmp_path / 'test.pickle'

    obj = []
    with pytest.raises(TypeError):
        # obj cannot be None
        pickleslicer.dump(None, test_base_filename)
    with pytest.raises(TypeError):
        # max_size must be an integer
        pickleslicer.dump(obj, test_base_filename, max_size=1.234)
    with pytest.raises(ValueError):
        # base_filename cannot be empty string
        pickleslicer.dump(obj, '')
    with pytest.raises(ValueError):
        # max_size must be positive
        pickleslicer.dump(obj, test_base_filename, max_size=-10)

def test_load_errors(tmp_path):
    test_base_filename = tmp_path / 'test.pickle.missing'

    with pytest.raises(ValueError):
        # base_filename cannot be empty string
        pickleslicer.load('')
    with pytest.raises(FileNotFoundError):
        # base_filename must have existing sliced pickles
        pickleslicer.load(test_base_filename)
