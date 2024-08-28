# Daily Crypto Investment Yield Analysis

This project is a Python-based script designed to calculate the daily yield of a cryptocurrency investment portfolio. By fetching historical price data from the CryptoCompare API and simulating daily investments, the script computes the portfolio's value and yield rate over time.

## Features

- **Automated Daily Investment Calculation**: Simulates a daily investment strategy by allocating a fixed amount of money across multiple cryptocurrencies based on predefined allocation percentages.
- **Historical Price Fetching**: Utilizes the CryptoCompare API to fetch historical minute-level price data for each cryptocurrency.
- **Yield Calculation**: Calculates the daily yield rate and updates the portfolio's total value based on current market prices.
- **JSON Output**: Saves daily price and yield data to JSON files, which are named based on the date of the data.

## How It Works

1. **Configuration**: The script reads a configuration file (`config_v1.json`) to determine which cryptocurrencies to include in the portfolio and their respective allocation percentages.
2. **Fetch Prices**: It uses the CryptoCompare API to fetch the historical prices of the specified cryptocurrencies for the previous day's midnight (UTC).
3. **Calculate Quantities**: Based on the current prices and allocation percentages, the script calculates how much of each cryptocurrency would be purchased with the fixed daily investment amount.
4. **Update Portfolio**: It updates the portfolio with the newly purchased quantities and calculates the total portfolio value.
5. **Compute Yield Rate**: The yield rate is calculated as the ratio of the portfolio's current value to the total invested amount.
6. **Save Results**: The calculated data, including the portfolio value, yield rate, and individual cryptocurrency quantities, is saved to a JSON file named with the corresponding date.

## Prerequisites

- **Python 3.x**: Ensure Python 3.x is installed on your system.
- **Python Packages**: The script requires the `requests` library to fetch data from the CryptoCompare API. You can install it using pip:

    ```
    pip install requests
    ```

## Setup

1. **Clone the Repository**:

    ```
    git clone https://github.com/yourusername/yourrepository.git
    cd yourrepository
    ```

2. **Configure the Script**:
   - Update the `config_v1.json` file with the cryptocurrencies and allocation percentages you want to use in the analysis.

3. **Run the Script**:

    ```
    python main.py
    ```

## Configuration File Format (`config_v1.json`)

The configuration file specifies the coins to include in the portfolio and their respective allocation percentages. Here is an example configuration:

```
{
  "version": "v1",
  "coins": {
      "BTC": 50,
      "ETH": 10,
      "LTC": 5,
      "DOGE": 5,
      "BCH": 5,
      "ADA": 5,
      "SOL": 5,
      "FIL": 5,
      "TON": 5,
      "XEC": 3,
      "DASH": 2
  }
}
```

## Output Files

- **Price Data (`YYYYMMDD.price.json`)**: Contains the fetched prices of all cryptocurrencies at midnight (UTC) for a specific day.
- **Yield Data (`YYYYMMDD.yield.json`)**: Contains the portfolio value, total investment, quantities of each cryptocurrency, and yield rate for a specific day.

## GitHub Actions Workflow

This project includes a GitHub Actions workflow (`.github/workflows/main.yml`) that automates the daily execution of the script at 01:00 UTC and commits the output files to the repository.

To manually trigger the workflow:

1. Navigate to the **Actions** tab in your repository.
2. Select the **Daily Crypto Investment Analysis** workflow.
3. Click the **Run workflow** button.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an Issue for any bugs, suggestions, or improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [CryptoCompare API](https://min-api.cryptocompare.com) for providing historical cryptocurrency data.
- The GitHub Actions team for automating workflows.