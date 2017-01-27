The attached application has been tested on Windows 7 OS.

Following are the post installation softwares needed to run the application:
1) Install python 2.7
2) Install Flask python module (pip install Flask)
3) Install postgresql (https://www.postgresql.org/download/windows/)
4) Install psycopg2 python module (pip install psycopg2)
5) Download redis on windows (https://redis.io/download)
6) Install redis python module (pip install redis)

-----------------------------------------------------------------------------------------------------------------------------

Once all softwares and modules are successfully installed follow the below steps post execution the testcases:

1) Download the plivo_app.py and testcases.py and make sure both are placed in same directory.
2) Create the database in postgresql and insert valid data.
   Make sure to update the following line of code in plivo_app.py at 31, 111 and 199 with your respective database details.
   (database="plivo", user="postgres", password="saikumar90", host="127.0.0.1", port="5432")
3) Start the redis-server.exe downloaded in post installation steps.
4) Run the application plivo_app.py as:
   python plivo_app.py

-----------------------------------------------------------------------------------------------------------------------------
   
Execution of testcases:

Totally 23 testcase are added. Description are added for each testcase.

1) Testcase 1: 
Client authenticated successfully
Inbound sms sent with invalid from_data.
Execution: python testcases.py TestCase.test_1
Expected output: 
{
  "status": {
    "User": "plivo1",
    "status": "authentication success"
  }
}

{"message": "", "error": "from data is invalid"}

2) TestCase 2:
Client authenticated successfully
Inbound sms sent with invalid to_data.
Execution: python testcases.py TestCase.test_2
Expected output:
{
  "status": {
    "User": "plivo1",
    "status": "authentication success"
  }
}

{"message": "", "error": "to data is invalid"}

3) TestCase 3:
Client authenticated successfully
Inbound sms sent with invalid text_data.
Execution: python testcases.py TestCase.test_3
Expected output:
{
  "status": {
    "User": "plivo1",
    "status": "authentication success"
  }
}

{"message": "", "error": "text data is invalid"}

4) TestCase 4:
Client authenticated successfully
Inbound sms sent with empty from_data.
Execution: python testcases.py TestCase.test_4
Expected output:
{
  "status": {
    "User": "plivo1",
    "status": "authentication success"
  }
}

{"message": "", "error": "from data is missing"}

5) TestCase 5:
Client authenticated successfully
Inbound sms sent with empty to_data.
Execution: python testcases.py TestCase.test_5
Expected output:
{
  "status": {
    "User": "plivo1",
    "status": "authentication success"
  }
}

{"message": "", "error": "to data is missing"}

6) TestCase 6:
Client authenticated successfully
Inbound sms sent with empty text_data.
Execution: python testcases.py TestCase.test_6
Expected output:
{
  "status": {
    "User": "plivo1",
    "status": "authentication success"
  }
}

{"message": "", "error": "text data is missing"}

7) TestCase 7:
Client Authentication Fail with invalid username and then with invalid 
Execution: python testcases.py TestCase.test_7
Expected output:
{
  "status": {
    "User": "plivo6",
    "status": "invalid username"
  }
}

{
  "status": {
    "User": "plivo1",
    "status": "authentication failed"
  }
}

8) TestCase 8:
Client authenticated successfully
Valid inbound sms sent by client
Execution: python testcases.py TestCase.test_8
Expected output:
{
  "status": {
    "User": "plivo1",
    "status": "authentication success"
  }
}

{"message": "inbound sms ok", "error": ""}

9) TestCase 9:
Client authenticated successfully
Valid inbound sms sent by client
To_data not present in database.
Execution: python testcases.py TestCase.test_9
Expected output:
{
  "status": {
    "User": "plivo1",
    "status": "authentication success"
  }
}

{"message": "", "error": "to parameter not found"}

10) TestCase 10:
Client authenticated successfully
Valid inbound sms sent by client
Text data containing STOP in inbound message followed by outbound message with same from and to data within 4 hours.
Note: In this case you need to modify the code as follows:
plivo_app.py,Line #234:
  Existing : difference_time = (current_time - stored_time).total_seconds() / 3600
  Update as: difference_time = (current_time - stored_time).total_seconds() 
The division by 3600 is removed in order to avoid waiting for 4 hours and tested with 4 seconds.

Execution: python testcases.py TestCase.test_10
Expected output:
{
  "status": {
    "User": "plivo1",
    "status": "authentication success"
  }
}

{"message": "inbound sms ok", "error": ""}
{"message": "", "error": "sms from 4924195509198 to 4924195509196 blocked by user"}

11) TestCase 11:
Client authenticated successfully
Valid inbound sms sent by client
Text data containing STOP in inbound message followed by outbound message with same from and to data after 4 hours.
But in this case the outbound sms is sent after 10 seconds as the code has to be modified as follows for testing.
Note: In this case you need to modify the code as follows:
plivo_app.py,Line #234:
  Existing : difference_time = (current_time - stored_time).total_seconds() / 3600
  Update as: difference_time = (current_time - stored_time).total_seconds() 
The division by 3600 is removed in order to avoid waiting for 4 hours and tested with 4 seconds.

Execution: python testcases.py TestCase.test_11
Expected output:
{
  "status": {
    "User": "plivo1",
    "status": "authentication success"
  }
}

{"message": "inbound sms ok", "error": ""}
{"message": "outbound sms ok", "error": ""}

12) TestCase 12:
Client authenticated successfully
Outbound sms sent with invalid from_data.
Execution: python testcases.py TestCase.test_12
Expected output: 
{
  "status": {
    "User": "plivo1",
    "status": "authentication success"
  }
}

{"message": "", "error": "from data is invalid"}

13) TestCase 13:
Client authenticated successfully
Outbound sms sent with invalid to_data.
Execution: python testcases.py TestCase.test_13
Expected output:
{
  "status": {
    "User": "plivo1",
    "status": "authentication success"
  }
}

{"message": "", "error": "to data is invalid"}

14) TestCase 14:
Client authenticated successfully
Outbound sms sent with invalid text_data.
Execution: python testcases.py TestCase.test_14
Expected output:
{
  "status": {
    "User": "plivo1",
    "status": "authentication success"
  }
}

{"message": "", "error": "text data is invalid"}

15) TestCase 15:
Client authenticated successfully
Outbound sms sent with empty from_data.
Execution: python testcases.py TestCase.test_15
Expected output:
{
  "status": {
    "User": "plivo1",
    "status": "authentication success"
  }
}

{"message": "", "error": "from data is missing"}

16) TestCase 16:
Client authenticated successfully
Outbound sms sent with empty to_data.
Execution: python testcases.py TestCase.test_16
Expected output:
{
  "status": {
    "User": "plivo1",
    "status": "authentication success"
  }
}

{"message": "", "error": "to data is missing"}

17) TestCase 17:
Client authenticated successfully
Outbound sms sent with empty text_data.
Execution: python testcases.py TestCase.test_17
Expected output:
{
  "status": {
    "User": "plivo1",
    "status": "authentication success"
  }
}

{"message": "", "error": "text data is missing"}

18) TestCase 18:
Client authenticated successfully
Valid outbound sms sent by client
4 outbound sms sent by client with same from_data.

In order to test this you need to do following changes in code.

plivo_app.py,Line #265:
  Existing : difference_time = (current_time - stored_time).total_seconds() / 3600
  Update as: difference_time = (current_time - stored_time).total_seconds() 
The division by 3600 is removed in order to avoid waiting for 24 hours and tested with 24 seconds.

plivo_app.py,Line #270:
  Existing : if int(stored_counter) < 50:
  Update as: if int(stored_counter) < 2:
The counter comparison is done with 2 in order to avoid sending 50 requests.

Execution: python testcases.py TestCase.test_18
Expected output:
{
  "status": {
    "User": "plivo1",
    "status": "authentication success"
  }
}

{"message": "outbound sms ok", "error": ""}
{"message": "outbound sms ok", "error": ""}
{"message": "", "error": "limit reached from 4924195509198"}
{"message": "", "error": "limit reached from 4924195509198"}

19) TestCase 19:
Client authenticated successfully
Valid outbound sms sent by client
2 outbound sms are sent by client with same from data.
Second one is sent after 60 seconds.

In order to test this you need to do following changes in code.

plivo_app.py,Line #265:
  Existing : difference_time = (current_time - stored_time).total_seconds() / 3600
  Update as: difference_time = (current_time - stored_time).total_seconds() 
The division by 3600 is removed in order to avoid waiting for 24 hours and tested with 24 seconds.

plivo_app.py,Line #270:
  Existing : if int(stored_counter) < 50:
  Update as: if int(stored_counter) < 2:
The counter comparison is done with 2 in order to avoid sending 50 requests.

Execution: python testcases.py TestCase.test_19
Expected output:
{
  "status": {
    "User": "plivo1",
    "status": "authentication success"
  }
}

{"message": "outbound sms ok", "error": ""}
{"message": "outbound sms ok", "error": ""}

20) TestCase 20:
Client authenticated successfully
Valid Outbound sms sent by client
From_data not present in database.
Execution: python testcases.py TestCase.test_20
Expected output:
{
  "status": {
    "User": "plivo1",
    "status": "authentication success"
  }
}

{"message": "", "error": "from parameter not found"}

21) TestCase 21:
Client not logged in.
Sending inbound sms.
Execution: python testcases.py TestCase.test_21
Expected output:
{"message": "", "error": "user not logged in"}

22) TestCase 22:
Client not logged in.
Sending outbound sms.
Execution: python testcases.py TestCase.test_22
Expected output:
{"message": "", "error": "user not logged in"}

23) TestCase 23:
Client authenticated successfully
Valid inbound sms sent by client using get method
Execution: python testcases.py TestCase.test_23
Expected output:
{
  "status": {
    "User": "plivo1",
    "status": "authentication success"
  }
}

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>405 Method Not Allowed</title>
<h1>Method Not Allowed</h1>
<p>The method is not allowed for the requested URL.</p>

------------------------------------------------------------------------------------------------------------------------------------------------------

Scope of Improvement:
Following things can be improved in the application:
1) Modularity:  The code can be moved in a class making it more modular and object oriented.
2) Session Management: Currently python-redis is used for user session management. This can be improved by using python's other better session modules.
3) Code restructure: Some lines of code are repeated which should be moved under a common method.

------------------------------------------------------------------------------------------------------------------------------------------------------

Automating testcases:

The testcases can be automated by following 2 methods:

1) Running the whole test case as follows:
   python testcases.py
   
2) Running the following command execution in any of the automation framework that accepts command line execution.
   python testcases.py
   Frameworks like:
   1) Robogalaxy
   2) ALM tool

