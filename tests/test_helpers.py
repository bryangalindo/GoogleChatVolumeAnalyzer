import pytest 

from common import helpers


class TestCreateValuesDictFunction:
    def test_valid_values(self):
        _dict = helpers.create_values_dict("Test")
        assert _dict == {'values': "Test"}
        
    def test_null_value(self):
        _dict = helpers.create_values_dict(None)
        assert _dict == {'values': None}
        
    def test_blank_value(self):
        _dict = helpers.create_values_dict('')
        assert _dict == {'values': ''}

class TestFlattenListFunction:
    def test_valid_list(self):
        _list = [["Test 1"], ["Test 2"]]
        assert helpers.flatten_list(_list) == ["Test 1", "Test 2"]
    
    def test_null_value(self):
        assert helpers.flatten_list(None) == None
        
    def test_empty_string(self):
        assert helpers.flatten_list('') == None
        
    def test_int_value(self):
        with pytest.raises(TypeError):
            helpers.flatten_list(6)
    
    def test_empty_list(self):
        assert helpers.flatten_list([]) == None