#(C)Tsubasa Kato - Inspire Search Corporation - 8/5/2023 17:43PM
#This is a concept of a generator of seed URLs to be used alongside a web crawler.
#This will output related seeds after asking LLM or a search API in a text file called seeds.txt . 
#Needs actual testing for the code to work. This is provided as a concept to implement further.
#Created with the help of ChatGPT (GPT-4)
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

LLM_LOCAL_ENDPOINT = "http://localhost:5001/expand-query"
SEARCH_API_ENDPOINT = "https://searchapi.example.com/search"  # Replace with actual search API endpoint

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
    query = request.json.get('query')
    
    # Expand the query using the LLM
    try:
        response = requests.post(LLM_LOCAL_ENDPOINT, json={'query': query})
        response.raise_for_status()
        llm_data = response.json()
        related_urls = llm_data.get('related_urls', [])

        # Save the related URLs from LLM to seeds.txt
        save_to_seeds_txt(related_urls)

        # If no related URLs are found in the LLM, fetch from a search API
        if not related_urls:
            related_urls = get_urls_from_search_api(query)
            save_to_seeds_txt(related_urls)  # Save the fetched URLs to seeds.txt as well

        return jsonify({'related_urls': related_urls})

    except requests.RequestException as e:
        return jsonify({'error': f"Error processing the request: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(port=5000)
