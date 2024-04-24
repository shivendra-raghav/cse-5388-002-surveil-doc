# Authors - Shivendra Raghav (1001123853)
# CSE 5388-002

# This file calls the Claude API and saves the response in a file and tracks details in a json file
# Reference - https://docs.anthropic.com/claude/reference/client-sdks
# Reference - https://www.pullrequest.com/blog/retrying-and-exponential-backoff-smart-strategies-for-robust-software/

import os
import re
import json
import time
import random
import anthropic

# Models:
# Claude 3 Haiku - claude-3-haiku-20240307
# Claude 3 Sonnet - claude-3-sonnet-20240229
# Claude 3 Opus - claude-3-opus-20240229

# Creating Claude client
client = anthropic.Anthropic(api_key="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")

# Function to call Claude with retry with backoff
def claude_message_retry_backoff(prompt, model="claude-3-sonnet-20240229", max_tokens=4096, role="user", max_retries=3, initial_delay=3):
    delay = initial_delay
    for attempt in range(max_retries):
        try:
            message = client.messages.create(
                model=model,
                max_tokens=max_tokens,
                messages=[
                    {"role": role, "content": prompt},
                ],
            )

            content_blocks = message.content
            return "\n\n".join(block.text for block in content_blocks)
        except anthropic.APIError as e:
            if e.status_code == 429:
                print(f"Rate limit exceeded. Will retry in {delay} seconds.")
                time.sleep(delay)
                delay *= 2
                delay += random.uniform(0, 1)
            else:
                raise Exception("Max retries exceeded")

def main():
    sensitive_prompt = f"""Based on the data give in the <data></data> tags, give me the updated value without tags and using the following standards:
    1. Update all details inside [] tags with sample values, these values should be realistic for example [Company Name] should be replaced by ABC Corp or some other realistic name. Similar thing should happen for other things within [] tags.
    2. Ensure that these values are context based and appropriate values are being assigned.
    3. Do not update placeholders with <> tags as these are sensitive information placeholders such as <SSN>, <PASSWORD> etc and should appeat in the response as such.
    """

    non_sensitive_prompt = f"""Based on the data give in the <data></data> tags, give me the updated value without tags and using the following standards:
    1. Update all details inside [] tags with sample values, these values should be realistic for example [Company Name] should be replaced by ABC Corp or some other realistic name. Similar thing should happen for other things within [] tags.
    2. Ensure that these values are context based and appropriate values are being assigned.
    3. Do not include any sensitive information like PII or secrets such as username, passwords, api keys etc or even placeholders for them like <access_token>, <your_password>, etc. If there are such instances, replace them with a generic phrases indicating where the actual value should be used. For example, replace usernames with "your unique username" or "####" or "****". This ensures the text is free of sensitive data (even synthetic) while maintaining the context and structure of the content.
    """

    data_dir = "../synthetic_dataset/sensitive_with_placeholders"
    response_dir = "../synthetic_dataset/processed_sensitive_with_placeholders"
    cache_file = f"{response_dir}/processed_sensitive_with_placeholders.json"

    # Read the files from the data directory
    data_files = os.listdir(data_dir)

    # Use JSON file to track the prompts and responses as a cache file
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            cache = json.load(f)
    else:
        cache = {}

    # Iterate through the prompts files and read the text from the files
    for file in data_files:
        # Check if the file is a .txt file
        if file.endswith(".txt"):
            # Check if the filename is already in the cache
            if file in cache:
                print(f"Skipping {file} as it is already processed.")
                continue

            with open(f"{data_dir}/{file}", "r") as f:
                content = f.read()

            # Check if the filename contains "_sent_"
            if "_sent_" in file:
                # Copy the file without calling claude_message_retry_backoff
                response_filename = f"{file.split('.')[0]}_not_processed.txt"
                with open(f"{response_dir}/{response_filename}", "w") as f:
                    f.write(content)
                print(f"Copied {file} to {response_filename}")
                cache[file] = [response_filename]
                with open(cache_file, "w") as f:
                    json.dump(cache, f)
                continue

            # Check if the filename contains "_prompt_"
            if "_prompt_" in file:
                # Check if the content has no [] or <> placeholders
                if not re.search(r'\[.*?\]|<.*?>', content):
                    # Copy the file without calling claude_message_retry_backoff
                    response_filename = f"{file.split('.')[0]}_not_processed.txt"
                    with open(f"{response_dir}/{response_filename}", "w") as f:
                        f.write(content)
                    print(f"Copied {file} to {response_filename}")
                    cache[file] = [response_filename]
                    with open(cache_file, "w") as f:
                        json.dump(cache, f)
                    continue

                prompt = f"{sensitive_prompt}<data>{content}</data>"

                # Check if the filename is in the cache
                if file in cache:
                    response_file_num = len(cache[file]) + 1
                else:
                    response_file_num = 1

                # Getting prompt filename without the extension
                filename = file.split(".")[0]

                # Creating response filename
                response_filename = f"{filename}_{response_file_num}.txt"

                # Call Claude with the prompt
                response = claude_message_retry_backoff(prompt)

                # Save the response in a file
                with open(f"{response_dir}/{response_filename}", "w") as f:
                    f.write(response)
                print(f"Saved response to {response_filename}")

                # Update the cache with the response file name
                if file in cache:
                    cache[file].append(response_filename)
                else:
                    cache[file] = [response_filename]

                with open(cache_file, "w") as f:
                    json.dump(cache, f)

# Call the main function
if __name__ == '__main__':
    main()