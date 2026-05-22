<a className="gh-badge" href="https://datahub.io/core/house-prices-us"><img src="https://badgen.net/badge/icon/View%20on%20datahub.io/orange?icon=https://datahub.io/datahub-cube-badge-icon.svg&label&scale=1.25" alt="badge" /></a>

Case-Shiller Index of US residential house prices. Data comes from S&P
Case-Shiller data and includes both the national index and the indices for 20
metropolitan regions. The indices are created using a repeat-sales methodology.

## Data

As per the [home page for Indices on S&P website][sp-home] (now hosted at spglobal.com):

> The S&P/Case-Shiller U.S. National Home Price Index is a composite of
> single-family home price indices for the nine U.S. Census divisions and is
> calculated monthly. It is included in the S&P/Case-Shiller Home Price Index
> Series which seeks to measure changes in the total value of all existing
> single-family housing stock.

[Documentation of the methodology can be found at](https://www.spglobal.com/spdji/en/documents/methodologies/methodology-sp-cs-home-price-indices.pdf)

Key points are (excerpted from methodology):

* The indices use the "repeat sales method" of index calculation which uses
  data on properties that have sold at least twice, in order to capture the
  true appreciated value of each specific sales unit.
* The quarterly S&P/Case-Shiller U.S. National Home Price Index aggregates nine
  quarterly U.S. Census division repeat sales indices using a base period a nd
  estimates of the aggregate value of single family housing stock for those periods.
* The S&P/Case - Shiller Home Price Indices originated in the 1980s by Case
  Shiller Weiss's research principals, Karl E. Case and Robert J. Shiller. At
  the time, Case and Shiller developed the repeat sales pricing technique. This
  methodology is recognized as the most reliable means to measure housing price
  movements and is used by other home price ind ex publishers, including the
  Office of Federal Housing Enterprise Oversight (OFHEO)

[sp-home]: https://www.spglobal.com/spdji/en/index-family/real-estate/sp-case-shiller

## Preparation

To download and process the data, set the `API_KEY` environment variable to a
valid [FRED API key](https://fred.stlouisfed.org/docs/api/api_key.html) and run:

    make

This runs `scripts/data_fetch_and_process.py` (fetches per-series data from the
FRED API into `archive/`) followed by `scripts/convert_to_final_data.py`
(combines the archive files into the final CSVs in `data/`).

## Data quirks

- **MA-Boston (NSA)**: values are `0` for months in the early part of the series
  where FRED reports no observation rather than a null.
- **CA-San Diego (SA)**: blank values appear in the earliest months before the
  series begins.
- All dates are set to the first day of the month (`YYYY-MM-01`).

This product uses the FRED® API but is not endorsed or certified by the Federal Reserve Bank of St. Louis.

## License

Any rights of the maintainer are licensed under the PDDL. Exact legal status of
source data (and hence of resulting processe data) is unclear but could have a
presumption of public domain given its factual nature and US provenance.
However, the current application of PDDL is indicative of maintainers
best-guess (and comes with no warranty).

