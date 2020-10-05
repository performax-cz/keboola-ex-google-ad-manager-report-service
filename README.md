Extractor for download report from Ad Manager. Report is created by ReportService.ReportQuery API. You are allowed to specify your own metrics and dimensions.

## Credentials

1. [Create new service account. Download json file with credentials.](https://console.developers.google.com/apis/credentials/serviceaccountkey)

2. Make API enabled in Ad Manager client (General settings)

3. Add service account in Ad Manager client

[Documentation for getting credentials](https://developers.google.com/ad-manager/api/start#python_)

## Configuration

### date_from - date_to

Along with credentials, you must provide some additinal configuration. You need to specify time range - `date_from` and `date_to`. Valid entries are anything which can be parsed using `dateparser.parse()` python method (https://dateparser.readthedocs.io/en/latest/).

#### Example:

```
"date_from": "4 days ago",
"date_to": "yesterday 
```

### network_code

You also need to specify `network_code`. This information should be obtained in Ad Manager UI.

#### Example:

```
"network_code": 1234567
```

### timezone

This configuration directive does not set timezone directly (like Europe/Prague), it specifies "timezone type". Allowed values are "PUBLISHER", "PROPOSAL_LOCAL" and "AD_EXCHANGE".

#### Example:

```
"timezone": "AD_EXCHANGE"
```

### metrics and dimensions

Using this configuration directive, you are able to define your custom metrics and dimensions. If this configuration is omitted, extractor will use default values.

This is the defaults:

```
DEFAULT_DIMENSIONS = [
    'AD_EXCHANGE_DFP_AD_UNIT',
    'AD_EXCHANGE_PRICING_RULE_NAME',
]

DEFAULT_METRICS = [
    'AD_EXCHANGE_AD_REQUESTS',
    'AD_EXCHANGE_MATCHED_REQUESTS',
    'AD_EXCHANGE_ESTIMATED_REVENUE',
    'AD_EXCHANGE_IMPRESSIONS',
]
```

For full list of allowed entries please see [official documentation](https://developers.google.com/ad-manager/api/reference/v202008/ReportService.ReportQuery)

#### Example:

```
"metrics": ["AD_EXCHANGE_AD_REQUESTS", "AD_EXCHANGE_MATCHED_REQUESTS"]
"dimensions": ["AD_EXCHANGE_PRICING_RULE_NAME"]
```

## Run extractor in local environment

If you want to test this extractor outside of Keboola, manually create `config/config.json` file (use template in `config/config.template.json`). Parameters prefixed by "#" are considered private.

After creating config file simply run

```
docker-compose up
```

Downloaded data will be stored into `output/output.csv` file.


## DOC

https://developers.google.com/ad-manager/api/start#python
https://developers.google.com/ad-manager/api/start#enable_api
https://developers.google.com/ad-manager/api/reference/v202002/ReportService.Column
