from ad_manager_extractor import AdManagerReportQueryExtractor
from config import Config

OUTPUT_FILE = '/data/out/tables/output.csv'
EXTRACTOR_VERSION = "__VERSION__"

# Deprecation = May 2021
# Sunset = August 2021
API_VERSION = "v202008"
APPLICATION_NAME = "performax.ex-ad-manager-report-service"

MAX_RETRIES_DEFAULT = 5

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


def main():
    print(f"Version of Ad Manager API: {API_VERSION}")
    params = Config.load(
        default_max_retries=MAX_RETRIES_DEFAULT,
        default_dimensions=DEFAULT_DIMENSIONS,
        default_metrics=DEFAULT_METRICS
    )

    extractor = AdManagerReportQueryExtractor(
        application_name=APPLICATION_NAME,
        extractor_version=EXTRACTOR_VERSION,
        api_version=API_VERSION,
        network_code=params["network_code"],
        date_from=params["date_from"],
        date_to=params["date_to"],
        timezone=params["timezone"],
        private_key_file=params["private_key_file"],
        max_retries=params["max_retries"]
    )

    tmp_file = extractor.download_data_to_temp_file(
        params['dimensions'], params['metrics']
    )

    extractor.save_stats(tmp_file, OUTPUT_FILE)


if __name__ == "__main__":
    print("Extractor is going to get all data from Google Ad Manager")
    main()
