import json
import boto3
from datetime import datetime, timedelta

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('user-activity')

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])

        user_id = body.get('user_id')
        event_type = body.get('event_type')
        metadata = body.get('metadata', {})

        if not user_id or not event_type:
            return {
                'statusCode': 400,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': 'Missing required fields'})
            }

        timestamp = datetime.utcnow().isoformat()
        ttl = int((datetime.utcnow() + timedelta(days=30)).timestamp())

        item = {
            'user_id': user_id,
            'timestamp': timestamp,
            'event_type': event_type,
            'metadata': metadata,
            'ttl': ttl
        }

        table.put_item(Item=item)
        print(json.dumps({
        "event_type": event_type,
        "user_id": user_id,
        "timestamp": timestamp,
        "status": "SUCCESS"
    }))

        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'message': 'Event stored'})
        }

    except Exception as e:
        print(json.dumps({
        "status": "ERROR",
        "error": str(e)
    }))
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps(str(e))
        }