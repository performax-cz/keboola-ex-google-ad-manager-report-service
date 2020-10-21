import sys

from extractor_gam import GoogleAdMangerExtractor
from config import Config

# Deprecation = May 2021
# Sunset = August 2021
API_VERSION = "v202008"

APPLICATION_NAME = "performax.ex-google-ad-manager-report-service"
OUTPUT_FILE = '/data/out/tables/output.csv'
EXTRACTOR_VERSION = "__VERSION__"


def main():
    print("Run the GAM Report Service Extractor")

    try:
        extractor = GoogleAdMangerExtractor(
            application_name=APPLICATION_NAME,
            extractor_version=EXTRACTOR_VERSION,
            api_version=API_VERSION,
            params=Config.load(),
        )
        extractor.download_report(OUTPUT_FILE)
    except ValueError as e:
        print(f"{e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
