import utils as u


EMPTY_NESTED_LIST = [[],[]]
THREAD_ID = 'Test'
THREADS = [["Test 2"], ["Test 2"]]

class TestIsFirstResponderFunction:
    def test_empty_thread_list():
        assert u.is_first_responder(THREAD_ID, EMPTY_NESTED_LIST) == None
