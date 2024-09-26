import json
import requests
import os
from datetime import datetime, timedelta

# Load configuration file
def load_config(config_file='config_v1.1.json'):
    with open(config_file, 'r') as f:
        return json.load(f)

# Get the UNIX timestamp for today's midnight (00:00 UTC)
def get_midnight_timestamp():
    now = datetime.utcnow()
    midnight = datetime(now.year, now.month, now.day)
    return int(midnight.timestamp())

# Convert UNIX timestamp to date string in YYYYMMDD format
def timestamp_to_datestr(timestamp):
    return datetime.utcfromtimestamp(timestamp).strftime('%Y%m%d')

# Fetch prices from CryptoCompare API for a specific timestamp
def fetch_prices(coins, timestamp, prev_prices=None):
    api_url = "https://min-api.cryptocompare.com/data/v2/histominute"
    prices = {}
    for coin in coins:
        params = {
            'fsym': coin,
            'tsym': 'USD',
            'limit': 1,
            'toTs': timestamp
        }
        response = requests.get(api_url, params=params)
        data = response.json()
        if data['Response'] == 'Success':
            price = data['Data']['Data'][0]['close']
            prices[coin] = price
        else:
            print(f"Failed to fetch data for {coin}: {data['Message']}")
            # If the price cannot be fetched, use the previous day's price as a backup
            if prev_prices and coin in prev_prices:
                prices[coin] = prev_prices[coin]
            else:
                print(f"No previous price available for {coin}")
    return prices

# Calculate the quantity of each coin based on investment and allocation
def calculate_coin_quantity(prices, investment, allocations):
    quantities = {}
    for coin, percentage in allocations.items():
        if coin in prices:
            allocation_amount = investment * (percentage / 100)
            quantities[coin] = allocation_amount / prices[coin]
    return quantities

# Calculate the total portfolio value based on current prices and quantities
def calculate_portfolio_value(prices, quantities):
    total_value = 0
    for coin, data in quantities.items():
        if data['active']:
            # For active coins, use the latest price
            total_value += data['quantity'] * prices.get(coin, 0)
        else:
            # For inactive coins, use the last known price
            total_value += data['quantity'] * data['last_price']
    return total_value

# Save data to a JSON file
def save_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

# Update the coin quantities and their active status based on the current coin list and prices
def update_quantities_based_on_coins(prev_quantities, new_coins, prices):
    updated_quantities = {}
    for coin in prev_quantities:
        if coin in new_coins:
            # Keep active status and update the latest price
            updated_quantities[coin] = {
                'quantity': prev_quantities[coin]['quantity'],
                'active': True,
                'last_price': prices.get(coin, prev_quantities[coin]['last_price'])  # Update the latest price
            }
        else:
            # For inactive coins, retain the last known price
            updated_quantities[coin] = {
                'quantity': prev_quantities[coin]['quantity'],
                'active': False,
                'last_price': prev_quantities[coin]['last_price']  # Keep the last known price
            }
    
    for coin in new_coins:
        if coin not in updated_quantities:
            updated_quantities[coin] = {
                'quantity': 0,
                'active': True,
                'last_price': prices.get(coin, 0)
            }
    
    return updated_quantities

def main():
    # Load configuration
    config = load_config()
    coins = config['coins']
    allocations = config['coins']
    
    # Get the UNIX timestamp for today's midnight (00:00 UTC)
    timestamp = get_midnight_timestamp()

    # Convert timestamp to date string
    date_str = timestamp_to_datestr(timestamp)

    # Read the previous day's price data
    prev_price_filename = f"{timestamp_to_datestr(timestamp - 86400)}.price.json"
    prev_prices = {}
    if os.path.exists(prev_price_filename):
        with open(prev_price_filename, 'r') as f:
            prev_prices = json.load(f)

    # Fetch prices using the timestamp (passing the previous day's prices as backup)
    prices = fetch_prices(coins, timestamp, prev_prices)

    # Save price data to a file using the date string as filename
    price_filename = f"{date_str}.price.json"
    save_json(prices, price_filename)

    # Initial daily investment amount
    daily_investment = 100

    # Read the previous day's yield file if it exists
    prev_yield_filename = f"{timestamp_to_datestr(timestamp - 86400)}.yield.json"
    if os.path.exists(prev_yield_filename):
        with open(prev_yield_filename, 'r') as f:
            prev_data = json.load(f)
            prev_quantities = prev_data['quantities']
            prev_total_investment = prev_data['total_investment']
            
            # Check and convert old format of prev_quantities if necessary
            for coin, value in prev_quantities.items():
                if isinstance(value, float):
                    prev_quantities[coin] = {'quantity': value, 'active': True, 'last_price': prev_prices.get(coin, 0)}
    else:
        # Initialize the quantities if no previous yield data exists
        prev_quantities = {coin: {'quantity': 0, 'active': True, 'last_price': prices.get(coin, 0)} for coin in coins}
        prev_total_investment = 0

    # Update prev_quantities, retain old coins, and mark active status
    prev_quantities = update_quantities_based_on_coins(prev_quantities, coins, prices)

    # Calculate today's coin purchase quantities
    today_quantities = calculate_coin_quantity(prices, daily_investment, allocations)

    # Update the held quantities
    for coin in prev_quantities:
        if coin in today_quantities and prev_quantities[coin]['active']:
            prev_quantities[coin]['quantity'] += today_quantities[coin]

    # Update total investment amount
    total_investment = prev_total_investment + daily_investment

    # Calculate the total portfolio value
    portfolio_value = calculate_portfolio_value(prices, prev_quantities)

    # Calculate the yield rate (return rate)
    yield_rate = portfolio_value / total_investment if total_investment != 0 else 0

    # Save yield data to a file
    yield_data = {
        'date': date_str,
        'portfolio_value': portfolio_value,
        'total_investment': total_investment,
        'quantities': prev_quantities,
        'yield_rate': round(yield_rate, 4)  # Round to 4 decimal places
    }
    yield_filename = f"{date_str}.yield.json"
    save_json(yield_data, yield_filename)

if __name__ == "__main__":
    main()