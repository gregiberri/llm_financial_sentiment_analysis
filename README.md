# LLM for Financial Sentiment Analysis
## Prerequisites
### Download the data to `data` folder
`wget https://huggingface.co/datasets/Zihan1004/FNSPID/resolve/main/Stock_news/nasdaq_exteral_data.csv`
`wget https://huggingface.co/datasets/Zihan1004/FNSPID/resolve/main/Stock_price/full_history.zip`

### Build the docker container
`docker compose build`

### Start the docker container
Set `docker-compose.yml` to your structure, originally it was made for the repository.
`docker compose up -d`