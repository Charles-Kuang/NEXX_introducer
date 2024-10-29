import requests
import json

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


#cid = ""
#while True:
#    input_query = input()
#    answer, cid = NEXX_introducer_response(input_query, conversation_id=cid)
#    print(answer)
#    print()

#NEXX_image_upload("https://example.com", "This is a simple test.")