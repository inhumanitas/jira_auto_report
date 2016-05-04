# coding: utf-8

from __future__ import unicode_literals

import logging
import os

from jira import JIRA
from jira_auto_report.notifiers import smpt_connection
try:
    from jira.exceptions import JIRAError
except ImportError:
    from jira import JIRAError
from jira_auto_report import settings
from jira_auto_report.reports import active_reports

logger = logging.getLogger(__name__)


def main():
    logger.info('Started jira auto report')

    try:
        jira_cg = JIRA(server=settings.jira_url,
                       basic_auth=(settings.login, settings.passwd))
    except JIRAError as e:
        logger.critical(e)
        logger.critical('Check authentication params')
        return
    # import datetime
    # start_date, end_date = settings.get_period(datetime.date(day=22, month=4, year=2016))

    start_date, end_date = settings.get_period()

    dir_name = (
        start_date.strftime(settings.dir_fmt) + '-' +
        end_date.strftime(settings.dir_fmt))
    report_file_dir = os.path.join(settings.base_dir, dir_name)

    logger.info('Report file dir')
    logger.info(report_file_dir)

    if os.path.exists(report_file_dir):
        logger.critical('Skipping report requests, path exists: {0}'.format(
            report_file_dir))
    else:
        os.makedirs(report_file_dir)

        for report in active_reports:
            logger.debug('Process report')
            logger.debug(report)

            r = report(jira_cg, settings.project_id, start_date, end_date,
                       base_dir=report_file_dir)
            r.save_report()

    if settings.recipient:
        logger.info('Sending mails')
        file_list = report_file_dir + '\n'
        deep = 0
        for root, dirs, files in os.walk(report_file_dir):
            deep += 1
            offset = deep * '\t'
            for file_name in dirs+files:
                try:
                    file_name = file_name.decode('utf-8')
                except UnicodeEncodeError:
                    pass

                file_list += offset + file_name + '\n'

        # TODO refactor notifiers
        msg = settings.mail_message_temlate.format(
            begin=start_date,
            end=end_date,
            file_list=file_list
        )

        mail_subject = settings.mail_subject_template.format(
            begin=start_date,
            end=end_date)

        with smpt_connection(settings.mail_server_url,
                             settings.user_mail,
                             settings.user_password) as server:
            server.send_email(
                settings.from_mail, settings.recipient, mail_subject, msg)

if __name__ == '__main__':
    # TODO parse date in arguments
    main()
