#(C)Tsubasa Kato - Inspire Search Corporation 10/10/2023 14:35PM 
#This allows to create open ended conversations etc. with Stability AI's LLM .
#Great for creating new data out of a small subset of data.
#Please visit my company's website at: https://www.inspiresearch.io/en
import sys
from transformers import AutoModelForCausalLM, AutoTokenizer
import time
from datetime import datetime
from decimal import Decimal
import random
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

n = 10
for _ in range(n):
  input_from_source = get_data()
  inputs = tokenizer(input_from_source, return_tensors="pt").to("cuda")
  tokens = model.generate(
    **inputs,
    max_new_tokens=512,
    temperature=0.75,
    top_p=0.95,
    do_sample=True,
  )
  ts = time.time()
  timestamp = datetime.fromtimestamp(ts)
  now = datetime.now()
  dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
  safe_dt_string = dt_string.replace("/", "-").replace(" ", "_").replace(":", "-")
  filename = "llm-" + safe_dt_string + ".txt"
  print(tokenizer.decode(tokens[0], skip_special_tokens=True))
  output_string = (tokenizer.decode(tokens[0], skip_special_tokens=True))
  with open(filename, 'a') as out:
      out.write(output_string)
