# coding: utf-8

from __future__ import unicode_literals

import urllib
import urlparse
import os
import re
import logging

logger = logging.getLogger(__name__)


class Report(object):
    # extract url to zip file
    url_re = re.compile(r'URL=(/reports/[\w.]+/\w+.zip)">')
    # file name for downloaded report
    report_filename = ''
    # report plugin
    jira_report_plugin = None
    # checkbox argument
    checked = False
    # additional params to url
    options = None
    # date format in url request
    date_agrs_fmt = '%d/%b/%y'
    # report getter url
    __report_url_template = (
        'secure/ConfigureReport.jspa?'
        'startDate={startDate}&endDate={endDate}&'
        'project=&selectedProjectId={project_id}&'
        '{options}'
        'reportKey=ru.cg.jirareport.plugin:{plugin}&'
        'Next=Next')

    def __init__(self, jira, project_id, start_date, end_date, base_dir='',
                 options=None):
        """ Base for all reports.
        :param jira: Jira instance
        :type jira: jira.JIRA
        :param project_id: project id in jira system
        :param start_date: report beginning period
        :param end_date: report ends period
        :param base_dir: dir to export reports
        """

        super(Report, self).__init__()

        self.jira_cli = jira
        self.jira_url = self.jira_cli._options['server']

        self.start_date = start_date
        self.end_date = end_date
        self.start_date_arg = start_date.strftime(self.date_agrs_fmt)
        self.end_date_arg = end_date.strftime(self.date_agrs_fmt)
        self.project_id = project_id
        self.base_dir = base_dir
        self.options = options or {}

        if self.checked:
            self.options['checkbox'] = 'true'

    def __repr__(self):
        return self.__class__.__name__

    @property
    def report_url(self):
        report_url = self.__report_url_template.format(**{
            'startDate': self.start_date_arg,
            'endDate': self.end_date_arg,
            'project_id': self.project_id,
            'plugin': self.jira_report_plugin,
            'options': (''.join(
                [str(k)+'='+str(v)+'&' for k, v in self.options.items()])
                if self.options else ''
            ),
        })
        return report_url

    @property
    def report_file_path(self):
        return os.path.join(self.base_dir, self.report_filename)

    def get_zip_url(self):
        full_url = urlparse.urljoin(self.jira_url, self.report_url)
        logger.info('Processing url for report {0}'.format(full_url))

        response = self.jira_cli._session.get(full_url)
        zip_url = None
        if response.status_code == 200:
            zip_urls = re.findall(self.url_re, response.text)
            zip_url = (urlparse.urljoin(self.jira_url, zip_urls[0])
                       if zip_urls else None)
        else:
            logger.critical('Stauts code {0}: {1}'.format(
                response.status_code, response.text))
        return zip_url

    def save_report(self):
        zip_url = self.get_zip_url()
        if not zip_url:
            logger.critical('No report url parsed! '
                            'Skipping report {0}'.format(self))
        else:
            logger.info('Downloading file {0}'.format(zip_url))
            zip_file = urllib.urlopen(zip_url)

            with open(self.report_file_path, 'wb') as f:
                f.write(zip_file.read())


class WorkProjectByStaffReport(Report):
    report_filename = 'Трудозатраты проекта (по сотрудникам).zip'
    jira_report_plugin = 'WorkProjectByStaff'


class WorkProjectByStaffAllReport(WorkProjectByStaffReport):
    report_filename = 'Трудозатраты проекта (по сотрудникам) ALL.zip'
    checked = True


class WorkProjectByStaffByUserReport(Report):
    report_filename = 'Трудозатраты проекта (по сотрудникам).zip'
    jira_report_plugin = 'WorkProjectByStaff'

    def __init__(self, jira, project_id, start_date, end_date,
                 base_dir='', username=''):
        super(WorkProjectByStaffByUserReport, self).__init__(
            jira, project_id, start_date, end_date, base_dir,
            options={'user': username})


class WorkProjectByTaskReport(Report):
    report_filename = 'Трудозатраты проекта по задачам.zip'
    jira_report_plugin = 'WorkProjectByTask'


class WorkProjectByTaskALLReport(WorkProjectByTaskReport):
    report_filename = 'Трудозатраты проекта по задачам ALL.zip'
    checked = True


class LoadControlReport(Report):
    report_filename = 'Контроль загрузки сотрудников с 9.00 до 18.00.xls'
    url_re = re.compile(r'URL=(/reports/[\w.]+/\w+ - LOAD_CONTROL.xls)">')
    jira_report_plugin = 'LoadControl'


class TimeSheetReport(Report):
    report_filename = 'табель учета рабочего времени.xls'
    url_re = re.compile(r'URL=(/reports/[\w.]+/\w+ - TimeSheetReport.xls)">')
    jira_report_plugin = 'report'


active_reports = [
    WorkProjectByStaffReport,
    WorkProjectByStaffAllReport,
    WorkProjectByTaskReport,
    WorkProjectByTaskALLReport,
    LoadControlReport,
    TimeSheetReport,
]
