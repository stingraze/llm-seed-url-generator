#(C)Tsubasa Kato - Inspire Search Corporation 2023/11/3 12:52PM
#Multi Thread Version of stabilityai-data-expander.py 
#Much faster upon test on a 64GB RAM machine with Core i5 10th generation with 12 threads.
#Code made to be multithread with the help of ChatGPT (GPT-4)
import sys
from transformers import AutoModelForCausalLM, AutoTokenizer
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import random

# Initialize the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("stabilityai/stablelm-3b-4e1t")
model = AutoModelForCausalLM.from_pretrained(
    "stabilityai/stablelm-3b-4e1t",
    trust_remote_code=True,
    torch_dtype="auto",
)
model.cuda()

def get_data():
    lines = open('file.txt').read().splitlines()
    myline = random.choice(lines)
    return myline

def generate_and_save(input_from_source):
    inputs = tokenizer(input_from_source, return_tensors="pt").to("cuda")
    tokens = model.generate(
        **inputs,
        max_new_tokens=512,
        temperature=0.75,
        top_p=0.95,
        do_sample=True,
    )
    output_string = tokenizer.decode(tokens[0], skip_special_tokens=True)
    print(output_string)
    # Use a timestamp for unique filenames
    dt_string = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
    filename = f"llm-{dt_string}.txt"
    with open(filename, 'a') as out:
        out.write(output_string)

# Number of texts to generate
n = 25

# Using ThreadPoolExecutor to generate text concurrently
with ThreadPoolExecutor() as executor:
    # Create a list to hold the futures
    futures = [executor.submit(generate_and_save, "Brain storm from this, as an esteemed professor: " + get_data()) for _ in range(n)]
    # Wait for all futures to complete
    for future in as_completed(futures):
        future.result()  # This will raise any exceptions that occurred in the thread
