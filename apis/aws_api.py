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
NEWS_FOLDER_NAME = 'nexx-news/'

# Initialize the S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    region_name=REGION
)

def sanitize_filename(filename):
    sanitized_filename = re.sub(r'[\\/:"*?<>|]+', '', filename)  # Exclude invalid characters
    if '.' in sanitized_filename:
        sanitized_filename = sanitized_filename.rsplit('.', 1)[0] + '.' + sanitized_filename.split('.')[-1]
    
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

def patched_close():
    print("good try boto3")

def upload_text_to_s3(file, content_type, bucket_name, folder_name):
    object_name = file.name
    object_name = sanitize_filename(object_name)    
    
    s3_key = folder_name + object_name

    # Save the original close function
    original_close = file.close

    # Patch the close function with ours
    file.close = patched_close

    # Upload the file to S3
    s3_client.upload_fileobj(file, bucket_name, s3_key, ExtraArgs={'ContentType': content_type})

    # Unpatch it
    file.close = original_close
    
    # Construct the URL for the uploaded image
    text_url = f"https://{bucket_name}.s3.{REGION}.amazonaws.com/{s3_key}"

    return text_url
    