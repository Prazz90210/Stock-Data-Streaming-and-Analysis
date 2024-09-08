Real-Time Stock Data Streaming and Analysis

This project builds a real-time data streaming architecture. Apache Kafka, Zookeeper, and Python are used for fetching, processing, and analyzing stock price data. The setup of Kafka and Zookeeper servers, a Kafka producer for fetching stock data from APIs, Kafka consumers for consuming and storing the data, and Python scripts for data analysis and visualization is required.

Prerequisites

- Apache Kafka and Zookeeper
- Python 3.8.10 with the following libraries installed:
  - `requests`
  - `pandas`
  - `matplotlib`
  - `seaborn`
  - `pyspark`
  - `kafka-python`
  - `yfinance`

Setup

1. Start Zookeeper server:

   bin/zookeeper-server-start.sh config/zookeeper.properties

2. Start Kafka server:

   bin/kafka-server-start.sh config/server.properties


Data Fetching and Streaming

1. Run the Kafka producer script to fetch stock data and publish it to Kafka topics:

   python3 1_multiple_fetch.py

2. In a separate terminal, run the Kafka consumer script to consume the data from Kafka topics and write it to CSV files:
  
   python3 2_multiple_consumer.py
   
 
Data Analysis and Visualization

1. Run the following script to download historical stock data for analysis:

  datadownload.ipynb

2. After downloading the data, you can start the analysis and visualization script:

  3_Project.ipynb
