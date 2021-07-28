import utils as u

_NULL = None
BLANK_STRING = ''
EMPTY_NESTED_LIST = [[],[]]
EMPTY_LIST = []
THREAD_ID = 'Test'
THREADS = [["Test"], ["Test"]]
ALT_THREADS = [["Test2"], ["Test2"]]
VALID_EVENT_RESPONSE_DICT = {
    'message': {'argumentText': 'Test',
    'createTime': '2021-07-27T05:50:55.079839Z',
    'sender': {'avatarUrl': 'url', 'displayName': 'Test User', 'domainId': 'domainId',
               'email': 'test@test.com', 'name': 'users/123456', 'type': 'HUMAN'},
    'space': {'displayName': 'Room Name', 'name': 'spaces/A', 
              'threaded': True,'type': 'ROOM'},
    'thread': {'name': 'spaces/A/threads/B', 'retentionSettings': {'state': 'PERMANENT'}}
    },
    }
EXPECTED_FILTERED_DICT = {
    'timestamp': '2021-07-27T05:50:55.079839Z', 'email': 'test@test.com',
    'room_id': 'A', 'thread_id': 'B', 'room_name': 'Room Name',
    'message': 'Test', 'user_id': 'users/123456',
    }
MISSING_MESSAGE_KEY_RESPONSE_DICT = {
    'missing': {'argumentText': 'Test',
    'createTime': '2021-07-27T05:50:55.079839Z',
    'sender': {'avatarUrl': 'url', 'displayName': 'Test User', 'domainId': 'domainId',
               'email': 'test@test.com', 'name': 'users/123456', 'type': 'HUMAN'},
    'space': {'displayName': 'Room Name', 'name': 'spaces/A', 
              'threaded': True,'type': 'ROOM'},
    'thread': {'name': 'spaces/A/threads/B', 'retentionSettings': {'state': 'PERMANENT'}}
    },
    }
MISSING_ALL_KEYS_RESPONSE_DICT = {
    'message': {'missing': 'Test',
    'missingTimeStamp': '2021-07-27T05:50:55.079839Z',
    'missingSender': {'avatarUrl': 'url', 'displayName': 'Test User', 'domainId': 'domainId',
               'missingEmail': 'test@test.com', 'missingSenderID': 'users/123456', 'type': 'HUMAN'},
    'space': {'missingRoomName': 'Room Name', 'name': 'spaces/A', 
              'threaded': True,'type': 'ROOM'},
    'missingThread': {'missingRoomName': 'spaces/A/threads/B', 'retentionSettings': {'state': 'PERMANENT'}}
    },
    }
EXPECTED_EMPTY_DICT = {
    'timestamp': None, 'email': None,
    'room_id': None, 'thread_id': None, 'room_name': None,
    'message': None, 'user_id': None, 
}

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
        
    def test_duplicate_thread_id(self):
        assert u.is_first_responder(THREAD_ID, THREADS) == False
        
    def test_valid_unique_thread_id(self):
        assert u.is_first_responder(THREAD_ID, ALT_THREADS) == True
        
class TestCreateFilteredDict:
    def test_valid_event_dict(self):
        assert u.create_filtered_dict(VALID_EVENT_RESPONSE_DICT) == EXPECTED_FILTERED_DICT
        
    def test_missing_message_key(self):
        assert u.create_filtered_dict(MISSING_MESSAGE_KEY_RESPONSE_DICT) is None
                
    def test_null_dict(self):
        assert u.create_filtered_dict(_NULL) is None
        
    def test_blank_string_as_dict(self):
        assert u.create_filtered_dict(BLANK_STRING) is None
        
    def test_all_missing_keys(self):
        print(u.create_filtered_dict(MISSING_ALL_KEYS_RESPONSE_DICT))
        assert u.create_filtered_dict(MISSING_ALL_KEYS_RESPONSE_DICT) == EXPECTED_EMPTY_DICT
        
        
        
        
    
