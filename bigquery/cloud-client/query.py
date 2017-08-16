#!/usr/bin/env python

# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Command-line application to perform queries in BigQuery.

For more information, see the README.rst.

Example invocation:
    $ python query.py '#standardSQL
          SELECT corpus
          FROM `publicdata.samples.shakespeare`
          GROUP BY corpus
          ORDER BY corpus'
"""

import argparse
import uuid

from google.cloud import bigquery


def query(query):
    client = bigquery.Client()
    query_job = client.run_async_query(str(uuid.uuid4()), query)

    query_job.begin()
    query_job.result()  # Wait for job to complete.

    # Print the results.
    destination_table = query_job.destination
    destination_table.reload()
    for row in destination_table.fetch_data():
        print(row)


def query_standard_sql(query):
    client = bigquery.Client()
    query_job = client.run_async_query(str(uuid.uuid4()), query)
    # Set use_legacy_sql to False to use standard SQL syntax. See:
    # https://cloud.google.com/bigquery/docs/reference/standard-sql/enabling-standard-sql
    query_job.use_legacy_sql = False

    query_job.begin()
    query_job.result()  # Wait for job to complete.

    # Print the results.
    destination_table = query_job.destination
    destination_table.reload()
    for row in destination_table.fetch_data():
        print(row)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('query', help='BigQuery SQL Query.')
    parser.add_argument(
        '--use_standard_sql',
        action='store_true',
        help='Use standard SQL syntax.')

    args = parser.parse_args()

    if args.use_standard_sql:
        query_standard_sql(args.query)
    else:
        query(args.query)
