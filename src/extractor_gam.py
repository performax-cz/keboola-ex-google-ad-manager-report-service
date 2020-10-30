import sys
import yaml
import tempfile
from googleads import ad_manager
from googleads import errors
from googleads.common import ZeepServiceProxy
from extractor_base import BaseExtractor


class GoogleAdMangerExtractor(BaseExtractor):

    def __init__(self, application_name: str, extractor_version: str,
                 api_version: str, params: dict):

        super().__init__(
            date_from=params["date_from"],
            date_to=params["date_to"],
            extractor_version=extractor_version,
            max_retries=params["max_retries"],
        )

        self.timezone = params["timezone"]
        self.dimensions = params["dimensions"]
        self.metrics = params["metrics"]
        self.currency = params.get("currency")
        self.dimension_attributes = params.get("dimension_attributes")
        self.ad_unit_view = params.get("ad_unit_view")

        print(f"[INFO]: Version of Google Ad Manager API: {api_version}")

        try:
            client = ad_manager.AdManagerClient.LoadFromString(yaml.dump({
                "ad_manager": {
                    "application_name": application_name,
                    "network_code": params["network_code"],
                    "path_to_private_key_file": params["private_key_file"]
                }
            }))
        except ValueError as e:
            raise ValueError(
                f"{e} Please, check format of your private key. New lines"
                f" must be delimited by \\n character."
            )

        # disable caching
        client.cache = ZeepServiceProxy.NO_CACHE
        self.report_downloader = client.GetDataDownloader(version=api_version)

    def create_report(self, report_job: dict):
        """Create report via API"""
        try:
            # Run the report and wait for it to finish
            report_job_id = self.report_downloader.WaitForReport(report_job)
            return report_job_id
        except errors.AdManagerReportError as e:
            print('[INFO]: Failed to generate report. Error: %s' % e)
            sys.exit()

    # @BaseExtractor.retryable
    def download_report(self, path: str):
        """Download the report to file"""

        report_file = tempfile.NamedTemporaryFile(
            mode='w+b', suffix='.csv', delete=False
        )

        report_query = {
                'dimensions': self.dimensions,
                'columns': self.metrics,
                'dateRangeType': 'CUSTOM_DATE',
                'startDate': self.date_from,
                'endDate': self.date_to,
                'timeZoneType': self.timezone
            }

        if self.dimension_attributes:
            report_query['dimensionAttributes'] = self.dimension_attributes

        if self.ad_unit_view:
            report_query['adUnitView'] = self.ad_unit_view

        if self.currency:
            report_query['adxReportCurrency'] = self.currency

        report_job = {
            'reportQuery': report_query
        }

        print("[INFO]: Create the report")
        report_job_id = self.create_report(report_job)

        print("[INFO]: Download the report")
        self.report_downloader.DownloadReportToFile(
            report_job_id=report_job_id,
            export_format='CSV_DUMP',
            outfile=report_file,
            use_gzip_compression=False
        )

        report_file.close()
        print(f"[INFO]: Report downloaded to temporary file {report_file.name}")

        self.write_to_file(report_file.name, path)

    @staticmethod
    def write_to_file(original_path, new_path):
        """Write binary data from temporary file to output file"""
        print(f"[INFO]: Transform data from binary to text file {new_path}")
        with open(new_path, mode='wt', encoding='utf-8') as new_file:
            with open(original_path, mode='rb') as original_file:
                for line in original_file:
                    new_file.write(line.decode())
