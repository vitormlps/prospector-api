from typing import List, Any
from datetime import datetime, date


class Filter:
    def __init__(self, key: str, values: List[Any] | Any):
        """
        :param key: Class attribute to compare with values
        :param values: Values to compare with key

        Example:
        Filter(key="status", values=["FINISHED", "WAITING"])
        """

        self.key = key
        self.values = values if isinstance(values, list) else [values]


class FilterJoin:
    def __init__(
            self,
            class_: object,
            class_attr: object,
            join_attr: object,
            values: List[Any] | Any = None,
            class_key: str = "id",
    ):
        """
        :param class_: Class to join
        :param class_attr: Class attribute to compare with join_attr
        :param join_attr: Class attribute to compare with class_attr
        :param values: Values to compare with class_key
        :param class_key: Class attribute to compare with values

        Example:

        # Filter Inspections by Mission id
        FilterJoin(
            class_=Mission,
            class_attr=Mission.inspection_id,
            join_attr=Inspection.id,
            values=[1, 2, 3],
            class_key="id"
        )
        """

        self.class_ = class_
        self.class_attr = class_attr
        self.join_attr = join_attr
        self.values = values if isinstance(values, list) else [values]
        self.class_key = class_key


class FilterDateBetween:
    def __init__(self, key: datetime | date, start: datetime | date, end: datetime | date):
        """
        :param key: Class attribute to compare with dates
        :param start: Start date
        :param end: End date

        Example:
        FilterBetween(key="created_at", start=datetime(2021, 1, 1), end=datetime(2021, 1, 31))
        """
        self.key = key
        self.start = start
        self.end = end
