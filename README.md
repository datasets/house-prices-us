Case-Shiller Index of US residential house prices. Data comes from S&P
Case-Shiller data and includes both the national index and the indices for 20
metropolitan regions. The indices are created using a repeat-sales methodology.

## Data

There is [home page for Indices on S&P website][sp-home]. This provides a table
of links but these are not direct file URLs and you have dig around in S&P's
javascript to find the actual download locations:

[sp-home]: http://www.standardandpoors.com/indices/sp-case-shiller-home-price-indices/en/us/?indexId=spusa-cashpidff--p-us----

* [National index][nat] (xls)
* [City indices][city] (xls)

To convert to the final form we do various processing:

* Convert to CSV with dataconvert
* Normalize the files using scripts/process.py

[nat]: http://www.standardandpoors.com/servlet/BlobServer?blobheadername3=MDT-Type&blobcol=urldocumentfile&blobtable=SPComSecureDocument&blobheadervalue2=inline%3B+filename%3Ddownload.xls&blobheadername2=Content-Disposition&blobheadervalue1=application%2Fexcel&blobkey=id&blobheadername1=content-type&blobwhere=1245214513097&blobheadervalue3=abinary%3B+charset%3DUTF-8&blobnocache=true
[city]: http://www.standardandpoors.com/servlet/BlobServer?blobheadername3=MDT-Type&blobcol=urldocumentfile&blobtable=SPComSecureDocument&blobheadervalue2=inline%3B+filename%3Ddownload.xls&blobheadername2=Content-Disposition&blobheadervalue1=application%2Fexcel&blobkey=id&blobheadername1=content-type&blobwhere=1245214507048&blobheadervalue3=abinary%3B+charset%3DUTF-8&blobnocache=true

