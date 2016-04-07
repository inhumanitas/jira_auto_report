# coding: utf-8

from setuptools import setup, find_packages

setup(
    name='jira_auto_report',
    version='0.1',
    description='Automation for report launch',
    author='inhumanitas',
    packages=find_packages(),
    platforms='any',
    include_package_data=True,
    install_requires=['jira'],
    entry_points={
        'console_scripts': [
            'jira_auto_report = jira_auto_report.main:main',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: CLI Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
