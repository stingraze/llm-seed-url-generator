#Experimental code generated with the help of ChatGPT (GPT-4)
#Not yet tested to work or not
#(C)Tsubasa Kato 2023/8/16 10:10AM JST
#You can start a Celery worker by running the following command in the same directory as your script:
#celery -A <your_module_name> worker --loglevel=info
#Replace <your_module_name> with the name of the Python file (without the .py extension) where the above code is located.
from flask import Flask, jsonify, request
from celery import Celery
import requests
import subprocess

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)
#Not really needed for this example
SEARCH_API_ENDPOINT = "https://searchapi.example.com/search"  # Replace with actual search API endpoint

@celery.task
def call_script(script_path, *args):
    """
    Calls an external python script with given arguments and captures its output.
    
    Parameters:
    - script_path: Path to the python script to be executed.
    - *args: Variable-length argument list containing arguments for the script.
    
    Returns:
    - The output of the executed script as a string.
    """
    
    command = ['python', script_path] + list(args)
    result = subprocess.run(command, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error occurred while executing {script_path}. Error message:\n{result.stderr}")
        return None
    
    return result.stdout
#Not really needed
def get_urls_from_search_api(query):
    try:
        response = requests.get(SEARCH_API_ENDPOINT, params={'q': query})
        response.raise_for_status()
        search_data = response.json()
        return search_data.get('urls', [])
    except requests.RequestException:
        return []
#To call test-llama-13b.py to get related topics etc., depending on the query. It can be request to list URLs, expand the topic etc.
@app.route('/expand-query', methods=['POST'])
def expand_query():
    query = request.args.get('query')
    task = call_script.apply_async(args=["test-llama-13b.py", query])

    response = {
        'status': 'queued',
        'task_id': task.id
    }

    return jsonify(response), 202

@app.route('/task-status/<task_id>', methods=['GET'])
def task_status(task_id):
    task = call_script.AsyncResult(task_id)

    response = {
        'status': task.state,
        'result': task.result if task.state == 'SUCCESS' else None
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(port=5000)
