import requests
import json
import csv
from datetime import datetime
import pandas as pd
import glob

def main():
    url = 'https://api.taostats.io/api/metagraph/latest/v1'
    headers = {
        'Authorization': 'oMsSsdmi9ILQpk3Cokql3C0VPsutpKoy4O2y3RrhNn2qOxJcha7E1RbR2LTnI4E0',
        'accept': 'application/json'
    }
    params = {
        'netuid': 45,
        'order': 'emission_desc'
    }

    # Perform the GET request
    response = requests.get(url, headers=headers, params=params)

    # Check if the response was successful
    if response.status_code == 200:
        data = response.json()
        # Define CSV columns
        columns = [
            'netuid', 'uid', 'hotkey(ss58)', 'coldkey(ss58)', 'block_number', 'timestamp', 'trust', 'stake', 
            'validator_trust', 'incentive', 'dividends', 'emission', 'active', 'validator_permit', 'daily_reward', 
            'registered_at_block', 'is_immunity_period', 'rank'
        ]

        # Extract timestamp for file naming
        timestamp_str = data.get('data', [])[0].get('timestamp', '')
        if isinstance(timestamp_str, str):
            try:
                timestamp_dt = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S.%fZ")
            except ValueError:
                try:
                    timestamp_dt = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%SZ")
                except ValueError:
                    timestamp_dt = None
        else:
            timestamp_dt = None

        # Create filename using extracted timestamp
        if timestamp_dt:
            filename = timestamp_dt.strftime("taostats_data_%y_%m_%d_%H_%M.csv")
        else:
            filename = 'taostats_data.csv'

        # Create and write to the CSV file
        with open(filename, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=columns)
            writer.writeheader()

            # Iterate over each item in the data to extract specific fields
            for item in data.get('data', []):
                timestamp = item.get('timestamp')
                if isinstance(timestamp, str):
                    try:
                        timestamp = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y %m %d %H %M")
                    except ValueError:
                        try:
                            timestamp = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y %m %d %H %M")
                        except ValueError:
                            timestamp = ''
                
                hotkey = item.get('hotkey', {}).get('ss58', '')
                coldkey = item.get('coldkey', {}).get('ss58', '')
                
                row = {
                    'netuid': item.get('netuid', ''),
                    'uid': item.get('uid', ''),
                    'hotkey(ss58)': hotkey,
                    'coldkey(ss58)': coldkey,
                    'block_number': item.get('block_number', ''),
                    'timestamp': timestamp,
                    'trust': item.get('trust', ''),
                    'stake': item.get('stake', ''),
                    'validator_trust': item.get('validator_trust', ''),
                    'incentive': item.get('incentive', ''),
                    'dividends': item.get('dividends', ''),
                    'emission': item.get('emission', ''),
                    'active': item.get('active', ''),
                    'validator_permit': item.get('validator_permit', ''),
                    'daily_reward': item.get('daily_reward', ''),
                    'registered_at_block': item.get('registered_at_block', ''),
                    'is_immunity_period': item.get('is_immunity_period', ''),
                    'rank': item.get('rank', '')
                }
                writer.writerow(row)

        # Calculate metrics for each taostats_data_*.csv file separately and store results in a list
        all_files = glob.glob("taostats_data_*.csv")
        metrics_list = []
        for file in all_files:
            df = pd.read_csv(file)

            # Convert daily_reward to be divided by 1,000,000,000
            df['daily_reward'] = df['daily_reward'] / 1_000_000_000

            metrics = {
                'filename': file,
                'MAX_netuid': df['netuid'].max(),
                'MAX_block_number': df['block_number'].max(),
                'MAX_timestamp': df['timestamp'].max(),
                'MIN_daily_reward': df['daily_reward'].min(),
                'MIN_NON_IMMUNE_daily_reward': df[df['is_immunity_period'] == False]['daily_reward'].min(),
                'UID_152_daily_reward': df[df['uid'] == 152]['daily_reward'].values[0] if not df[df['uid'] == 152].empty else '',
                'UID_155_daily_reward': df[df['uid'] == 155]['daily_reward'].values[0] if not df[df['uid'] == 155].empty else '',
                'MAX_NON_VALI_daily_reward': df[df['validator_trust'] == 0]['daily_reward'].max(),
                'COUNT_NON_IMMUNE_daily_reward_less_UID_152': len(df[(df['is_immunity_period'] == False) & (df['daily_reward'] < df[df['uid'] == 152]['daily_reward'].values[0])]) if not df[df['uid'] == 152].empty else 0,
                'COUNT_NON_IMMUNE_daily_reward_less_UID_155': len(df[(df['is_immunity_period'] == False) & (df['daily_reward'] < df[df['uid'] == 155]['daily_reward'].values[0])]) if not df[df['uid'] == 155].empty else 0,
                'COUNT_NON_VALI_daily_reward_greater_UID_152': len(df[(df['validator_trust'] == 0) & (df['daily_reward'] > df[df['uid'] == 152]['daily_reward'].values[0])]),
                'COUNT_NON_VALI_daily_reward_greater_UID_155': len(df[(df['validator_trust'] == 0) & (df['daily_reward'] > df[df['uid'] == 155]['daily_reward'].values[0])])
            }
            metrics_list.append(metrics)

        # Write all metrics to a new CSV file or overwrite the existing metrics file
        metrics_filename = 'taostats_metrics.csv'
        metrics_df = pd.DataFrame(metrics_list)
        metrics_df.to_csv(metrics_filename, index=False)

    else:
        print(f"Failed to retrieve data: {response.status_code}")

if __name__ == "__main__":
    main()
