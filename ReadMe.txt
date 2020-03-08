This project will:
1. Fetch daily data from a chosen subreddit
2. Fetch monthly data from said subreddit for a sepecified date range
3. Clean data
4. Create summary tables from the data
5. Load data into Google Big Query


To run this code:

1. add project id from your GCP Account into gcp_credentials.py
2. add your reddit API credentials to Reddit_data_credentials.py
4. Execute Reddit_Project.py

Additional information:

The monthly historical data is to get data for the month of Febuary. If you wish to change this parameter then please see line 51
and 52 in Reddit_Project.py. dates must be entered in Epoch Unix Timestamp format. 


*NOTE*: After executing the code please check Big Query to see if the tables are generated, if you received an error in the terminal: 'Unable to create credentials directory.' then re-execute the script again as this will still successfully load into Big Query despite the error message. 
