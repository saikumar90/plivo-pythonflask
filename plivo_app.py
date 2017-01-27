"""
Filename: plivo_app.py
Description: Basic user authentication.
			 Handling inbound sms api
			 Handling outbound sms api
Date Created: 27/01/2017
User: Saikumar
"""

#!flask/bin/python
from flask import Flask, jsonify,request
import json,psycopg2,redis,datetime,ast

app = Flask(__name__)

""" 
    Login method to handle authentication
    Fetches username and password sent in POST HTTP method by client
    Authenticate againist the data stored in account table in database
    Store the client id in redis for session management
    Return appropriate response based on authentication status	
"""
@app.route('/login', methods=['POST'])
def login():
    """Fetch username and password from post message"""
    username = request.json['username']
    password = request.json['password']
	
    try:
	    """ In the below connect statement change the arguments appropriately based on database values"""
	    conn = psycopg2.connect(database="plivo", user="postgres", password="saikumar90", host="127.0.0.1", port="5432")
    except psycopg2.Error as e:
	    print "DB Connect Error " + e
    cur = conn.cursor()
    try:
	    """ plivo_schema is the schema and account is the table name containing username column"""
	    cur.execute("SELECT * from plivo_schema.account where username= '%s'" %username)
    except psycopg2.Error as e:
	    print "Query Execute Error "+ e
    rows = cur.fetchall() #fetch query results
    user_data = ()
    for row in rows:
	    user_data = row
    """ Case when username is invalid"""
    if len(rows) == 0:
	    result = {"User":username,"status":"invalid username"}
	    return jsonify({'status':result}),403

    else:
	    """ Case when password is valid"""
	    if user_data[1] == password:
		    result={"User":username,"status":"authentication success"}
		    try:
			    r = redis.Redis(host='localhost',port=6379)
		    except Exception:
			    print "Redis Connect Error"
		    r.set('id',user_data[0])
		    return jsonify({'status':result})
	    else:
		    result={"User":username,"status":"authentication failed"}
		    return jsonify({'status':result}),403

"""
    Inboud method to handle inbound sms recieved from client using POST HTTP method.
	Processess input validation of inbound data.
	Frames appropriate result based on the requirement and responds the data back to client.
"""
@app.route('/inbound',methods=['POST'])
def inbound():
    """ Fethes inbound input parameters from POST method"""
    from_data = request.json['from']
    to_data = request.json['to']
    text_data = request.json['text']
    flag = "valid" # flag to validate the input data
    """ Case when from_data is not present"""
    if len(from_data) == 0:
	    json_message = {"message":"",
		                "error":"from data is missing"}
	    flag = "invalid"

    elif len(to_data) == 0: #Case when to_data is not present#
	    json_message = {"message":"",
					    "error":"to data is missing"}
	    flag = "invalid"

    elif len(text_data) == 0:#Case when text_data is not present
	    json_message = {"message":"",
		                "error":"text data is missing"}
	    flag = "invalid"

    elif len(from_data) < 6 or len(from_data) > 16: #""" Case when from_data is invalid"""
        json_message = {"message":"",
		                "error":"from data is invalid"}
        flag = "invalid"

    elif len(to_data) < 6 or len(to_data) > 16:    #""" Case when to_data is invalid"""
        json_message = {"message":"",
		                "error":"to data is invalid"}	
        flag = "invalid"

    elif len(text_data) < 1 or len(text_data) > 120 : #    """ Case when text_data is invalid"""
        json_message = {"message":"",
		                "error":"text data is invalid"}
        flag = "invalid"
    else:
	    try:
		    r = redis.Redis(host='localhost',port=6379)
	    except Exception:
		    print "Redis connect error"
	    try:
		    conn = psycopg2.connect(database="plivo", user="postgres", password="saikumar90", host="127.0.0.1", port="5432")
	    except psycopg2.Error as e:
		    print "DB connect Error "+e
	    cur = conn.cursor()
	    query=("SELECT * from plivo_schema.phone_number where number = %s and account_id = %s ")
	    id = r.get('id')
	    """ Case when the client tries to bypass login and send inbound message """
	    if id is None:
		    json_message = {"message":"",
						    "error":"user not logged in"}
		    flag = "invalid"
	    else:
		    args=(to_data,id)
		    try:
			    cur.execute(query,args)
		    except psycopg2.Error as e:
			    print "Query Execute Error "+e
		    rows = cur.fetchall()
		    """ Case when to data is not present in database"""
		    if len(rows) == 0:
			    flag = "invalid"
			    json_message = {"message":"",
							    "error":"to parameter not found"}
		    else:
			    """ Case when client sends STOP in text_data"""
			    if text_data == "STOP":
				    data = {"from_data":from_data,"to_data":to_data,"time":str(datetime.datetime.now())}
				    r.rpush("stop_list",data)
				

    """Case when the message is valid"""
    if flag is "valid":
        json_message = {"message":"inbound sms ok",
		                "error":""}
		
    
    message = json.dumps(json_message) #dump the response in json format						
    return message

"""
    Outbound method to handle outbound sms recieved from client using POST HTTP method.
	Processess input validation of outbound data.
	Frames appropriate result based on the requirement and responds the data back to client.
"""
@app.route('/outbound',methods=['POST'])
def outbound():
    """ Fethes outbound input parameters from POST method"""
    from_data = request.json['from']
    to_data = request.json['to']
    text_data = request.json['text']
    """ flag to validate outbound input parameters"""
    flag = "valid"
    """ Case when from_data is not present"""
    if len(from_data) == 0:
	    json_message = {"message":"",
		                "error":"from data is missing"}
	    flag = "invalid"

    elif len(to_data) == 0: #    """ Case when to_data is not present"""
	    json_message = {"message":"",
		                "error":"to data is missing"}
	    flag = "invalid"

    elif len(text_data) == 0: #    """ Case text from_data is not present"""
	    json_message = {"message":"",
		                "error":"text data is missing"}
	    flag = "invalid"

    elif len(from_data) < 6 or len(from_data) > 16: #    """ Case when from_data is invalid"""
        json_message = {"message":"",
		                "error":"from data is invalid"}
        flag = "invalid"

    elif len(to_data) < 6 or len(to_data) > 16: #    """ Case when to_data is invalid"""
        json_message = {"message":"",
		                "error":"to data is invalid"}	
        flag = "invalid"

    elif len(text_data) < 1 or len(text_data) > 120 : #    """ Case when text_data is invalid"""
        json_message = {"message":"",
		                "error":"text data is invalid"}
        flag = "invalid"
    else:
	    try:
		    r = redis.Redis(host='localhost',port=6379)
	    except Exception:
		    print "redis connect error"
	    try:
		    conn = psycopg2.connect(database="plivo", user="postgres", password="saikumar90", host="127.0.0.1", port="5432")
	    except psycopg2.Error as e:
		    print "DB connect error "+e
	    cur = conn.cursor()
	    query=("SELECT * from plivo_schema.phone_number where number = %s and account_id = %s ")
	    id = r.get('id')
	    """ Case when client by passes login and sends outbound sms"""
	    if id is None:
		    json_message = {"message":"",
						    "error":"user not logged in"}
		    flag = "invalid"
	    else:
		    args=(from_data,id)
		    try:
			    cur.execute(query,args)
		    except psycopg2.Error as e:
			    print "Query execute error "+e
		    rows = cur.fetchall()
		    """ Case when from data not present in database"""
		    if len(rows) == 0:
			    flag = "invalid"
			    json_message = {"message":"",
							    "error":"from parameter not found"}
		    else:
			    current_stop_data = r.lrange('stop_list',0,len('stop_list'))
			    """ Case when atleast one pair of from and to is present containing STOP as text"""
			    if len(current_stop_data) != 0:
				    for i in range(len(current_stop_data)):
					    temp_data = ast.literal_eval(current_stop_data[i])
					    stored_from_data = temp_data["from_data"]
					    stored_to_data = temp_data["to_data"]
					    """Case when the requested from data is same as stored in redis"""
					    if from_data == stored_from_data and to_data == stored_to_data:
						    stored_time = datetime.datetime.strptime(temp_data["time"],"%Y-%m-%d %H:%M:%S.%f")
						    current_time = datetime.datetime.now()
						    difference_time = (current_time - stored_time).total_seconds() / 3600
						    """ Case when the client sends outbound sms where from data is stored in redis and within 4 hours"""
						    if difference_time < 4:
							    json_message = {"message":"",
											    "error":"sms from " + from_data + " to " + to_data + " blocked by user"}
							    flag = "invalid"
						
						    else: #    """ Case when the client sends outbound sms where from data is stored in redis and after 4 hours so delete the entry from redis"""
							    r.lrem('stop_list',current_stop_data[i])

    """case when outbound message is valid"""	
    if flag is "valid":
	    try:
		    r = redis.Redis(host='localhost',port=6379)
	    except Exception:
		    print "Redis connect error"
	    stored_counter_data = r.lrange('counter_list',0,len('counter_list'))
	    """ Case when the from data is received first time in outbound sms"""
	    if len(stored_counter_data) == 0:
		    data = {"from_data":from_data,"counter":1,"time":str(datetime.datetime.now())}
		    r.rpush('counter_list',data)
		    json_message = {"message":"outbound sms ok",
		                    "error":""}
	    else:
		    for i in range(len(stored_counter_data)):
			    temp_data = ast.literal_eval(stored_counter_data[i])
			    stored_from_data = temp_data["from_data"]
			    """ case when the from data is not received first time in outbound sms"""
			    if stored_from_data == from_data:
				    current_time = datetime.datetime.now()
				    stored_time = datetime.datetime.strptime(temp_data["time"],"%Y-%m-%d %H:%M:%S.%f")	
				    difference_time = (current_time - stored_time).total_seconds() / 3600
				    """ Case when the from data is received within 24 hours"""
				    if difference_time < 24:
					    stored_counter =  temp_data["counter"]
					    """ case when the limit of outbound sms is within 50"""
					    if int(stored_counter) < 50:
						    json_message = {"message":"outbound sms ok",
										    "error":""}
						    temp_data["counter"] = int(temp_data["counter"]) + 1
						    r.lset('counter_list',i,temp_data)
					    else:
						    json_message = {"message":"",
										    "error":"limit reached from "+ from_data}
				    else:
					    json_message = {"message":"outbound sms ok",
									    "error":""}
					    temp_data["counter"] = 1
					    r.lset('counter_list',i,temp_data)

					
    message = json.dumps(json_message)						
    return message
if __name__ == '__main__':
    app.run(debug=True)