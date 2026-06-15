import os
import boto3
from botocore.config import Config
from flask import Flask, render_template

app = Flask(__name__)

def get_spaces_client():
    return boto3.client(
        's3',
        endpoint_url=os.environ.get('SPACES_ENDPOINT'),
        aws_access_key_id=os.environ.get('SPACES_KEY'),
        aws_secret_access_key=os.environ.get('SPACES_SECRET'),
        config=Config(signature_version='s3v4')
    )

@app.route("/")
def hello_world():
    image_url = None
    error = None
    try:
        client = get_spaces_client()
        bucket = os.environ.get('SPACES_BUCKET', 'nfs-app-test')
        image_url = client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket, 'Key': 'images (1).jpeg'},
            ExpiresIn=3600
        )
    except Exception as e:
        error = str(e)
    return render_template("index.html", image_url=image_url, error=error)
