from __future__ import print_function

import base64
# We need base64 as the messages from Kinesis are base64 encoded
import json
# boto3 to connect to S3
import boto3
from datetime import datetime

# Creating a boto3 Client for S3
s3_client = boto3.client('s3')

# Converting datetime object to string
dateTimeObj = datetime.now()

# formatting the string
timestampStr = dateTimeObj.strftime("%d-%b-%Y-%H%M%S")

# Creating a list for Kinesis records
kinesisRecords = []

# Function to process the incoming events from Kinesis or lines of data
# I chose when setting up the Lambda Function


def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))
    for record in event['Records']:
        # Kinesis data is base64 encoded so here we encode it.
        # If running into the error: [ERROR] TypeError: sequence item 0: expected str instance, bytes found
        # then we add the encoding into UTF8:
        payload = base64.b64decode(record['kinesis']['data']).decode('utf-8')
        #payload = base64.b64decode(record['kinesis']['data'])

        # appending each record to a list
        kinesisRecords.append(payload)
        # this is just for logging
        # print("Decoded payload: " + payload)

    # making a string out of the list. Backslash n for new line in the s3 file
    ex_string = '\n'.join(kinesisRecords)

    # generate the name for the file with the timestamp
    mykey = 'output-' + timestampStr + '.txt'

    # putting the file into the s3 bucket
    response = s3_client.put_object(
        Body=ex_string, Bucket='stream-data-lake', Key=mykey)
    # returning how many records have been processed within the function
    return 'Successfully processed {} records.'.format(len(event['Records']))
