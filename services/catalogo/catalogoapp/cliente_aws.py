import os
import boto3

def get_bucket():
    s3 = boto3.resource('s3', 
        region_name=os.getenv('AWS_REGION'), 
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), 
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
    )
    return s3.Bucket(os.getenv('AWS_BUCKET'))
