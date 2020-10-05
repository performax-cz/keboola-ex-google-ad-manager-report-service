import json

import dateparser
from keboola import docker


MAX_RETRIES_DEFAULT = 5

PRIVATE_KEY_FILE = "/tmp/data.json"

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


class Config:
    @staticmethod
    def private_key_file(params, path):
        with open(path, 'w') as outfile:
            json.dump({
                "private_key": params["#private_key"],
                "client_email": params["#client_email"],
                "token_uri": params["token_uri"]
            }, outfile)
        return path

    @staticmethod
    def load():
        cfg = docker.Config('/data/')
        params = cfg.get_parameters()
        dimensions = params.get("dimensions")
        metrics = params.get("metrics")

        if not dimensions:
            print("Dimensions are empty. Extractor will continue with"
                  " default values")
            dimensions = DEFAULT_DIMENSIONS
        if not metrics:
            print("Metrics are empty. Extractor will continue with"
                  " default values")
            metrics = DEFAULT_METRICS

        print("Dimensions: %s" % dimensions)
        print("Metrics: %s" % metrics)

        try:
            params['date_from'] = dateparser.parse(params['date_from']).date()
            params['date_to'] = dateparser.parse(params['date_to']).date()
        except Exception:
            raise ValueError(
                "Date format is wrong. Find dateparser"
                " library on pypi for more information."
            )
        params['metrics'] = metrics
        params['dimensions'] = dimensions
        params['private_key_file'] = Config.private_key_file(
            params, PRIVATE_KEY_FILE
        )

        allowed_timezones = ('PUBLISHER', 'PROPOSAL_LOCAL', 'AD_EXCHANGE')
        if params['timezone'] not in allowed_timezones:
            raise ValueError(
                f"Invalid timezone. Choose from {allowed_timezones}"
            )

        if 'max_retries' not in params:
            params["max_retries"] = MAX_RETRIES_DEFAULT

        return params
