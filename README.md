# llm-seed-url-generator
Experimental Repository of Seed URL generator using LLM for use with a web crawler

Tested on a Ubuntu 20.04 environment with 12 thread 10th Generation Core i5 with 64GB of RAM and NVIDIA GeForce RTX 3090. 
dolly2-data-expander.py ran on 16GB of RAM and NVIDIA T4 GPU, but did not run till the end. Better spec is recommended.

Still needs work for full implementation. (Concept stage, some implementation done)

Updated: 11/3/2023: Uploaded stabilityai-data-expander-multi-thread.py under experimental folder. This is the multithread version of stabilityai-data-expander.py. Much faster than single thread version upon test.

Updated: 10/11/2023: Uploaded dolly2-data-expander.py under experimental folder. This asks the LLM (Databrick's Dolly 2 3b) to expand data. The code is mostly the same as stabilityai-data-expander.py.

Update: 10/10/2023: Uploaded stabilityai-data-expander.py under experimental folder. This asks the LLM (Stability AI's Stable LM 3B) to expand data.

Update: 9/6/2023: Modified llm-seed-url-generator2.py (not under experimental) so it works well and provides search URLs to extract the related URLs from a search engine endpoint (this is search.php in this case, not in this repository).

Update: 9/1/2023: Added llm-seed-generator2.py under experimental folder. Still work in progress, but it now extracts sentences from the output from Llama 2 by a simple method and jsonifies (jsonify) it. It now needs to make URL that will send the sentences extracted to a search engine query for this script to be fully implemented to make it be crawled with a web crawler.

Update: 8/23/2023: test-llama-13b.py wasn't working anymore so I made a fixed version and uploaded it here.

Update: 8/14/2023: Made an implemented version of API working with Llama 2. (llm-seed-url-generator-working.py).

(C)Tsubasa Kato 2023 Made with the help of ChatGPT (GPT-4)
