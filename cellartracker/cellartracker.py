"""Main module."""
import csv
import logging

from io import StringIO

from .client import CellarTrackerClient
from .enum import CellarTrackerFormat, CellarTrackerTable

_LOGGER = logging.getLogger(__name__)

class CellarTracker(object):
    """
    CellarTracker is the class handling the CellarTracker data export.
    """

    def __init__(self, username: None, password: None):
        if username and password:
            self.client = CellarTrackerClient(username, password)
        elif username or password:
            _LOGGER.warning('Either username or password missing, not using authentication.')

    def get_list(self):
        """Get list data."""
        return self.get_data(table=CellarTrackerTable.List)

    def get_availability(self):
        """Get availability data."""
        return self.get_data(table=CellarTrackerTable.Availability)

    def get_bottles(self):
        """Get bottles data."""
        return self.get_data(table=CellarTrackerTable.Bottles)

    def get_data(self, table:CellarTrackerTable):
        """Get data."""
        return _parse_data(self.client.get(table=table, format=CellarTrackerFormat.tab))


def _parse_data(data:str):
    reader = csv.DictReader(StringIO(data), dialect="excel-tab")
    results = []
    for row in reader:
        result = {}
        for key, value in row.items():
            result[key] = value

        results.append(result)

    return results
