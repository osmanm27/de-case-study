This project will:
1. Fetch daily data from a selected subreddit
2. Fetch monthly data from selected subreddit for a specified date range
3. Clean data
4. Create summary tables from the data
5. Load data into Google Big Query


To run this code:

1. Add project id from your GCP Account into gcp_credentials.py
2. Add your reddit API credentials to Reddit_data_credentials.py
3. Execute Reddit_Project.py

Additional information:

The monthly historical data is configured for the month of Febuary. If you wish to change this parameter then please see line 51 and 52 in Reddit_Project.py. Dates must be entered in Epoch Unix Timestamp format. 


*NOTE*: After executing the code please check Big Query to see if the tables are generated, if you received an error in the terminal: 'Unable to create credentials directory.' then re-execute the script again as this will still successfully load into Big Query despite the error message. 
