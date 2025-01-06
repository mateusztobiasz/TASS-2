import pandas as pd

## Preprocessing

# taxis = pd.read_csv('./data/2015_Green_Taxi_Trip_Data_20250106.csv')

# taxis['pickup_date'] = pd.to_datetime(taxis['pickup_datetime'], format="%m/%d/%Y %I:%M:%S %p")
# taxis['dropoff_date'] = pd.to_datetime(taxis['dropoff_datetime'], format="%m/%d/%Y %I:%M:%S %p")

# taxis['Total_cost'] = taxis['Total_amount'] - taxis['Tip_amount']

# taxis = taxis.drop(columns=['vendorid', 'Store_and_fwd_flag', 'pickup_datetime', 'dropoff_datetime', 'rate_code', 'Passenger_count', 'Fare_amount', 'Extra', 'MTA_tax', 'Tolls_amount', 'Tip_amount', 'Total_amount', 'Ehail_fee', 'Improvement_surcharge', 'Payment_type', 'Trip_type'])
# taxis.to_pickle('./data/taxis.pkl')

# traffic = pd.read_csv('./data/Automated_Traffic_Volume_Counts.csv')
# traffic = traffic[traffic['Yr'] == 2015]

# df = pd.DataFrame({'year': traffic['Yr'],
#                    'month': traffic['M'],
#                    'day': traffic['D'],
#                    'hour': traffic['HH'],
#                    'minute': traffic['MM']})

# traffic['date'] = pd.to_datetime(df)
# traffic = traffic.drop(columns=['SegmentID', 'Vol', 'Boro','RequestID', 'Yr', 'M', 'D', 'HH', 'MM'])

# traffic.to_pickle('./data/traffic.pkl')

## Extracting data

traffic = pd.read_pickle('./data/traffic.pkl')

traffic_hours_count = traffic.groupby(['date'])
counts = traffic_hours_count.count()
chosen_traffics = counts[counts['street'] > 100]

print(chosen_traffics)
chosen_traffics.to_pickle('./data/chosen_traffics.pkl')

taxis = pd.read_pickle('./data/taxis.pkl')

n_taxis = 1000000
time_bias = pd.Timedelta(minutes=31)
taxi_pickups = taxis['pickup_date'][0:n_taxis]
indices = pd.Series([False]*len(taxi_pickups))
for traffic_timestamp in chosen_traffics.index:
    indices = indices | ((traffic_timestamp - taxi_pickups).abs() < time_bias)

chosen_taxis = taxis[0:n_taxis][indices]
chosen_taxis.to_pickle('./data/chosen_taxis.pkl')
print(chosen_taxis)
