import pandas as pd
import requests
from langchain.text_splitter import RecursiveCharacterTextSplitter
from tqdm import tqdm
from langchain.docstore.document import Document
import ollama

MODEL = 'llama3_8b-Q5_km'

# Data
ticker_to_stock = {'GE': 'General Electric (GE)'}
ext_df = pd.read_csv('../dat_ge.csv', index_col=0)

# Prom
llama3_prompt_template = """### System: 
Forget all your previous instructions. You are a financial expert with stock market analysis experience. A news article will be passed and you will give only a single score between 1-5 as an answer. Based on a specific stock, score what sentiment the article implies on a certain stock: range from 1 to 5, where 1 is negative, 2 is somewhat negative, 3 is neutral, 4 is somewhat positive, 5 is positive.
Examples:  
  Stock of interest -- Apple: `AAPL: Apple (AAPL) announced iPhone 15`: Answer: `4`
  Stock of interest -- XOM: `Exxon (XOM) price decreased more than 3%: Answer: `1`
  Stock of interest -- MSFT: `Microsoft (MSTF) price has no change`: Answer: `3`
  Stock of interest -- Visa: `Visa got better earnings than expected`: Answer: `5` 
  Stock of interest -- BRK: `BRK got slightly worse earnings than expected`: Answer: `2` 

### Article:
```
{article}
```
## User:
What is the implied sentiment of the article to {stock} stock? Answer only a single number from 1 to 5.

### Assistant:
The implied sentiment for {stock} is """

# Functions for stuff sentiment
def ollama_api(prompt, model=MODEL, temperature=0, max_new_tokens=1):
    response = ollama.chat(model=model, messages=[
                  {
                    'role': 'user',
                    'content': prompt,
                    'options': {
                        "seed": 123,
                        "temperature": temperature,
                        "num_predict": max_new_tokens
                  }
                  }
                ])['message']['content']
    return response

def clean_output(output):
    output = output[:2]
    output = output.strip(':`.!?\n\\#"')
    return output

def stuff_sentiment(article, stock):
    headers = {"Content-Type": "application/json"}
    template = llama3_prompt_template
    prompt = template.format(article=article, stock=stock)
    response = ollama_api(prompt)
    response =  clean_output(response)
    return response

# Run
results = []
for i in ext_df.index:
    response = stuff_sentiment(ext_df.loc[i].Article, ticker_to_stock[ext_df.loc[i].Stock_symbol])
    results.append(response)

# Export
result_df = pd.DataFrame(results, index=ext_df.index)
result_df.to_csv('results_llm3q5.csv')





