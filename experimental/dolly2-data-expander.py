#(C)Tsubasa Kato - Inspire Search Corporation 10/11/2023 8:26AM 
#This allows to create open ended conversations etc. with Databrick's dolly-v2-3b
#Great for creating new data out of a small subset of data.
#Please visit my company's website at: https://www.inspiresearch.io/en
import sys
import time
from datetime import datetime
from decimal import Decimal
import random
import torch
from transformers import pipeline
import sys
def get_data():
  lines = open('file.txt').read().splitlines()
  myline = random.choice(lines)
  return myline

n = 10
for _ in range(n):
  #Get Data from file (file.txt)
  input_from_source = get_data()
  #Get timestamp and use it as the variable for file name
  ts = time.time()
  timestamp = datetime.fromtimestamp(ts)
  now = datetime.now()
  dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
  safe_dt_string = dt_string.replace("/", "-").replace(" ", "_").replace(":", "-")
  filename = "llm-" + safe_dt_string + ".txt"

  generate_text = pipeline(model="databricks/dolly-v2-3b", torch_dtype=torch.bfloat16, trust_remote_code=True, device_map="auto")
  res = generate_text(input_from_source)
  print(res[0]["generated_text"])
  #Output to File 
  output_string = (res[0]["generated_text"])
  with open(filename, 'a') as out:
      out.write(output_string)
