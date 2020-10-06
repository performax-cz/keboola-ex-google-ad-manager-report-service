import json
import dateparser
from keboola import docker


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
    def load(default_max_retries: int, default_dimensions: list,
             default_metrics: list):
        cfg = docker.Config('/data/')
        params = cfg.get_parameters()
        dimensions = params.get("dimensions")
        metrics = params.get("metrics")

        # validate timezone type
        allowed_timezones = ('PUBLISHER', 'PROPOSAL_LOCAL', 'AD_EXCHANGE')
        if params['timezone'] not in allowed_timezones:
            raise ValueError(
                f"Invalid timezone. Choose from {allowed_timezones}"
            )

        # handle default dimensions
        if not dimensions:
            print("Dimensions are empty. Extractor will continue with"
                  " default values")
            dimensions = default_dimensions

            # add date column to dimensions - depends on timezone type
            if params["timezone"] in ("PUBLISHER", "PROPOSAL_LOCAL"):
                dimensions.append("DATE")
            elif params["timezone"] == "AD_EXCHANGE":
                dimensions.append("AD_EXCHANGE_DATE")
        print("Dimensions: %s" % dimensions)
        params['dimensions'] = dimensions

        # handle default metrics
        if not metrics:
            print("Metrics are empty. Extractor will continue with"
                  " default values")
            metrics = default_metrics
        print("Metrics: %s" % metrics)
        params['metrics'] = metrics

        # parse date range
        try:
            params['date_from'] = dateparser.parse(params['date_from']).date()
            params['date_to'] = dateparser.parse(params['date_to']).date()
        except Exception:
            raise ValueError(
                "Date format is wrong. Find dateparser"
                " library on pypi for more information."
            )

        # create file with private key
        key_file = "/tmp/private_key.json"
        params['private_key_file'] = Config.private_key_file(params, key_file)

        # set max retries count for retryable decorator
        if 'max_retries' not in params:
            params["max_retries"] = default_max_retries

        return params
