#(C)Tsubasa Kato - Inspire Search Corporation - 8/14/2023 12:16PM
#This is a concept of a generator of seed URLs to be used alongside a web crawler.
#This will output related seeds after asking LLM or a search API in a text file called seeds.txt . 
#Working as of 8/14/2023. Needs cleaning of the code for removing unneeded code etc.
#Created with the help of ChatGPT (GPT-4)
from flask import Flask, jsonify, request
import requests
import subprocess
app = Flask(__name__)

LLM_LOCAL_ENDPOINT = "http://localhost:5001/expand-query"
SEARCH_API_ENDPOINT = "https://searchapi.example.com/search"  # Replace with actual search API endpoint


def call_script(script_path, *args):
    """
    Calls an external python script with given arguments and captures its output.
    
    Parameters:
    - script_path: Path to the python script to be executed.
    - *args: Variable-length argument list containing arguments for the script.
    
    Returns:
    - The output of the executed script as a string.
    """
    
    # Construct the command list
    command = ['python', script_path] + list(args)
    
    # Use the subprocess.run method to execute the script and capture the output
    result = subprocess.run(command, capture_output=True, text=True)
    
    # Check if there's any error in the output
    if result.returncode != 0:
        print(f"Error occurred while executing {script_path}. Error message:\n{result.stderr}")
        return None
    
    # Return the captured output
    return result.stdout


def get_urls_from_search_api(query):
    try:
        response = requests.get(SEARCH_API_ENDPOINT, params={'q': query})
        response.raise_for_status()
        search_data = response.json()
        # Assuming the search API response contains a 'urls' key with a list of URLs
        return search_data.get('urls', [])
    except requests.RequestException:
        return []

def save_to_seeds_txt(urls):
    """Save a list of URLs to seeds.txt, one URL per line."""
    with open('seeds.txt', 'a') as file:
        for url in urls:
            file.write(f"{url}\n")

@app.route('/expand-query', methods=['POST'])
def expand_query():
    #query = request.json.get('query')
    query = request.args.get('query')
    # Expand the query using the LLM
    try:
        #response = requests.post(LLM_LOCAL_ENDPOINT, json={'query': query})
        #response.raise_for_status()
        #llm_data = response.json()
        #related_urls = llm_data.get('related_urls', [])

        # Save the related URLs from LLM to seeds.txt
        #save_to_seeds_txt(related_urls)

        # If no related URLs are found in the LLM, fetch from a search API
        #if not related_urls:
        #    related_urls = get_urls_from_search_api(query)
        #    save_to_seeds_txt(related_urls)  # Save the fetched URLs to seeds.txt as well

        #if output is not None:
            #print("Output from the script:\n", output)
        output = call_script("test-llama-13b.py", query)
        output = str(output) + " " + " Yes, it's working"
        return jsonify({'related_urls': output})

    except requests.RequestException as e:
        return jsonify({'error': f"Error processing the request: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(port=5000)
