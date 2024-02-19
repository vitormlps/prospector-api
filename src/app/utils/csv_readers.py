#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
import csv
from datetime import date

# ### Third-party deps

# ### Local deps


def read_csv_file(csv_file, delimiter):
    table = csv.DictReader(csv_file, delimiter=delimiter)
    result = []

    for row in table:
        _id = row["id"]
        name = row['nome'] if len(row['nome']) > 0 else "Sem nome"

        result.append({
            'id': _id,
            'name': name,
            'field': row['field'],
        })

    if len(result) == 0:
        return {"error": "No valid data found in the uploaded file."}

    return result
