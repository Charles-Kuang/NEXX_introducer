import boto3

import os
import re

# AWS S3 credentials
ACCESS_KEY = 'AKIA6GBMF4FAZVIUZUAZ'
SECRET_KEY = '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'
REGION = 'ap-east-1'
IMAGE_BUCKET_NAME = 'nexx-image'
IMAGE_FOLDER_NAME = 'nexx-home/'  # The folder where the file will be uploaded (ensure it ends with '/')
TEXT_BUCKET_NAME = 'nexx-text'

# Initialize the S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    region_name=REGION
)

def sanitize_filename(filename):
    # Replace spaces with underscores
    filename = filename.replace(" ", "_")
    
    # Remove all special characters except for allowed ones (like . and _)
    filename = re.sub(r'[^A-Za-z0-9._-]', '', filename)
    
    return filename

def upload_image_to_s3(image, description, bucket_name, folder_name, object_name):
    extension_name = os.path.splitext(object_name)[1].lower()[1:]
    object_name = sanitize_filename(object_name)
    # The full path to the image file in S3 (folder + filename)
    s3_key = folder_name + object_name
    
    # Upload the file to S3
    s3_client.put_object(Bucket=bucket_name, Key=s3_key, Body=image, ContentType='image/' + extension_name)

    # Upload image description as a text file (optional)
    #description_file_name = s3_key + ".txt"
    #s3_client.put_object(Body=description, Bucket=bucket_name, Key=description_file_name)

    # Construct the URL for the uploaded image
    image_url = f"https://{bucket_name}.s3.{REGION}.amazonaws.com/{s3_key}"

    return image_url

def upload_text_to_s3(text, content_type, bucket_name, folder_name, object_name):
    object_name = sanitize_filename(object_name)
    # The full path to the image file in S3 (folder + filename)
    s3_key = folder_name + object_name
    
    # Upload the file to S3
    s3_client.put_object(Bucket=bucket_name, Key=s3_key, Body=image, ContentType=content_type)

    # Upload image description as a text file (optional)
    #description_file_name = s3_key + ".txt"
    #s3_client.put_object(Body=description, Bucket=bucket_name, Key=description_file_name)

    # Construct the URL for the uploaded image
    image_url = f"https://{bucket_name}.s3.{REGION}.amazonaws.com/{s3_key}"

    return image_url
    