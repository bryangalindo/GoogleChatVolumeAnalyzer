import utils as u


_NULL = None
BLANK_STRING = ''
EMPTY_NESTED_LIST = [[],[]]
EMPTY_LIST = []
THREAD_ID = 'Test'
THREADS = [["Test 2"], ["Test 2"]]

class TestIsFirstResponderFunction:
    def test_null_thread_list(self):
        assert u.is_first_responder(THREAD_ID, _NULL) == None
    
    def test_blank_string_thread_list(self):
        assert u.is_first_responder(THREAD_ID, BLANK_STRING) == None
        
    def test_null_thread_id(self):
        assert u.is_first_responder(_NULL, THREADS) == None
        
    def test_blank_thread_id(self):
        assert u.is_first_responder(BLANK_STRING, THREADS) == None
        
    def test_empty_nested_thread_list(self):
        assert u.is_first_responder(THREAD_ID, EMPTY_NESTED_LIST) == None
        
    def test_empty_thread_list(self):
        assert u.is_first_responder(THREAD_ID, EMPTY_NESTED_LIST) == None
        
        
    
