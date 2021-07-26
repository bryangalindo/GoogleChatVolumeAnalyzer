import pytest 
from common import helpers


_STRING = "Test"
_NULL = None
_INT = 6
EMPTY_LIST = []
EMPTY_STRING = ''
NESTED_LIST = [["Test 1"], ["Test 2"]]

class TestCreateValuesDictFunction:
    def test_valid_values(self):
        _dict = helpers.create_values_dict(_STRING)
        assert _dict == {'values': _STRING}
        
    def test_null_value(self):
        _dict = helpers.create_values_dict(_NULL)
        assert _dict == {'values': _NULL}
        
    def test_blank_value(self):
        _dict = helpers.create_values_dict(EMPTY_STRING)
        assert _dict == {'values': EMPTY_STRING}

class TestFlattenListFunction:
    def test_valid_list(self):
        assert helpers.flatten_list(NESTED_LIST) == ["Test 1", "Test 2"]
    
    def test_null_value(self):
        assert helpers.flatten_list(_NULL) == _NULL
        
    def test_empty_string(self):
        assert helpers.flatten_list(EMPTY_STRING) == _NULL
        
    def test_int_value(self):
        with pytest.raises(TypeError):
            helpers.flatten_list(_INT)
    
    def test_empty_list(self):
        assert helpers.flatten_list(EMPTY_LIST) == _NULL