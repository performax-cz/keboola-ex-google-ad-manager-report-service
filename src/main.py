from ad_manager_extractor import AdManagerReportQueryExtractor
from config import Config

OUTPUT_FILE = '/data/out/tables/output.csv'
EXTRACTOR_VERSION = "__VERSION__"

# Deprecation = May 2021
# Sunset = August 2021
API_VERSION = "v202008"
APPLICATION_NAME = "performax.ex-ad-manager-report-service"


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
        max_retries=params["max_retries"]
    )

    tmp_file = extractor.download_data_to_temp_file(
        params['dimensions'], params['metrics']
    )

    extractor.save_stats(tmp_file, OUTPUT_FILE)


if __name__ == "__main__":
    print("Extractor is going to get all data from Google Ad Manager")
    main()
