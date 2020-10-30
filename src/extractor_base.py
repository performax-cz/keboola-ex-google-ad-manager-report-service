import datetime
import time


class BaseExtractor:

    def __init__(self, date_from: datetime.date, date_to: datetime.date,
                 extractor_version: str, max_retries: int):
        self.date_from = date_from
        self.date_to = date_to
        self.max_retries = max_retries
        print(f"[INFO]: Extractor {extractor_version} is executed")
        print(f"[INFO]: Selected interval: {self.date_from} - {self.date_to}")

    def date_range(self):
        """Iterator for date in date range"""
        for n in range(int((self.date_to - self.date_from).days) + 1):
            yield self.date_from + datetime.timedelta(n)

    @staticmethod
    def retryable(func):
        """Allows to retry (param max_retries) methods which are unstable"""
        def func_wrapper(self, *args, **kwargs):
            for i in range(1, self.max_retries + 2):
                try:
                    return func(self, *args, **kwargs)
                except Exception as ex:
                    if i > self.max_retries:
                        raise ex
                    sleep_time = i * 2
                    print(
                        "Error while getting the data from source:"
                        " exporter is going to sleep for %s seconds"
                        " and retry it again (%s/%s)" % (
                            sleep_time, i, self.max_retries
                        )
                    )
                    time.sleep(sleep_time)
        return func_wrapper
