from tests.test_utils import BLANK_STRING
import pytest 
from common import helpers


_LIST = ["Test"]
_NULL = None
_INT = 6
_STRING = "Test"
ALT_STRING = "12"
EMPTY_LIST = []
EMPTY_STRING = ''
NESTED_LIST = [["Test 1"], ["Test 2"]]

class TestCreateValuesDictFunction:
    def test_valid_values(self):
        _dict = helpers.create_values_dict(_LIST)
        assert _dict == {'values': _LIST}
        
    def test_null_value(self):
        _dict = helpers.create_values_dict(_NULL)
        assert _dict == {'values': _NULL}
        
    def test_empty_string(self):
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
        
class TestStringIsUnique:
    def test_duplicate_string(self):
        assert helpers.string_is_unique(_STRING, _LIST) == False
        
    def test_unique_string(self):
        assert helpers.string_is_unique(ALT_STRING, _LIST) == True
        
    def test_empty_string(self):
        assert helpers.string_is_unique(EMPTY_STRING, _LIST) is None
        
    def test_empty_list(self):
        assert helpers.string_is_unique(_STRING, EMPTY_LIST) is None
        
    def test_null_string(self):
        assert helpers.string_is_unique(_NULL, _LIST) is None
    
    def test_null_list(self):
        assert helpers.string_is_unique(_STRING, _NULL) is None
        
    def test_null_string_null_list(self):
        assert helpers.string_is_unique(_NULL, _NULL) is None
        
    def test_empty_string_empty_string_list(self):
        assert helpers.string_is_unique(EMPTY_STRING, EMPTY_STRING) is None