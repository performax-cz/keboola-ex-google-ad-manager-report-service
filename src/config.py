import json
import dateparser
from keboola import docker

DEFAULT_MAX_RETRIES = 5
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
    def private_key_file(params: dict, path: str) -> str:
        with open(path, 'w') as outfile:
            json.dump({
                "private_key": params["#private_key"],
                "client_email": params["#client_email"],
                "token_uri": params["token_uri"]
            }, outfile)
        return path

    @staticmethod
    def load() -> dict:
        cfg = docker.Config('/data/')
        params = cfg.get_parameters()

        # validate timezone type
        allowed_timezones = ('PUBLISHER', 'PROPOSAL_LOCAL', 'AD_EXCHANGE')
        if params['timezone'] not in allowed_timezones:
            raise ValueError(
                f"Invalid timezone. Choose from {allowed_timezones}"
            )

        # handle default dimensions
        if "dimensions" not in params:
            print("Dimensions field is empty -> use default")
            params['dimensions'] = DEFAULT_DIMENSIONS

            # add date column to dimensions - depends on timezone type
            if params["timezone"] in ("PUBLISHER", "PROPOSAL_LOCAL"):
                params['dimensions'].append("DATE")
            elif params["timezone"] == "AD_EXCHANGE":
                params['dimensions'].append("AD_EXCHANGE_DATE")

        print(f"Selected dimensions: {params['dimensions']}")

        # handle default metrics
        if "metrics" not in params:
            print("Metrics field is empty -> use default")
            params['metrics'] = DEFAULT_METRICS

        print(f"Selected metrics: {params['metrics']}")

        # parse date range
        try:
            params['date_from'] = dateparser.parse(params['date_from']).date()
            params['date_to'] = dateparser.parse(params['date_to']).date()
        except Exception:
            raise ValueError("Invalid date format")

        # create file with private key
        key_file = "/tmp/private_key.json"
        params['private_key_file'] = Config.private_key_file(params, key_file)

        # set max retries count for retryable decorator
        if 'max_retries' not in params:
            params["max_retries"] = DEFAULT_MAX_RETRIES

        if 'currency' not in params:
            params["currency"] = "CZK"

        return params
