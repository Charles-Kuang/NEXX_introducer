import requests
import json

import subprocess
import os
import re

# Define the API endpoint
def introducer_response(input_query, conversation_id="", memory=True):
    url = 'https://api.dify.ai/v1/chat-messages'

    # Define the headers
    headers = {
        'Authorization': 'Bearer app-295j9ISWmKXV5YuXhgCRh2Hf',  # Replace {api_key} with your actual API key
        'Content-Type': 'application/json'
    }
    
    # Define the JSON payload (body)
    data = {
        "inputs": {},
        "query": input_query,
        "response_mode": "blocking",
        "conversation_id": conversation_id,
        "user": "tester",
    }

    # Send the POST request
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Print the response (status and content)
    #print(response.status_code)
    try:
        json_data = response.json()

        if response.status_code == 200:
            return json_data['answer'], json_data['conversation_id']
        else:
            return json_data['code'] + ':' + json_data['message'], ""
    except ValueError:
        print("Response is not in JSON format.")
        exit()

def image_upload(image_url, image_description, answer='', keywords=[]):
    # Define the API endpoint and parameters
    dataset_id = 'aa4b5b76-b7e5-4931-a386-7f4b022bb836'  # Replace with your actual dataset ID
    document_id = '93c13eff-53b8-4d40-a173-26b9a06e3259'
    api_key = 'dataset-R6uN5v8TUK0WlwSdeYY7Hbrw'  # Replace with your actual API key

    # Define the URL and headers
    url = f'https://api.dify.ai/v1/datasets/{dataset_id}/documents/{document_id}/segments'
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    # Define the payload
    data = {
        'segments': [
            {
                'content': f'\"Image URL\":\"{image_url}\";\"Description\":\"{image_description}\"',
                'answer': f'{answer}',
                'keywords': keywords
            }
        ]
    }

    # Send the POST request
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Print the response
    #print(response.status_code)
    #print(response.json())
    if response.status_code == 200:
        return response.status_code, ""
    else:
        return response.status_code, response.json()['code'] + ': ' + response.json()['message']

def text_upload(file, text_url):
    dataset_id = 'fea03902-9c1b-490a-8f70-5abedca8e3ef'
    api_key = 'dataset-R6uN5v8TUK0WlwSdeYY7Hbrw'

    url = f'https://api.dify.ai/v1/datasets/{dataset_id}/document/create_by_file'
    headers = {
        'Authorization': f'Bearer {api_key}',
    }

    form_data = {
        'data': '{"indexing_technique":"high_quality","process_rule":{"rules":{"pre_processing_rules":[{"id":"remove_extra_spaces","enabled":true},{"id":"remove_urls_emails","enabled":true}],"segmentation":{"separator":"###","max_tokens":500}},"mode":"custom"}}',
    }

    files={'file': text_url}
    # Make the POST request
    print(form_data)
    response = requests.post(url, headers=headers, data=form_data, files=files)
    print(response.json())
    if response.status_code == 200:
        return response.status_code, ""
    else:
        return response.status_code, response.json()['code'] + ': [' + response.json()['message'] + ']'

def text_upload_subprocess(file, content_type):
    temp_file_path = f'tmp/{file.name}'
    dataset_id = 'fea03902-9c1b-490a-8f70-5abedca8e3ef'
    api_key = 'dataset-R6uN5v8TUK0WlwSdeYY7Hbrw'
        
    with open(temp_file_path, 'wb') as f:
        f.write(file.getbuffer())

    curl_cmd = [
        'curl', 
        '--location',
        '--request', 'POST',
        f'https://api.dify.ai/v1/datasets/{dataset_id}/document/create_by_file',
        '--header', f'Authorization: Bearer {api_key}',
        '--form', 'data={"indexing_technique":"high_quality","process_rule":{"rules":{"pre_processing_rules":[{"id":"remove_extra_spaces","enabled":true},{"id":"remove_urls_emails","enabled":true}],"segmentation":{"separator":"###","max_tokens":500}},"mode":"custom"}};type='+str(content_type),
        '--form', f'file=@"{temp_file_path}"'
    ]
    
    response = subprocess.run(curl_cmd, capture_output=True, text=True)
    os.remove(temp_file_path)

    if response.returncode != 0:
        return 1, response.stderr
    else:
        return 0, ""


#cid = ""
#while True:
#    input_query = input()
#    answer, cid = NEXX_introducer_response(input_query, conversation_id=cid)
#    print(answer)
#    print()

#NEXX_image_upload("https://example.com", "This is a simple test.")