import sys
import datetime
import yaml
import tempfile
from googleads import ad_manager
from googleads import errors
from googleads.common import ZeepServiceProxy


class AdManagerReportQueryExtractor:
    def __init__(self, date_from: datetime.date, date_to: datetime.date,
                 application_name: str, network_code: int,
                 extractor_version: str, timezone: str, private_key_file: str,
                 api_version: str):
        print(f"Extractor with version {extractor_version} is executed")

        self.date_from = date_from
        self.date_to = date_to
        print("Selected interval: %s - %s" % (self.date_from, self.date_to))

        self.timezone = timezone
        if timezone in ["PUBLISHER", "PROPOSAL_LOCAL"]:
            self.report_column_date = "DATE"
        elif timezone == "AD_EXCHANGE":
            self.report_column_date = "AD_EXCHANGE_DATE"

        client = ad_manager.AdManagerClient.LoadFromString(yaml.dump({
            "ad_manager": {
                "application_name": application_name,
                "network_code": network_code,
                "path_to_private_key_file": private_key_file
            }
        }))

        # disable caching
        client.cache = ZeepServiceProxy.NO_CACHE
        self.report_downloader = client.GetDataDownloader(version=api_version)

    def date_range(self):
        """
        Iterator for date in date_range

        Returns
        -------
        Single date inside date_range
        """

        for n in range(int((self.date_to - self.date_from).days) + 1):
            yield self.date_from + datetime.timedelta(n)

    def run_report(self, report_job: dict):
        """
        Create report in API and wait for it

        :param report_job: dict report configuration
        :return: report job ID
        """
        print("Report downloader is going to run the report")
        try:
            # Run the report and wait for it to finish.
            report_job_id = self.report_downloader.WaitForReport(report_job)
            return report_job_id
        except errors.AdManagerReportError as e:
            print('Failed to generate report. Error was: %s' % e)
            sys.exit()

    def download_report(self, report_job: dict):
        """
        Downloads report into tmp file

        :param report_job: report configuration
        :return: str path to downloaded report
        """

        report_file = tempfile.NamedTemporaryFile(
            mode='w+b', suffix='.csv', delete=False)
        report_job_id = self.run_report(report_job)

        print("Report downloader is going to download the report")
        self.report_downloader.DownloadReportToFile(
            report_job_id=report_job_id,
            export_format='CSV_DUMP',
            outfile=report_file,
            use_gzip_compression=False
        )

        report_file.close()
        print('Report job downloaded to: %s' % report_file.name)
        return report_file.name

    def download_data_to_temp_file(self, dimensions: list, metrics: list):
        """
        Get stats for all items between two dates

        :param dimensions: list

        :param metrics: list
        :return: str path to downloaded report
        """
        report_job = {
            'reportQuery': {
                'dimensions': dimensions + [self.report_column_date],
                'columns': metrics,
                'dateRangeType': 'CUSTOM_DATE',
                'startDate': self.date_from,
                'endDate': self.date_to,
                'timeZoneType': self.timezone,
                'adxReportCurrency': 'CZK',
            }
        }
        return self.download_report(report_job)

    @staticmethod
    def save_stats(original_path, new_path):
        print("Exporter is going to transform stats from binary to text file")
        with open(new_path, mode='wt', encoding='utf-8') as new_file:
            with open(original_path, mode='rb') as original_file:
                for line in original_file:
                    new_file.write(line.decode())
