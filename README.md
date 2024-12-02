**Real-Time Stock Data Streaming and Analysis**

**FinalProjectBigData.docx.pdf:** This paper describes a real-time stock prediction project that integrates Hadoop, Kafka, and PySpark to develop a scalable solution for analyzing financial data. The authors created an ETL pipeline to process historical and real-time stock data, implementing three technical analysis indicators (Moving Average, Relative Strength Index, and Bollinger Bands) to predict stock trends, with a specific focus on analyzing Nvidia and Tesla stocks. The project aims to address limitations in existing stock prediction methods by leveraging distributed computing, real-time data streaming, and advanced analytics to provide more accurate and timely insights for investors.

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


