# Running Scripts Locally

## Overview
This repository contains scripts originally designed to gather house price data from [eu.spindices.com](https://eu.spindices.com). However, as this data is now considered premium and requires paid access, the current scripts have been updated to use publicly available data from the [FRED API](https://fred.stlouisfed.org/docs/api/api_key.html). The FRED API provides an extensive range of economic datasets, including housing indices and other key economic indicators, making it a suitable alternative for data analysis.

By using these scripts, you can gather real-time and historical data from FRED for various economic metrics.

## Dependencies

To run the scripts locally, you need to install the required dependencies. Ensure that Python is installed on your system before proceeding.

### Install the Required Python Libraries

Use the following commands to install the necessary Python libraries and dependencies:

```bash
pip install -r scripts/requirements.txt
make
```

This will install all the required packages listed in the `requirements.txt` file and run the necessary setup through `make`.

### API Key Setup

In order to access data from the FRED API, you will need to supply your own API key. You can obtain this key by registering for an account at the FRED website. Once you have your API key, make sure to add it to the script or environment where necessary.

> Important: Be mindful of the FRED API's rate limits. The scripts include mechanisms to handle request limits, but it is recommended to monitor your usage to avoid hitting these limits.

### Usage Notes

- The scripts have been designed to minimize the number of API requests made to FRED in order to respect rate limits.
- Ensure that your FRED API key is securely stored and not hardcoded in the scripts to maintain privacy and security.
- For more detailed documentation on the available datasets through the FRED API, refer to the [official API documentation](https://fred.stlouisfed.org/docs/api/fred/).

By following these steps, you should be able to run the scripts locally and access a wide range of economic data for analysis.