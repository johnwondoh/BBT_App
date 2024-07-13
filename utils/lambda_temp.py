import json
import boto3
from botocore.exceptions import ClientError
from decimal import Decimal
from boto3.dynamodb.conditions import Key

# Initialize the DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')
revenue_table = dynamodb.Table('Revenue')
asset_table = dynamodb.Table('Asset')
expense_table = dynamodb.Table('Expense')

status_check_path = '/status'
revenue_path = '/revenue'
asset_path = '/assets'
expense_path = '/expenses'


def lambda_handler(event, context):
    print('Request event: ', event)
    response = None
    # response = {'f': 's}'

    try:
        http_method = event.get('httpMethod')
        path = event.get('path')

        if http_method == 'GET' and path == status_check_path:
            response = build_response(200, 'Service is operational')
        elif http_method == 'GET' and path == revenue_path:
            response = get_all_revenue()
        elif http_method == 'GET' and path == asset_path:
            response = get_all_asset()
        elif http_method == 'GET' and path == expense_path:
            response = get_all_expense()
        else:
            response = build_response(404, '404 Not Found')
    except Exception as e:
        print('Error:', e)
        response = build_response(400, 'Error processing request')
    return response


def get_all_revenue():
    try:
        scan_params = {
            'TableName': revenue_table.name
        }
        return build_response(200, scan_dynamo_records(scan_params, [], revenue_table))
    except ClientError as e:
        print('Error:', e)
        return build_response(400, e.response['Error']['Message'])


def get_all_asset():
    try:
        scan_params = {
            'TableName': asset_table.name
        }
        return build_response(200, scan_dynamo_records(scan_params, [], asset_table))
    except ClientError as e:
        print('Error:', e)
        return build_response(400, e.response['Error']['Message'])


def get_all_expense():
    try:
        scan_params = {
            'TableName': expense_table.name
        }
        return build_response(200, scan_dynamo_records(scan_params, [], expense_table))
    except ClientError as e:
        print('Error:', e)
        return build_response(400, e.response['Error']['Message'])


# ============ support =============
def scan_dynamo_records(scan_params, item_array, table):
    response = table.scan(**scan_params)
    item_array.extend(response.get('Items', []))

    if 'LastEvaluatedKey' in response:
        scan_params['ExclusiveStartKey'] = response['LastEvaluatedKey']
        return scan_dynamo_records(scan_params, item_array)
    else:
        return {'data': item_array}


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            # Check if it's an int or a float
            if obj % 1 == 0:
                return int(obj)
            else:
                return float(obj)
        # Let the base class default method raise the TypeError
        return super(DecimalEncoder, self).default(obj)


def build_response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(body, cls=DecimalEncoder)
    }