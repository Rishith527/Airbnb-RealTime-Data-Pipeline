import json
import boto3
from datetime import datetime

s3 = boto3.client('s3')
bucket_name = 'airbnb-filtered-data-cicd'

def lambda_handler(event, context):
    for record in event['Records']:
        message = json.loads(record['body'])
        start_date = datetime.strptime(message['startDate'], "%Y-%m-%d")
        end_date = datetime.strptime(message['endDate'], "%Y-%m-%d")
        duration = (end_date - start_date).days
        
        
        if duration > 1:
            print(f"Processing booking ID: {message['bookingId']} with duration: {duration} days")
            # Write the message to S3
            s3.put_object(
                Bucket=bucket_name,
                Key=f"{message['bookingId']}.json",
                Body=json.dumps(message),
                ContentType='application/json'
            )
        else:
            print(f"Skipping booking ID: {message['bookingId']} with duration: {duration} days")
            
    return {
        'statusCode': 200,
        'body': json.dumps('Processing complete')
    }