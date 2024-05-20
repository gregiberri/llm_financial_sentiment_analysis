# LLM for Financial Sentiment Analysis
## Prerequisites

### Build the docker container
`docker compose build`

### Start the docker container
Change `docker-compose.yml` to your liking.
`docker compose up -d`

It will start the following containers: 
- oobabooga: for loading and setting LLMs on a webui (localhost:7860) calling them on api (localhost:5000)
- llm_sentiment: developement container for ssh remote interpreter developement (localhost:5578) and jupyter lab (localhost:5577)

## Project Structure
The project consists of 7 notebooks from data loading and cleaning through sentiment prediction to sentiment enhanced stock price prediction. All notebooks can be found in the notebooks folder.

### 1_EDA.ipynb
This notebook is made for data downloading, extracting the required data for the sentiment and stock price prediction and analyzing it.
If you would not like to download the full original FNSPID stock news data (~24gb) then skip the first 2 points and start with `3. Select GE and make deeper investigation`

### 2_sentiment_prediction.ipynb
This notebook contains the code for predicting sentiment from full articles and headlines in Vicuna prompt format. This is done with oobabooga api (localhost:5000), sending the prompt and receiving the llm answer. 

As LLMs have limited prompt length we used 2 methods for predicting sentiment based on the prompt length:
- for short prompts: use the whole prompt
- for long promtpts: map-reduce: split the article into smaller parts and use the llm to summarize them with keeping the sentiment information, then concatenate the summarys and run the sentiment prediction model on them

To run the sentiment prediction on a selected model the model has to be selected on oobabooga webui (localhost:7860).

### 3_finbert_benchmark.ipynb and 5_openai_benchmark.ipynb
Running the sentiment prediction on FinBERT and GPT3.5 on headlines as benchmark. While FinBERT was specifically trained on financial sentiment prediction, its training mostly consisted of single sentences and its context length is only 512 tokens, making it insufficient for running on full articles. On the othe hand, GPT3.5 was trained on general texts and has a large context size, but is a paid model: the more tokens used the  higher the price is, which makes it also insufficient to run on longer articles.

### 6_sentiment_prediction_analysis.ipynb
Analysing the predicted sentiments and drawing graphs for further understanding. We can see a double grouping: models run on headlines correlate more with each other than with models run on full articles, and models run on full articles correlate more with each other than with models run on headlines. This shows that headlines and full articles provide different information and give different sentiments. This implies that full articles are more sufficient for sentiment analysis and headlines can lead to higher noise during the training.

### 7_stock_prediction.ipynb and 8_evaluation_backtest.ipynb
Cleaning the sentiment predictions and merging it with historical stock price and Fama-French factors. Furthermore preprocessing the merged data (normalizing and scaling) for providing sufficient input for the model. 
Finally, training the model with different sentiments to show their difference providing evidence that using full articles is superior to not using sentiment or using headlines. Furthermore, we can see that using headline sentiments deteriorates results, showing that headline information is not sufficient for sentiment prediction and can lead to adding noise to stock price prediction.
