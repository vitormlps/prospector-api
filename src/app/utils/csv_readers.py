#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
import csv

# ### Third-party deps
# ### Local deps


def read_csv_file(csv_file_path, delimiter=";"):
    result_table = []

    with open(csv_file_path, encoding="latin-1") as csv_file:
        raw_table = csv.reader(csv_file, delimiter=delimiter)
        result_table.extend(raw_table)

    return result_table
