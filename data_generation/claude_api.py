# Authors - Shivendra Raghav (1001123853), Amirhosein Morteza (1002187551)
# CSE 5388-002

# This file calls the Claude API and saves the response in a file and tracks details in a json file
# Reference - https://docs.anthropic.com/claude/reference/client-sdks
# Reference - https://www.pullrequest.com/blog/retrying-and-exponential-backoff-smart-strategies-for-robust-software/

import os
import json
import time
import random
import anthropic

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
    prompts_dir = "prompts"
    response_dir = "../synthetic_dataset/sensitive_with_placeholders"
    cache_file = f"{response_dir}/sensitive_with_placeholders.json"

    # Read the files from the prompts directory
    prompts_files = os.listdir(prompts_dir)

    # Use JSON file to track the prompts and responses as a cache file
    # Check if the file exists in the synthetic_dataset directory called sensitive_with_placeholders.json
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            cache = json.load(f)
    else:
        cache = {}
    
    # Iterate through the prompts files and read the text from the files
    for file in prompts_files:
        with open(f"{prompts_dir}/{file}", "r") as f:
            prompt = f.read()

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
            cache[file].append(f"{response_filename}")
        else:
            cache[file] = [f"{response_filename}"]

        # Save the updated cache to the JSON file
        with open(cache_file, "w") as f:
            json.dump(cache, f)
    
# Call the main function
if __name__ == '__main__':
    main()
