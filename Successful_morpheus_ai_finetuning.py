# -*- coding: utf-8 -*-
"""Morpheus AI Finetuning.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/19A0dyE4miTXpvpN0RnajN91qUp__hsnn
"""

!pip install requests tqdm tenacity mistralai

import os
import requests
import time
import json
from getpass import getpass
from tqdm import tqdm
from google.colab import files

# Securely input your API key
api_key = getpass("Enter your Mistral AI API key: ")
os.environ['MISTRAL_API_KEY'] = api_key

def api_request(method, endpoint, **kwargs):
    url = f"https://api.mistral.ai/v1/{endpoint}"
    headers = {"Authorization": f"Bearer {os.environ['MISTRAL_API_KEY']}"}
    try:
        print(f"Making {method} request to {endpoint}")
        response = requests.request(method, url, headers=headers, **kwargs)
        response.raise_for_status()
        print(f"Successful {method} request to {endpoint}")
        return response.json()
    except Exception as e:
        print(f"API request failed: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response content: {e.response.text}")
        raise

def validate_jsonl(file_path):
    print(f"Validating JSONL file: {file_path}")
    valid_data = []
    with open(file_path, 'r') as f:
        for i, line in enumerate(f, 1):
            try:
                data = json.loads(line)
                if 'messages' in data and isinstance(data['messages'], list):
                    for message in data['messages']:
                        if 'role' not in message or 'content' not in message:
                            raise ValueError(f"Invalid message format in line {i}")
                        if message['role'] not in ['user', 'assistant', 'system']:
                            raise ValueError(f"Invalid role in line {i}")
                    valid_data.append(data)
                else:
                    raise ValueError(f"Missing or invalid 'messages' field in line {i}")
            except json.JSONDecodeError:
                print(f"Invalid JSON in line {i}")
            except ValueError as e:
                print(str(e))

    if not valid_data:
        raise Exception("No valid data found in the JSONL file")

    print(f"JSONL file validated successfully")
    return file_path

def upload_file():
    print("Please upload your 'morpheus_fine_tuning_data.jsonl' file.")
    try:
        uploaded = files.upload()
        uploaded_file = next((name for name in uploaded.keys() if 'morpheus_fine_tuning_data' in name), None)
        if not uploaded_file:
            raise Exception("No file containing 'morpheus_fine_tuning_data' was uploaded.")
        print(f"File '{uploaded_file}' uploaded successfully.")
        return uploaded_file
    except Exception as e:
        print(f"Error during file upload: {e}")
        raise

if __name__ == "__main__":
    try:
        # Test API connection
        try:
            models = api_request('GET', 'models')
            print(f"Successfully connected to API. Available models: {models}")
        except Exception as e:
            print(f"Failed to connect to API: {e}")
            raise

        # Upload file to Colab
        uploaded_file = upload_file()
        print(f"Uploaded file: {uploaded_file}")

        # Validate the JSONL file
        validated_file = validate_jsonl(uploaded_file)

        # Upload file to Mistral AI
        print(f"Uploading file to Mistral AI: {validated_file}")
        with open(validated_file, 'rb') as file:
            files = {
                'file': (validated_file, file, 'application/jsonl'),
                'purpose': (None, 'fine-tune')
            }
            response = api_request('POST', 'files', files=files)
            file_id = response['id']
            print(f"File uploaded successfully. File ID: {file_id}")

        # Create fine-tuning job
        print("Creating fine-tuning job...")
        payload = {
            "training_files": [file_id],
            "model": "open-mistral-7b",
            "hyperparameters": {
                "learning_rate_multiplier": 1e-5,
                "batch_size": 4
            }
        }

        # Perform a dry run to check for potential issues
        dry_run_payload = {**payload, "dry_run": True}
        dry_run_response = api_request('POST', 'fine_tuning/jobs', json=dry_run_payload)
        print(f"Dry run response: {json.dumps(dry_run_response, indent=2)}")

        # Adjust training steps based on dry run results
        n_epochs = dry_run_response.get('n_epochs', 1)
        n_train_tokens = dry_run_response.get('n_train_tokens', 1000)
        desired_epochs = min(10, 100 / n_epochs)  # Aim for 10 epochs, but don't exceed 100 total
        training_steps = max(1, int(desired_epochs * n_train_tokens / 1000))

        payload['hyperparameters']['training_steps'] = training_steps
        print(f"Adjusted training steps to {training_steps}")

        # Create the actual fine-tuning job
        job_response = api_request('POST', 'fine_tuning/jobs', json=payload)
        job_id = job_response['id']
        print(f"Fine-tuning job created successfully. Job ID: {job_id}")
        print(f"Full job creation response: {json.dumps(job_response, indent=2)}")

        # Monitor fine-tuning job
        print("Monitoring fine-tuning job...")
        start_time = time.time()
        last_log_time = start_time
        with tqdm(total=100, desc="Fine-tuning progress") as pbar:
            while True:
                try:
                    job_status = api_request('GET', f'fine_tuning/jobs/{job_id}')
                    status = job_status.get('status', '').upper()
                    progress = job_status.get('progress', {}).get('percentage_complete', 0)
                    print(f"Job status: {status} - Progress: {progress}%")
                    print(f"Full job status: {json.dumps(job_status, indent=2)}")

                    # Update progress bar
                    pbar.n = int(progress)
                    pbar.refresh()

                    elapsed_time = time.time() - start_time

                    if status in ['SUCCESS', 'FAILED', 'CANCELLED']:
                        break

                    current_time = time.time()
                    if current_time - last_log_time > 60:  # Log every minute
                        print(f"Job status: {status} - Progress: {progress}% - Elapsed time: {elapsed_time:.2f}s")
                        last_log_time = current_time

                    time.sleep(60)  # Check every minute
                except Exception as e:
                    print(f"Error checking job status: {e}")
                    time.sleep(60)  # Wait a minute before retrying in case of an error

        if status == 'SUCCESS':
            fine_tuned_model_id = job_status.get('fine_tuned_model')
            print(f"Fine-tuning job completed successfully. Fine-tuned model ID: {fine_tuned_model_id}")

            # Function to generate responses using the fine-tuned model
            def generate_morpheus_response(prompt):
                payload = {
                    "model": fine_tuned_model_id,
                    "messages": [{"role": "user", "content": prompt}]
                }
                response = api_request('POST', 'chat/completions', json=payload)
                return response['choices'][0]['message']['content']

            # Test the fine-tuned model
            test_prompt = "Hello, how are you?"
            response = generate_morpheus_response(test_prompt)
            print(f"Test prompt response: {response}")

            # Save the fine-tuned model information
            with open('fine_tuned_model_info.json', 'w') as f:
                json.dump({"fine_tuned_model_id": fine_tuned_model_id}, f)

            print("Fine-tuned model information saved successfully.")

        else:
            print(f"Fine-tuning job failed with status: {status}")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        print("Process completed.")