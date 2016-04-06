# coding: utf-8

from __future__ import unicode_literals

import urllib
import urlparse
import re

from jira import JIRA

from options import jira_url, login, passwd, project_id, get_period


class Report(object):
    # extract url to zip file
    url_re = re.compile(r'URL=(/reports/[\w.]+/\w+.zip)">')
    # file name for downloaded report
    report_filename = ''
    # report getter url
    report_url_template = None

    def __init__(self, jira, project_id, start_date, end_date):

        super(Report, self).__init__()
        self.jira_cli = jira
        date_fmt = '%d/%b/%y'
        self.start_date = start_date.strftime(date_fmt)
        self.end_date = end_date.strftime(date_fmt)
        self.project_id = project_id

    def get_zip_url(self):
        report_url = self.report_url_template.format(**{
            'startDate': self.start_date,
            'endDate': self.end_date,
            'project_id': project_id,
        })
        full_url = urlparse.urljoin(jira_url, report_url)
        response = self.jira_cli._session.get(full_url)
        zip_url = None
        if response.status_code == 200:
            zip_urls = re.findall(self.url_re, response.text)
            zip_url = (urlparse.urljoin(self.jira_cli._options['server'],
                                        zip_urls[0])
                       if zip_urls else None)
        return zip_url

    def save_report(self):
        zip_url = self.get_zip_url()
        if zip_url:
            zip_file = urllib.urlopen(zip_url)
            with open(self.report_filename, 'wb') as f:
                f.write(zip_file.read())
            return self.report_filename


class WorkProjectByStaffReport(Report):
    report_filename = 'Трудозатраты проекта (по сотрудникам).zip'

    report_url_template = (
        'secure/ConfigureReport.jspa?'
        'startDate={startDate}&endDate={endDate}&'
        'project=&selectedProjectId={project_id}&'
        'reportKey=ru.cg.jirareport.plugin:WorkProjectByStaff&'
        'Next=Next')


class WorkProjectByStaffAllReport(Report):
    report_filename = 'Трудозатраты проекта (по сотрудникам) ALL.zip'

    report_url_template = (
        'secure/ConfigureReport.jspa?'
        'startDate={startDate}&endDate={endDate}&'
        'checkbox=true&'
        'project=&selectedProjectId={project_id}&'
        'reportKey=ru.cg.jirareport.plugin:WorkProjectByStaff&'
        'Next=Next')


class LoadControlReport(Report):
    report_filename = 'Контроль загрузки сотрудников с 9:00 до 18:00.xls'
    url_re = re.compile(r'URL=(/reports/[\w.]+/\w+ - LOAD_CONTROL.xls)">')
    report_url_template = (
        'secure/ConfigureReport.jspa?'
        'startDate={startDate}&endDate={endDate}&'
        'selectedProjectId={project_id}&'
        'reportKey=ru.cg.jirareport.plugin:LoadControl&'
        'Next=Next')


# jira_cg = JIRA(server=jira_url, basic_auth=(login, passwd))
# start_date, end_date = get_period()
#
# # r = WorkProjectByStaffReport(jira_cg, project_id, start_date, end_date)
# # r.save_report()
# # print r
# r = LoadControlReport(jira_cg, project_id, start_date, end_date)
# r.save_report()
# print r