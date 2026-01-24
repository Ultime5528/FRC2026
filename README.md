# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/Ultime5528/FRC2026/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                            |    Stmts |     Miss |   Branch |   BrPart |   Cover |   Missing |
|------------------------------------------------ | -------: | -------: | -------: | -------: | ------: | --------: |
| commands/\_\_init\_\_.py                        |        0 |        0 |        0 |        0 |    100% |           |
| commands/diagnostics/\_\_init\_\_.py            |        0 |        0 |        0 |        0 |    100% |           |
| commands/diagnostics/drivetrain/\_\_init\_\_.py |        9 |        1 |        0 |        0 |     89% |        12 |
| commands/diagnostics/drivetrain/odometry.py     |       36 |       24 |       10 |        0 |     26% |13-19, 22-24, 27-34, 37, 40-49 |
| commands/diagnostics/drivetrain/swerve.py       |       53 |       29 |        4 |        0 |     42% |21-29, 32, 35, 38-41, 44, 47-52, 65-79, 82-83, 86-88 |
| commands/diagnostics/utils/\_\_init\_\_.py      |        0 |        0 |        0 |        0 |    100% |           |
| commands/diagnostics/utils/setrunningtest.py    |       15 |        5 |        0 |        0 |     67% |13-15, 18, 21 |
| commands/drivetrain/\_\_init\_\_.py             |        0 |        0 |        0 |        0 |    100% |           |
| commands/drivetrain/drive.py                    |       54 |       34 |       14 |        0 |     29% |13-17, 21-24, 37-42, 45, 48-87, 90 |
| commands/drivetrain/driverelative.py            |       37 |       18 |        0 |        0 |     51% |11-13, 17-19, 23-25, 29-31, 34-37, 40, 43 |
| commands/drivetrain/resetgyro.py                |       20 |       11 |        2 |        0 |     41% |11-14, 17-25, 30 |
| commands/drivetrain/resetpose.py                |       13 |        6 |        0 |        0 |     54% |9-12, 15, 18 |
| conftest.py                                     |        1 |        0 |        0 |        0 |    100% |           |
| modules/\_\_init\_\_.py                         |        0 |        0 |        0 |        0 |    100% |           |
| modules/autonomous.py                           |       34 |       15 |        4 |        0 |     50% |20, 25-49, 52, 55-61, 64-65 |
| modules/control.py                              |       12 |        7 |        0 |        0 |     42% |     11-27 |
| modules/dashboard.py                            |       47 |       31 |       12 |        0 |     27% |22-29, 32, 39-42, 47-64, 70-87 |
| modules/hardware.py                             |       16 |        8 |        0 |        0 |     50% |     12-22 |
| modules/logging.py                              |       24 |       13 |        4 |        0 |     39% |12, 19-28, 31, 35-41 |
| modules/propertysavechecker.py                  |       35 |       26 |       16 |        0 |     18% |12-26, 29-47 |
| modules/questtagvision.py                       |       38 |       22 |        2 |        0 |     40% |22-25, 28-37, 44, 47, 50-64 |
| modules/tagvision.py                            |       35 |       35 |        6 |        0 |      0% |      1-61 |
| ports.py                                        |       17 |        0 |        0 |        0 |    100% |           |
| properties.py                                   |       85 |       72 |       18 |        1 |     14% |17-24, 34-58, 62-78, 82-127, 131-158 |
| robot.py                                        |       23 |       12 |        0 |        0 |     48% |     17-37 |
| subsystems/\_\_init\_\_.py                      |        0 |        0 |        0 |        0 |    100% |           |
| subsystems/drivetrain.py                        |      170 |      118 |       14 |        0 |     28% |50-201, 218-229, 234-259, 267, 270, 273, 276, 282-283, 291-300, 308-317, 322-325, 330-341, 344-388, 391-405, 411-418, 421, 438-439, 442, 445-460 |
| tests/\_\_init\_\_.py                           |        0 |        0 |        0 |        0 |    100% |           |
| tests/test\_common.py                           |        1 |        0 |        0 |        0 |    100% |           |
| ultime/\_\_init\_\_.py                          |        0 |        0 |        0 |        0 |    100% |           |
| ultime/affinecontroller.py                      |       77 |       77 |        2 |        0 |      0% |     1-122 |
| ultime/alert.py                                 |       90 |       26 |       14 |        0 |     65% |19-20, 24, 27, 44, 74-85, 88, 91-100, 103, 106, 136-137, 140 |
| ultime/auto.py                                  |        5 |        5 |        0 |        0 |      0% |       1-7 |
| ultime/autoproperty.py                          |       57 |       36 |       22 |        1 |     28% |33-35, 39, 52-105 |
| ultime/axistrigger.py                           |        8 |        8 |        2 |        0 |      0% |      1-16 |
| ultime/command.py                               |       71 |       43 |        4 |        0 |     37% |23-51, 56-58, 61, 64, 85-90, 94, 97-101, 104, 107, 110-111, 114-115 |
| ultime/coroutinecommand.py                      |       27 |       27 |        6 |        0 |      0% |      1-41 |
| ultime/dynamicmotion.py                         |       55 |       55 |       14 |        0 |      0% |     1-175 |
| ultime/gyro.py                                  |      123 |       69 |        2 |        0 |     43% |20, 25-26, 41, 44, 47, 50-52, 57-63, 66, 69, 72, 75, 80-84, 87, 90, 93, 96, 103-114, 119, 124, 129, 132, 135-136, 139-154, 163-167, 170, 173, 176, 179, 184-193, 196, 199, 202-203, 206-207, 210, 213 |
| ultime/immutable.py                             |        6 |        2 |        0 |        0 |     67% |      3, 8 |
| ultime/linearinterpolator.py                    |       25 |       25 |        6 |        0 |      0% |      1-36 |
| ultime/module.py                                |       81 |       19 |       20 |        2 |     79% |18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54, 57, 60, 63, 66, 69, 97, 109->108 |
| ultime/modulerobot.py                           |       45 |       22 |        4 |        0 |     47% |13-14, 17, 20-23, 26-29, 32, 35, 38, 41, 44, 47, 50, 53, 56, 59, 62, 65, 68 |
| ultime/proxy.py                                 |       19 |        0 |        2 |        0 |    100% |           |
| ultime/questnav/\_\_init\_\_.py                 |        0 |        0 |        0 |        0 |    100% |           |
| ultime/questnav/generated/\_\_init\_\_.py       |        0 |        0 |        0 |        0 |    100% |           |
| ultime/questnav/generated/commands\_pb2.py      |       23 |       10 |        2 |        1 |     56% |     28-39 |
| ultime/questnav/generated/data\_pb2.py          |       19 |        6 |        2 |        1 |     67% |     28-35 |
| ultime/questnav/generated/geometry2d\_pb2.py    |       28 |       28 |        2 |        0 |      0% |      7-44 |
| ultime/questnav/generated/geometry3d\_pb2.py    |       26 |       14 |        2 |        1 |     46% |     29-42 |
| ultime/questnav/questnav.py                     |      116 |       92 |       20 |        0 |     18% |87-119, 149-228, 259-290, 299, 315, 326-327, 336, 345, 356-357, 372, 393 |
| ultime/subsystem.py                             |       26 |       17 |        4 |        0 |     30% | 13, 18-39 |
| ultime/swerve.py                                |      117 |       87 |        8 |        0 |     24% |31-70, 73, 76, 81-107, 110, 117-132, 135-136, 139-140, 143, 146, 149, 152, 158, 164, 170-192, 204-209, 212-293 |
| ultime/swerveconfig.py                          |       67 |        0 |        0 |        0 |    100% |           |
| ultime/switch.py                                |       66 |        8 |       42 |        7 |     86% |29->exit, 41, 53, 57, 67, 71, 81, 84, 87 |
| ultime/tests/\_\_init\_\_.py                    |        9 |        0 |        0 |        0 |    100% |           |
| ultime/tests/test\_alert.py                     |       39 |       34 |        0 |        0 |     13% |8-42, 50-73 |
| ultime/tests/test\_commands.py                  |       75 |       15 |       54 |        7 |     83% |61->53, 63-66, 75-78, 79->69, 81-84, 99, 100->97, 114-136 |
| ultime/tests/test\_modules.py                   |       48 |        1 |        0 |        0 |     98% |        17 |
| ultime/tests/test\_properties.py                |        3 |        0 |        0 |        0 |    100% |           |
| ultime/tests/test\_proxy.py                     |       27 |        0 |        0 |        0 |    100% |           |
| ultime/tests/test\_subsystems.py                |       17 |        0 |        8 |        0 |    100% |           |
| ultime/tests/test\_switch.py                    |       33 |        0 |        0 |        0 |    100% |           |
| ultime/tests/test\_timethis.py                  |        3 |        0 |        0 |        0 |    100% |           |
| ultime/tests/utils.py                           |       74 |       42 |       10 |        0 |     45% |28-29, 37, 40-44, 47-51, 54-58, 61-65, 68-69, 72-73, 76-84, 87-93, 98-99 |
| ultime/timethis.py                              |       63 |       45 |       16 |        1 |     24% |20-45, 53-57, 61-93, 97-100 |
| ultime/trapezoidalmotion.py                     |       98 |       98 |       42 |        0 |      0% |     1-210 |
| ultime/vision.py                                |       91 |       91 |       28 |        0 |      0% |     1-154 |
| **TOTAL**                                       | **2532** | **1489** |  **444** |   **22** | **39%** |           |


## Setup coverage badge

Below are examples of the badges you can use in your main branch `README` file.

### Direct image

[![Coverage badge](https://raw.githubusercontent.com/Ultime5528/FRC2026/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/Ultime5528/FRC2026/blob/python-coverage-comment-action-data/htmlcov/index.html)

This is the one to use if your repository is private or if you don't want to customize anything.

### [Shields.io](https://shields.io) Json Endpoint

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/Ultime5528/FRC2026/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/Ultime5528/FRC2026/blob/python-coverage-comment-action-data/htmlcov/index.html)

Using this one will allow you to [customize](https://shields.io/endpoint) the look of your badge.
It won't work with private repositories. It won't be refreshed more than once per five minutes.

### [Shields.io](https://shields.io) Dynamic Badge

[![Coverage badge](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=coverage&query=%24.message&url=https%3A%2F%2Fraw.githubusercontent.com%2FUltime5528%2FFRC2026%2Fpython-coverage-comment-action-data%2Fendpoint.json)](https://htmlpreview.github.io/?https://github.com/Ultime5528/FRC2026/blob/python-coverage-comment-action-data/htmlcov/index.html)

This one will always be the same color. It won't work for private repos. I'm not even sure why we included it.

## What is that?

This branch is part of the
[python-coverage-comment-action](https://github.com/marketplace/actions/python-coverage-comment)
GitHub Action. All the files in this branch are automatically generated and may be
overwritten at any moment.