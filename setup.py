#!/usr/bin/env python


import setuptools


# =====
if __name__ == "__main__":
    setuptools.setup(
        name="gns-helpers",
        version="0.2",
        url="https://github.com/yandex-sysmon/gns-helpers",
        license="LGPLv3",
        author="Devaev Maxim",
        author_email="mdevaev@gmail.com",
        description="Send methods and constants for GNS rules",
        platforms="any",

        packages=[
            "gnshelpers",
            "gnshelpers/output",
        ],

        classifiers=[  # http://pypi.python.org/pypi?:action=list_classifiers
            "Development Status :: 2 - Pre-Alpha",
            "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "Topic :: System :: Networking :: Monitoring",
        ],

        install_requires=[
            "python-dateutil >= 2.2",
            "golemapi >= 0.5",
            "gns >= 0.1",
            "raava >= 0.10",
        ]
    )
