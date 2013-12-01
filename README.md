Case-Shiller Index of US residential house prices. Data comes from S&P
Case-Shiller data and includes both the national index and the indices for 20
metropolitan regions. The indices are created using a repeat-sales methodology.

## Data

There is [home page for Indices on S&P website][sp-home]. This provides a table
of links but these are not direct file URLs and you have dig around in S&P's
javascript to find the actual download locations:

[sp-home]: http://www.spindices.com/index-family/real-estate/sp-case-shiller

* [National index][nat] (xls)
* [City indices][city] (xls)

[nat]: http://us.spindices.com/documents/additionalinfo/20131126/64929_csnational-values-1126.xls'
[city]: http://us.spindices.com/documents/additionalinfo/20131126/64929_cshomeprice-history-1126.xls

## Wrangling

To download and process the data do:

    python scripts/process.py

Updated data files will then be in `data` directory.

