import pandas as pd

## Preprocessing

taxis = pd.read_csv('./data/2015_Green_Taxi_Trip_Data_20250106.csv')

taxis['pickup_date'] = pd.to_datetime(taxis['pickup_datetime'], format="%m/%d/%Y %I:%M:%S %p")
taxis['dropoff_date'] = pd.to_datetime(taxis['dropoff_datetime'], format="%m/%d/%Y %I:%M:%S %p")

taxis = taxis.drop(columns=['vendorid', 'Store_and_fwd_flag', 'pickup_datetime', 'dropoff_datetime', 'rate_code', 'Passenger_count', 'Fare_amount', 'Extra', 'MTA_tax', 'Tolls_amount', 'Ehail_fee', 'Improvement_surcharge', 'Payment_type', 'Trip_type'])
taxis.to_pickle('./data/taxis.pkl')

traffic = pd.read_csv('./data/Automated_Traffic_Volume_Counts.csv')
traffic = traffic.drop(columns=['SegmentID', 'Vol', 'Boro','RequestID'])

df = pd.DataFrame({'year': traffic['Yr'],
                   'month': traffic['M'],
                   'day': traffic['D'],
                   'hour': traffic['HH'],
                   'minute': traffic['MM']})

traffic['date'] = pd.to_datetime(df)

traffic.to_pickle('./data/traffic.pkl')

