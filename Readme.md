### PostgreAI 
### Intelligence to Postgres

#### The fetaures of PostgreAI are as below:

1. Enhancing Data Analysis for Improved Clarity through Distribution Plots and Time Series Visualization of data from PG tables
1. Leveraging Historical Data from PostgreSQL Tables for Proactive Decision-Making
	- Sales Forecasting 
	- Server Capacity Planning
	- Stock market Prediction


### Data Analysis
PostgreAI's Data Analysis feature transforms generic data from PostgreSQL tables into actionable insights. By loading table data into a Pandas DataFrame, users gain access to an array of statistical metrics, including means, medians, and standard deviations. The application provides a quick overview of the data by displaying the first 5 rows and essential DataFrame information like data types and non-null counts. For better data comprehension, PostgreAI creates graphs illustrating the distribution of distinct values in selected columns. Moreover, it offers time series analysis capabilities, automatically detecting timestamp columns and generating graphical representations to uncover trends and patterns over time.

### Forecasting
In the realm of forecasting, PostgreAI leverages predefined models to predict future outcomes based on diverse data sources, encompassing sales data, weather data, and database/server monitoring data. Through efficient data loading into Pandas DataFrames, the system prepares data for comprehensive analysis and pattern recognition. Using advanced algorithms, PostgreAI identifies meaningful patterns and relationships within the data, subsequently constructing predictive models for target fields such as sales, profit, or disk usage. With these predictive models, users gain the power to make informed decisions and forecasts, whether predicting future sales trends or anticipating resource utilization patterns. PostgreAI simplifies the process of data-driven forecasting, offering valuable insights for strategic planning and decision-making.

### Distributional analysis of data

![alt "Distributional analysis of manufacturers"](https://github.com/Harisai-edb/postgreAI/blob/main/pgai/empstat/static/pgai/make_chart.png?raw=true)


### Timeseries Analysis

![alt "Time series analysis for weather"](https://github.com/Harisai-edb/postgreAI/blob/main/pgai/empstat/static/pgai/Temperature_Avg_vs_Date_chart.png?raw=true)

### Forecasting

![alt "Capacity planning for disk space"](https://github.com/Harisai-edb/postgreAI/blob/main/pgai/empstat/static/pgai/disk_usage_fc_last_year.png?raw=true)
