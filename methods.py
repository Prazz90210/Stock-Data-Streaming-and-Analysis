import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from pyspark.sql import functions as F
from pyspark.sql.functions import avg, col, lag, when
from pyspark.sql.window import Window


def plot_moving_average(df, stock_name):
    # Ensure that the 'Date' column is in datetime format
    df['Date'] = pd.to_datetime(df['Date'])

    # Filter the dataframe to get the data for the last year
    last_year_df = df[df['Date'] >= '2023-03-21']

    # Plot the true data
    plt.plot(last_year_df['Date'], last_year_df['Close'], label='True Data')

    # Calculate the moving average
    last_year_df['Moving Average'] = last_year_df['Close'].rolling(window=30).mean()

    # Plot the moving average
    plt.plot(last_year_df['Date'], last_year_df['Moving Average'], label='Moving Average')

    # Set the x-axis label and title
    plt.xlabel('Date')
    plt.title(f'Moving Average vs True Data for {stock_name}')

    # Rotate the x-axis labels for better readability
    plt.xticks(rotation=45)

    # Adjust the x-axis to display dates every 30 days
    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=30))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

    # Display the legend
    plt.legend()

    # Show the plot
    plt.show()

def calculate_rsi(spark_df, period=14):
    # Calculate daily price change
    window = Window.orderBy("Date")
    spark_df = spark_df.withColumn("Delta", spark_df["Close"] - lag(spark_df["Close"], 1).over(window))

    # Separate gains and losses
    spark_df = spark_df.withColumn("Gain", when(col("Delta") > 0, col("Delta")).otherwise(0))
    spark_df = spark_df.withColumn("Loss", when(col("Delta") < 0, -col("Delta")).otherwise(0))

    # Calculate the average gain and loss
    avg_gain = Window.orderBy("Date").rowsBetween(-period + 1, 0)
    avg_loss = Window.orderBy("Date").rowsBetween(-period + 1, 0)
    spark_df = spark_df.withColumn("AvgGain", avg(col("Gain")).over(avg_gain))
    spark_df = spark_df.withColumn("AvgLoss", avg(col("Loss")).over(avg_loss))

    # Calculate RS and RSI
    spark_df = spark_df.withColumn("RS", col("AvgGain") / col("AvgLoss"))
    spark_df = spark_df.withColumn("RSI", 100 - (100 / (1 + col("RS"))))

    return spark_df

def plot_rsi(df, stock_name):
    # Convert Spark DataFrame to Pandas DataFrame
    df_pd = df.toPandas()

    # Ensure that the 'Date' column is in datetime format
    df_pd['Date'] = pd.to_datetime(df_pd['Date'])

    # Filter the dataframe to get the data for the last year
    last_year_df = df_pd[df_pd['Date'] >= pd.Timestamp.now() - pd.DateOffset(years=1)]

    # Plot the RSI
    plt.figure(figsize=(12, 6))
    plt.plot(last_year_df['Date'], last_year_df['RSI'], label='RSI')

    # Set the x-axis label, y-axis label, and title
    plt.xlabel('Date')
    plt.ylabel('RSI')
    plt.title(f'RSI for {stock_name} (Last Year)')

    # Set y-axis range to [0, 100] for RSI
    plt.ylim(0, 100)

    # Add a horizontal line at 70 and 30 to indicate overbought and oversold levels
    plt.axhline(70, color='r', linestyle='--', label='Overbought (70)')
    plt.axhline(30, color='g', linestyle='--', label='Oversold (30)')

    # Rotate the x-axis labels for better readability
    plt.xticks(rotation=45)

    # Display the legend
    plt.legend()

    # Show the plot
    plt.show()


def plot_bollinger_bands_last_year(df, stock_name, window=20, num_std=2):
    # Convert the PySpark DataFrame to a Pandas DataFrame
    df_pd = df.toPandas()

    # Ensure that the 'Date' column is in datetime format
    df_pd['Date'] = pd.to_datetime(df_pd['Date'])

    # Filter the dataframe to get the data for the last year
    last_year_df = df_pd[df_pd['Date'] >= pd.Timestamp.now() - pd.DateOffset(years=1)]

    # Calculate the moving average and standard deviation
    last_year_df['Moving_Average'] = last_year_df['Close'].rolling(window=window).mean()
    last_year_df['Standard_Deviation'] = last_year_df['Close'].rolling(window=window).std()

    # Calculate the upper and lower Bollinger Bands
    last_year_df['Upper_Band'] = last_year_df['Moving_Average'] + (last_year_df['Standard_Deviation'] * num_std)
    last_year_df['Lower_Band'] = last_year_df['Moving_Average'] - (last_year_df['Standard_Deviation'] * num_std)

    # Plot the closing price
    plt.plot(last_year_df['Date'], last_year_df['Close'], label='Close', color='blue')

    # Plot the moving average
    plt.plot(last_year_df['Date'], last_year_df['Moving_Average'], label='Moving Average', color='green')

    # Plot the upper and lower Bollinger Bands
    plt.plot(last_year_df['Date'], last_year_df['Upper_Band'], label='Upper Band', color='red', linestyle='--')
    plt.plot(last_year_df['Date'], last_year_df['Lower_Band'], label='Lower Band', color='red', linestyle='--')

    # Set the title and labels
    plt.title(f'Bollinger Bands for {stock_name} (Last Year)')
    plt.xlabel('Date')
    plt.ylabel('Price')

    # Rotate the x-axis labels for better readability
    plt.xticks(rotation=45)

    # Display the legend
    plt.legend()

    # Show the plot
    plt.show()