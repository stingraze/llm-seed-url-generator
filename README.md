# llm-seed-url-generator
Experimental Repository of Seed URL generator using LLM for use with a web crawler

Tested on a Ubuntu 20.04 environment with 12 thread 10th Generation Core i5 with 64GB of RAM and GeForce RTX 3090.

Still needs work for actual implementation. (Concept stage, implemented version coming soon)

Update: 8/14/2023: Made an implemented version of API working with Llama 2. 
(llm-seed-url-generator-working.py)

Update: 8/23/2023: test-llama-13b.py wasn't working anymore so I made a fixed version and uploaded it here.

Update: 9/1/2023: Added llm-seed-generator2.py under experimental. Still work in progress, but it now extracts sentences from the output from Llama 2 by a simple method and jsonifies (jsonify) it. 
It now needs to make URL that will send the sentences extracted to a search engine query for this script to be fully implemented to make it be crawled with a web crawler.

Update: 9/6/2023: Modified llm-seed-url-generator2.py (not under experimental) so it works well and provides search URLs to extract the related URLs from a search engine endpoint (this is search.php in this case, not in this repository)

(C)Tsubasa Kato 2023 Made with ChatGPT (GPT-4)
