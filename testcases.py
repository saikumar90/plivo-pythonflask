"""
Filename: testcases.py
Description: Testcases to cover all the requirements of application
Date Created: 27/01/2017
User: Saikumar
"""

import os
import plivo_app
import unittest
import tempfile
import json
import time
import redis

class TestCase(unittest.TestCase):
    def setUp(self):
	    plivo_app.app.testing = True
	    self.app = plivo_app.app.test_client()

    """ From data invalid case"""
    def test_1(self):
	    r = redis.Redis(host='localhost',port=6379)
	    r.flushall()
	    d = {"username":"plivo1","password":"20S0KPNOIM"}
	    rv = self.app.post('/login',data=json.dumps(d),content_type='application/json')
	    print rv.data
	    d = {"from":"4924","to":"4924195509029","text":"hello"}
	    rv = self.app.post('/inbound',data=json.dumps(d),content_type='application/json')
	    print rv.data

    """ To data invalid case"""
    def test_2(self):
	    r = redis.Redis(host='localhost',port=6379)
	    r.flushall()
	    d = {"username":"plivo1","password":"20S0KPNOIM"}
	    rv = self.app.post('/login',data=json.dumps(d),content_type='application/json')
	    print rv.data
	    d = {"from":"4924195509198","to":"49241955090291234567","text":"hello"}
	    rv = self.app.post('/inbound',data=json.dumps(d),content_type='application/json')
	    print rv.data

    """ Text data invalid case"""
    def test_3(self):
	    r = redis.Redis(host='localhost',port=6379)
	    r.flushall()
	    d = {"username":"plivo1","password":"20S0KPNOIM"}
	    rv = self.app.post('/login',data=json.dumps(d),content_type='application/json')
	    print rv.data
	    d = {"from":"4924195509198","to":"4924195509029","text":"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"}
	    rv = self.app.post('/inbound',data=json.dumps(d),content_type='application/json')
	    print rv.data

    """From data not present"""
    def test_4(self):
	    r = redis.Redis(host='localhost',port=6379)
	    r.flushall()
	    d = {"username":"plivo1","password":"20S0KPNOIM"}
	    rv = self.app.post('/login',data=json.dumps(d),content_type='application/json')
	    print rv.data
	    d = {"from":"","to":"4924195509029","text":"hello"}
	    rv = self.app.post('/inbound',data=json.dumps(d),content_type='application/json')
	    print rv.data

    """To data not present"""
    def test_5(self):
	    r = redis.Redis(host='localhost',port=6379)
	    r.flushall()
	    d = {"username":"plivo1","password":"20S0KPNOIM"}
	    rv = self.app.post('/login',data=json.dumps(d),content_type='application/json')
	    print rv.data
	    d = {"from":"4924195509029","to":"","text":"hello"}
	    rv = self.app.post('/inbound',data=json.dumps(d),content_type='application/json')
	    print rv.data

    """Text data not present"""
    def test_6(self):
	    r = redis.Redis(host='localhost',port=6379)
	    r.flushall()
	    d = {"username":"plivo1","password":"20S0KPNOIM"}
	    rv = self.app.post('/login',data=json.dumps(d),content_type='application/json')
	    print rv.data
	    d = {"from":"4924195509029","to":"4924195509029","text":""}
	    rv = self.app.post('/inbound',data=json.dumps(d),content_type='application/json')
	    print rv.data
		
    """Authentication Fail """	
    def test_7(self):
	    r = redis.Redis(host='localhost',port=6379)
	    r.flushall()
	    d = {"username":"plivo6","password":"20S0KPNOIM"}
	    rv = self.app.post('/login',data=json.dumps(d),content_type='application/json')
	    print rv.data
	    d = {"username":"plivo1","password":"20S0KPNOI"}
	    rv = self.app.post('/login',data=json.dumps(d),content_type='application/json')
	    print rv.data
						
    """Proper inbound message"""
    def test_8(self):
	    r = redis.Redis(host='localhost',port=6379)
	    r.flushall()
	    d = {"username":"plivo1","password":"20S0KPNOIM"}
	    rv = self.app.post('/login',data=json.dumps(d),content_type='application/json')
	    print rv.data
	    d = {"from":"4924195509198","to":"4924195509196","text":"Hello"}
	    rv = self.app.post('/inbound',data=json.dumps(d),content_type='application/json')
	    print rv.data
		
    """To data not present in database in case of inbound message"""
    def test_9(self):
	    r = redis.Redis(host='localhost',port=6379)
	    r.flushall()
	    d = {"username":"plivo1","password":"20S0KPNOIM"}
	    rv = self.app.post('/login',data=json.dumps(d),content_type='application/json')
	    print rv.data
	    d = {"from":"4924195509198","to":"14152243533","text":"Hello"}
	    rv = self.app.post('/inbound',data=json.dumps(d),content_type='application/json')
	    print rv.data

    """Text containing STOP in inbound message followed by outbound message with same from and to data within 4 hours"""
    def test_10(self):
	    d = {"username":"plivo1","password":"20S0KPNOIM"}
	    rv = self.app.post('/login',data=json.dumps(d),content_type='application/json')
	    print rv.data
	    d = {"from":"4924195509198","to":"4924195509196","text":"STOP"}
	    rv = self.app.post('/inbound',data=json.dumps(d),content_type='application/json')
	    print rv.data
	    d = {"from":"4924195509198","to":"4924195509196","text":"hello"}
	    rv = self.app.post('/outbound',data=json.dumps(d),content_type='application/json')
	    print rv.data

    """Text containing STOP in inbound message followed by outbound message with same from and to data after 4 hours"""
    def test_11(self):
	    d = {"username":"plivo1","password":"20S0KPNOIM"}
	    rv = self.app.post('/login',data=json.dumps(d),content_type='application/json')
	    print rv.data
	    d = {"from":"4924195509198","to":"4924195509196","text":"STOP"}
	    rv = self.app.post('/inbound',data=json.dumps(d),content_type='application/json')
	    print rv.data
	    time.sleep(10)
	    d = {"from":"4924195509198","to":"4924195509196","text":"hello"}
	    rv = self.app.post('/outbound',data=json.dumps(d),content_type='application/json')
	    print rv.data		

    """ From data invalid case Outbound message"""
    def test_12(self):
	    r = redis.Redis(host='localhost',port=6379)
	    r.flushall()
	    d = {"username":"plivo1","password":"20S0KPNOIM"}
	    rv = self.app.post('/login',data=json.dumps(d),content_type='application/json')
	    print rv.data
	    d = {"from":"4924","to":"4924195509029","text":"hello"}
	    rv = self.app.post('/outbound',data=json.dumps(d),content_type='application/json')
	    print rv.data

    """ To data invalid case Outbound message"""
    def test_13(self):
	    r = redis.Redis(host='localhost',port=6379)
	    r.flushall()
	    d = {"username":"plivo1","password":"20S0KPNOIM"}
	    rv = self.app.post('/login',data=json.dumps(d),content_type='application/json')
	    print rv.data
	    d = {"from":"4924195509198","to":"49241955090291234567","text":"hello"}
	    rv = self.app.post('/outbound',data=json.dumps(d),content_type='application/json')
	    print rv.data

    """ Text data invalid case Outbound message"""
    def test_14(self):
	    r = redis.Redis(host='localhost',port=6379)
	    r.flushall()
	    d = {"username":"plivo1","password":"20S0KPNOIM"}
	    rv = self.app.post('/login',data=json.dumps(d),content_type='application/json')
	    print rv.data
	    d = {"from":"4924195509198","to":"4924195509029","text":"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"}
	    rv = self.app.post('/outbound',data=json.dumps(d),content_type='application/json')
	    print rv.data

    """From data not present Outbound message"""
    def test_15(self):
	    r = redis.Redis(host='localhost',port=6379)
	    r.flushall()
	    d = {"username":"plivo1","password":"20S0KPNOIM"}
	    rv = self.app.post('/login',data=json.dumps(d),content_type='application/json')
	    print rv.data
	    d = {"from":"","to":"4924195509029","text":"hello"}
	    rv = self.app.post('/outbound',data=json.dumps(d),content_type='application/json')
	    print rv.data

    """To data not present Outbound message"""
    def test_16(self):
	    r = redis.Redis(host='localhost',port=6379)
	    r.flushall()
	    d = {"username":"plivo1","password":"20S0KPNOIM"}
	    rv = self.app.post('/login',data=json.dumps(d),content_type='application/json')
	    print rv.data
	    d = {"from":"4924195509029","to":"","text":"hello"}
	    rv = self.app.post('/outbound',data=json.dumps(d),content_type='application/json')
	    print rv.data

    """Text data not present Outbound message"""
    def test_17(self):
	    r = redis.Redis(host='localhost',port=6379)
	    r.flushall()
	    d = {"username":"plivo1","password":"20S0KPNOIM"}
	    rv = self.app.post('/login',data=json.dumps(d),content_type='application/json')
	    print rv.data
	    d = {"from":"4924195509029","to":"4924195509029","text":""}
	    rv = self.app.post('/outbound',data=json.dumps(d),content_type='application/json')
	    print rv.data
		
    """ Outbound sms limit increased within 24 hours"""    
    def test_18(self):
	    r = redis.Redis(host='localhost',port=6379)
	    r.flushall()
	    d = {"username":"plivo1","password":"20S0KPNOIM"}
	    rv = self.app.post('/login',data=json.dumps(d),content_type='application/json')
	    print rv.data
	    d = {"from":"4924195509198","to":"4924195509196","text":"hello"}
	    rv = self.app.post('/outbound',data=json.dumps(d),content_type='application/json')
	    print rv.data
	    d = {"from":"4924195509198","to":"4924195509196","text":"hello"}
	    rv = self.app.post('/outbound',data=json.dumps(d),content_type='application/json')
	    print rv.data
	    d = {"from":"4924195509198","to":"4924195509196","text":"hello"}
	    rv = self.app.post('/outbound',data=json.dumps(d),content_type='application/json')
	    print rv.data
	    d = {"from":"4924195509198","to":"4924195509196","text":"hello"}
	    rv = self.app.post('/outbound',data=json.dumps(d),content_type='application/json')
	    print rv.data
		
    """ Outbound sms received after 24 hours"""    
    def test_19(self):
	    r = redis.Redis(host='localhost',port=6379)
	    r.flushall()
	    d = {"username":"plivo1","password":"20S0KPNOIM"}
	    rv = self.app.post('/login',data=json.dumps(d),content_type='application/json')
	    print rv.data
	    d = {"from":"4924195509198","to":"4924195509196","text":"hello"}
	    rv = self.app.post('/outbound',data=json.dumps(d),content_type='application/json')
	    print rv.data
	    time.sleep(60)
	    d = {"from":"4924195509198","to":"4924195509196","text":"hello"}
	    rv = self.app.post('/outbound',data=json.dumps(d),content_type='application/json')
	    print rv.data

    """From data not present in database in case of outbound message"""
    def test_20(self):
	    r = redis.Redis(host='localhost',port=6379)
	    r.flushall()
	    d = {"username":"plivo1","password":"20S0KPNOIM"}
	    rv = self.app.post('/login',data=json.dumps(d),content_type='application/json')
	    print rv.data
	    d = {"from":"492419550919","to":"4924195509196","text":"Hello"}
	    rv = self.app.post('/outbound',data=json.dumps(d),content_type='application/json')
	    print rv.data

    """User not logged in , sending inbound message"""
    def test_21(self):
	    r = redis.Redis(host='localhost',port=6379)
	    r.flushall()
	    d = {"from":"4924195509198","to":"4924195509196","text":"Hello"}
	    rv = self.app.post('/inbound',data=json.dumps(d),content_type='application/json')
	    print rv.data
		
    """User not logged in , sending outbound message"""
    def test_22(self):
	    r = redis.Redis(host='localhost',port=6379)
	    r.flushall()
	    d = {"from":"4924195509198","to":"4924195509196","text":"Hello"}
	    rv = self.app.post('/outbound',data=json.dumps(d),content_type='application/json')
	    print rv.data
		
    """GET HTTP Method in case of inbound message"""
    def test_23(self):
	    r = redis.Redis(host='localhost',port=6379)
	    r.flushall()
	    d = {"username":"plivo1","password":"20S0KPNOIM"}
	    rv = self.app.post('/login',data=json.dumps(d),content_type='application/json')
	    print rv.data
	    d = {"from":"4924195509198","to":"4924195509196","text":"Hello"}
	    rv = self.app.get('/inbound',data=json.dumps(d),content_type='application/json')
	    print rv.data
if __name__ == '__main__':
    unittest.main()