import json
import boto3


def lambda_handler(event, context):

    print("MyEvent:")
    print(event)

#    mycontext = event.get("context")
#    method = mycontext.get("http-method")
    method = event['context']['http-method']

    if method == "GET":
        # todo write code...
        dynamo_client = boto3.client('dynamodb')

        im_invoiceID = event['params']['querystring']['InvoiceNo']
        print(im_invoiceID)
        response = dynamo_client.get_item(TableName='Invoices', Key={
                                          'InvoiceNo': {'N': im_invoiceID}})
        print(response['Item'])

        #myreturn = "This is the return of the get"

        return {
            'statusCode': 200,
            'body': json.dumps(response['Item'])
        }

    elif method == "POST":

        #       mystring = event['params']['querystring']['param1']
        p_record = event['body-json']
        recordstring = json.dumps(p_record)

        client = boto3.client('kinesis')
        response = client.put_record(
            StreamName='APIData',
            Data=recordstring,
            PartitionKey='string'
        )

        return {
            'statusCode': 200,
            'body': json.dumps(p_record)
        }
    else:
        return {
            'statusCode': 501,
            'body': json.dumps("Server Error")
        }
