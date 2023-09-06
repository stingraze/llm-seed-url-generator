#(C)Tsubasa Kato - Inspire Search Corporation - Updated on 9/6/2023 10:44AM
#This is a concept of a generator of seed URLs to be used alongside a web crawler.
#This will output related seeds after asking LLM or a search API in a text file called seeds.txt . 
#Needs actual testing for the code to work. This is provided as a concept to implement further.
#Created with the help of ChatGPT (GPT-4)
from flask import Flask, jsonify, request
#import requests
import subprocess
import re
import urllib.parse

app = Flask(__name__)

LLM_LOCAL_ENDPOINT = "http://localhost:5000/expand-query"
SEARCH_API_ENDPOINT = "https://localhost/search.php?query="  # Replace with the actual search API endpoint

def call_script(script_path, *args):
    command = ['python', script_path] + list(args)
    result = subprocess.run(command, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error occurred: {result.stderr}")
        return None
    
    return result.stdout

def extract_sentences(text):
    return re.findall(r'.*?[?!.]', text)

@app.route('/expand-query', methods=['GET'])
def expand_query():
    query = request.args.get('query')
    
    try:
        output = call_script("test-llama-13b.py", query)
        output = str(output) + " " + "Yes, it's working"
        
        sentences = extract_sentences(output)
        #search using a script on localhost (search.php)
        #the search.php should save seeds with the returned hits to the query. (save to seeds.txt and then launch crawler)

        sentence_to_url = [SEARCH_API_ENDPOINT + urllib.parse.quote(sentence) for sentence in sentences]
        
        return jsonify({'input_and_output': output, 'urls': sentence_to_url})
        
    except Exception as e:
        return jsonify({'error': f"Error processing the request: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0')

