import json

import dateparser
from keboola import docker
from exporter import AdManagerReportQueryExtractor

OUTPUT_FILE = '/data/out/tables/output.csv'
EXTRACTOR_VERSION = "__VERSION__"

# Deprecation = May 2021
# Sunset = August 2021
API_VERSION = "v202008"
APPLICATION_NAME = "keboola.performax.ex-ad-manager"


class Config:
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
            dimensions = Config.DEFAULT_DIMENSIONS
        if not metrics:
            print("Metrics are empty. Extractor will continue with"
                  " default values")
            metrics = Config.DEFAULT_METRICS

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
            params, Config.PRIVATE_KEY_FILE
        )

        allowed_timezones = ('PUBLISHER', 'PROPOSAL_LOCAL', 'AD_EXCHANGE')
        if params['timezone'] not in allowed_timezones:
            raise ValueError(
                f"Invalid timezone. Choose from {allowed_timezones}"
            )

        return params


def main():
    print(f"Version of Ad Manager API: {API_VERSION}")
    params = Config.load()

    extractor = AdManagerReportQueryExtractor(
        application_name=APPLICATION_NAME,
        extractor_version=EXTRACTOR_VERSION,
        api_version=API_VERSION,
        network_code=params["network_code"],
        date_from=params["date_from"],
        date_to=params["date_to"],
        timezone=params["timezone"],
        private_key_file=params["private_key_file"],
    )

    tmp_file = extractor.download_data_to_temp_file(
        params['dimensions'], params['metrics']
    )

    extractor.save_stats(tmp_file, OUTPUT_FILE)


if __name__ == "__main__":
    print("Extractor is going to get all data from Google Ad Manager")
    main()
