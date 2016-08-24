# -*- coding: utf-8 -*-

""" Setup file for EMS Data Tool. """

from setuptools import find_packages
from setuptools import setup

def main():
    """ Performs setup related package tasks. """

    setup(
        name="EMSUpdate",
        description="Updates user records for ODoS EMS database.",
        version="0.0.1",
        author="Alex Seidel",
        author_email="als3ak@virginia.edu",
        install_requires=[
            "openpyxl>=2.2.3",
            "pyodbc>=3.0.6",
            "requests>=2.7.0",
            "pysmb>=1.1.16",
            "unidecode>=0.4.19",
            ],
        entry_points={
            "console_scripts": [
                "update_ems_staging = bin.ems_update:main",
                "update_ems = bin.hrtk_helper:main",
                "get_departments = bin.get_departments:main",
                "check_database = bin.check_database:main",
            ],
        },
        packages=find_packages(),
        package_data={"": ["config/settings_template.ini"]},
        test_suite="nose.collector",
        setup_requires=[
            "nose>=1.3.7"
            ]
        )

if __name__ == "__main__":
    main()
