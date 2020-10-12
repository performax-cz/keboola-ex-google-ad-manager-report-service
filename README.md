# GAM Report Service Extractor for KBC

Extractor for downloading reports from [Google Ad Manager API](https://developers.google.com/ad-manager/api). It executes a ReportJob and retrieves performance and statistics about ad campaigns, networks, inventory and sales. It uses `ReportService.ReportQuery` endpoint.

[![](images/gam.png)](https://developers.google.com/ad-manager/api/start) [![](images/keboola.png)](https://www.keboola.com/)

## :gear: Configuration

- **`date_from`** and **`date_to`** (REQUIRED) - Period which the reporting information is gathered, e.g. `4 days ago`, `yeserday`, `August 14, 2020 EST` (it uses [dateparser](https://dateparser.readthedocs.io/en/latest))
- **`network_code`** (REQUIRED) - You'll find this in the URL when you are logged into your network. For example, in the URL `https://admanager.google.com/1234#home`, `1234` is your network code.
- **`timezone`** (REQUIRED) - Determines the [time zone](https://developers.google.com/ad-manager/api/reference/v202008/ReportService.ReportQuery#timezonetype) used for the report's date range. It allows `AD_EXCHANGE`, `PUBLISHER` and `PROPOSAL_LOCAL`
- **`#private_key`**, **`#client_email`** and **`token_uri`** (REQUIRED) - Credentials
- **`dimensions`** (OPTIONAL) - The [list](https://developers.google.com/ad-manager/api/reference/v202008/ReportService.ReportQuery#dimensions) of break-down types being requested in the report. It defaults to `AD_EXCHANGE_DFP_AD_UNIT`, `AD_EXCHANGE_PRICING_RULE_NAME` and `DATE` (or `AD_EXCHANGE_DATE` if timezone is `AD_EXCHANGE`)
- **`metrics`** (OPTIONAL) - The [list](https://developers.google.com/ad-manager/api/reference/v202008/ReportService.ReportQuery#columns) of trafficking statistics and revenue information being requested in the report. It defaults to `AD_EXCHANGE_AD_REQUESTS`, `AD_EXCHANGE_MATCHED_REQUESTS`, `AD_EXCHANGE_ESTIMATED_REVENUE` and `AD_EXCHANGE_IMPRESSIONS`
- **`currency`** (OPTIONAL) - The [currency](https://developers.google.com/ad-manager/api/reference/v202008/ReportService.ReportQuery#adxReportCurrency) for Ad Exchange revenue metrics. It defaults to `CZK

## :bookmark: Sample configuration

```json
{
  "date_from": "80 days ago",
  "date_to": "yesterday",
  "network_code": "68713940014",
  "timezone": "AD_EXCHANGE",
  "#private_key": "KBC::ProjectSecure::eJwB1Qcq...OVNcF",
  "#client_email": "KBC::ProjectSecure::eJwBYQGeE...iKz=",
  "token_uri": "https://oauth2.googleapis.com/token",
  "dimensions": [
    "AD_EXCHANGE_DATE",
    "AD_EXCHANGE_DFP_AD_UNIT",
    "AD_EXCHANGE_DFP_AD_UNIT_ID",
    "AD_EXCHANGE_PRICING_RULE_NAME"
  ],
  "metrics": [
    "AD_EXCHANGE_AD_REQUESTS",
    "AD_EXCHANGE_MATCHED_REQUESTS",
    "AD_EXCHANGE_ESTIMATED_REVENUE",
    "AD_EXCHANGE_IMPRESSIONS"
  ]
}
```



## :unlock: How to get credentials and enable API access

1. Create a new [service account](https://console.developers.google.com/apis/credentials/serviceaccountkey) and download JSON file with credentials
2. Enable API in General settings of Google Ad Manager client

More details: https://developers.google.com/ad-manager/api/start

## :technologist: Development

1. Set your own config file `config/config.json` (use template in `config/config.template.json`)
2. Install Docker and Docker Compose and run it by `docker-compose up`
3. Output CSV file is in `output` directory

## :heart: Prepared by Performax

In case of any problems with the extractor or additional requests, contact us on development@performax.cz

[![](images/px.png)](https://performax.cz/)
