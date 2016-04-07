INSTALLATION
============

# Getting sources
    $ git clone https://github.com/inhumanitas/jira_auto_report

# Install package
    $ cd jira_auto_report
    $ python setup.py install

    
SET VARIABLES
=============

Edit before installation settings file 

    $ vi jira_auto_report.settings

Edit settings:

    jira_url = 'http://jira.cg.ru'
    project_id = 12533
    login, passwd = 'login', 'pass'


USAGE
=====

After installation in environment package installs script - jira_auto_report
Just run it to start download reports:

    $ jira_auto_report

