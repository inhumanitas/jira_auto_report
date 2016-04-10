# coding: utf-8

from __future__ import unicode_literals

import logging

import os
from jira import JIRA
try:
    from jira.exceptions import JIRAError
except ImportError:
    from jira import JIRAError

from jira_auto_report.settings import (
    jira_url, login, passwd, project_id, get_period, dir_fmt, base_dir)
from jira_auto_report.reports import active_reports

logger = logging.getLogger(__name__)


def main():
    try:
        jira_cg = JIRA(server=jira_url, basic_auth=(login, passwd))
    except JIRAError as e:
        logger.critical(e)
        raise

    start_date, end_date = get_period()

    dir_name = (
        start_date.strftime(dir_fmt) + '-' +
        end_date.strftime(dir_fmt))
    report_file_dir = os.path.join(base_dir, dir_name)

    if os.path.exists(report_file_dir):
        logger.critical('Skipping report requests, path exists: {0}'.format(
            report_file_dir))
    else:
        os.makedirs(report_file_dir)

        for report in active_reports:
            r = report(jira_cg, project_id, start_date, end_date,
                       base_dir=report_file_dir)
            r.save_report()


if __name__ == '__main__':
    main()
