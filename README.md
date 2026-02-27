# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/Ultime5528/FRC2026/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                              |    Stmts |     Miss |   Branch |   BrPart |   Cover |   Missing |
|-------------------------------------------------- | -------: | -------: | -------: | -------: | ------: | --------: |
| commands/\_\_init\_\_.py                          |        0 |        0 |        0 |        0 |    100% |           |
| commands/climber/\_\_init\_\_.py                  |        0 |        0 |        0 |        0 |    100% |           |
| commands/climber/maintainclimber.py               |        9 |        4 |        0 |        0 |     56% |  9-11, 14 |
| commands/climber/move.py                          |       44 |       10 |        0 |        0 |     77% |27-32, 36-41, 45-50, 53 |
| commands/drivetrain/\_\_init\_\_.py               |        0 |        0 |        0 |        0 |    100% |           |
| commands/drivetrain/auto/\_\_init\_\_.py          |        0 |        0 |        0 |        0 |    100% |           |
| commands/drivetrain/auto/alignpreciseafterpath.py |       32 |       18 |        4 |        0 |     39% |16-22, 25-37, 40-44, 47 |
| commands/drivetrain/auto/followpathprecise.py     |       11 |        5 |        0 |        0 |     55% |     10-15 |
| commands/drivetrain/auto/pathfindfollowpath.py    |       11 |        5 |        0 |        0 |     55% |     10-15 |
| commands/drivetrain/auto/pathfindprecise.py       |       11 |        5 |        0 |        0 |     55% |     10-15 |
| commands/drivetrain/drive.py                      |       54 |       34 |       14 |        0 |     29% |13-17, 21-24, 37-42, 45, 48-87, 90 |
| commands/drivetrain/driverelative.py              |       37 |       18 |        0 |        0 |     51% |11-13, 17-19, 23-25, 29-31, 34-37, 40, 43 |
| commands/drivetrain/forwardposition.py            |       20 |        9 |        0 |        0 |     55% |12-15, 18, 21, 24, 27-28 |
| commands/drivetrain/resetgyro.py                  |       20 |       11 |        2 |        0 |     41% |11-14, 17-25, 30 |
| commands/drivetrain/resetpose.py                  |       13 |        6 |        0 |        0 |     54% |9-12, 15, 18 |
| commands/feeder/\_\_init\_\_.py                   |        0 |        0 |        0 |        0 |    100% |           |
| commands/feeder/ejectfuel.py                      |       13 |        6 |        0 |        0 |     54% |7-9, 12, 15, 18 |
| commands/feeder/grabfuel.py                       |       13 |        6 |        0 |        0 |     54% |7-9, 12, 15, 18 |
| commands/guide.py                                 |       38 |        7 |        0 |        0 |     82% |29-34, 38-43, 46 |
| commands/hugger/\_\_init\_\_.py                   |        0 |        0 |        0 |        0 |    100% |           |
| commands/hugger/hug.py                            |       17 |        8 |        0 |        0 |     53% |9-12, 15, 18, 21, 24 |
| commands/hugger/unhug.py                          |       17 |        8 |        0 |        0 |     53% |9-12, 15, 18, 21, 24 |
| commands/pivot/\_\_init\_\_.py                    |        0 |        0 |        0 |        0 |    100% |           |
| commands/pivot/maintainpivot.py                   |       13 |        6 |        0 |        0 |     54% |7-9, 12, 15, 18 |
| commands/pivot/move.py                            |       38 |        7 |        0 |        0 |     82% |29-34, 38-43, 46 |
| commands/resetall.py                              |       12 |        1 |        0 |        0 |     92% |        15 |
| commands/shooter/\_\_init\_\_.py                  |        0 |        0 |        0 |        0 |    100% |           |
| commands/shooter/manualshoot.py                   |       27 |       12 |        2 |        0 |     52% |8-10, 13, 16, 19, 24, 27, 30-34 |
| commands/shooter/prepareshoot.py                  |       16 |        9 |        2 |        0 |     39% |7-10, 13-14, 17, 20-21 |
| commands/shooter/shoot.py                         |       17 |       10 |        2 |        0 |     37% |7-9, 12-18, 21, 24 |
| conftest.py                                       |        1 |        0 |        0 |        0 |    100% |           |
| modules/\_\_init\_\_.py                           |        0 |        0 |        0 |        0 |    100% |           |
| modules/autonomous.py                             |       28 |       12 |        4 |        0 |     50% |17, 22-28, 31-37, 40-41 |
| modules/control.py                                |       12 |        7 |        0 |        0 |     42% |     11-27 |
| modules/dashboard.py                              |      101 |       68 |       12 |        0 |     29% |39-46, 49, 56-122, 128-145, 151-168 |
| modules/hardware.py                               |       34 |       17 |        0 |        0 |     50% |20-38, 41-42 |
| modules/logging.py                                |       21 |       12 |        4 |        0 |     36% |11, 18-27, 31-37 |
| modules/propertysavechecker.py                    |       36 |       26 |       16 |        0 |     19% |13-27, 30-48 |
| modules/questvision.py                            |       37 |       22 |        2 |        0 |     38% |21-24, 27-36, 43, 46, 49-63 |
| modules/sysidmodule.py                            |       16 |        8 |        0 |        0 |     50% |    12-100 |
| modules/tagvision.py                              |       33 |       33 |        6 |        0 |      0% |      1-59 |
| ports.py                                          |       32 |        0 |        0 |        0 |    100% |           |
| properties.py                                     |       85 |       72 |       18 |        1 |     14% |17-24, 34-58, 62-78, 82-127, 131-158 |
| robot.py                                          |       23 |       11 |        0 |        0 |     52% |     18-40 |
| subsystems/\_\_init\_\_.py                        |        0 |        0 |        0 |        0 |    100% |           |
| subsystems/climber.py                             |       51 |       26 |        4 |        0 |     45% |26-54, 57, 60, 63, 66, 69, 72, 75, 78, 81, 84, 87, 90-96 |
| subsystems/drivetrain.py                          |      188 |      127 |       12 |        0 |     30% |49-217, 220, 223, 226, 243-254, 259-284, 292, 295, 298, 301, 307-308, 316-325, 333-342, 347-350, 355-366, 369-389, 392-415, 418-425, 431, 434, 451-452, 455, 458, 461, 465, 470, 475-479 |
| subsystems/feeder.py                              |       20 |        8 |        0 |        0 |     60% |14-20, 27, 30, 33 |
| subsystems/guide.py                               |       47 |       23 |        2 |        0 |     49% |18-40, 43-44, 47, 50, 53, 56, 59, 62, 65, 68, 71, 74, 77 |
| subsystems/hugger.py                              |       20 |        7 |        0 |        0 |     65% |16-18, 21-22, 25-26 |
| subsystems/pivot.py                               |       79 |       42 |       10 |        0 |     42% |36-69, 72-77, 80-82, 85, 88, 91, 94, 97, 100, 103, 106, 109, 112, 115-124, 127, 130-133 |
| subsystems/shooter.py                             |      124 |       81 |       28 |        0 |     28% |41-79, 82-83, 86-87, 90-106, 109-130, 133-135, 138-145, 148-156, 159-165, 168-174, 177, 182-189, 192, 195 |
| tests/\_\_init\_\_.py                             |        0 |        0 |        0 |        0 |    100% |           |
| tests/test\_climber.py                            |      136 |      112 |        0 |        0 |     18% |19-21, 25-28, 32-55, 66-108, 114-115, 128-129, 142-143, 156-157, 170-171, 184-185, 198-199, 212-213, 226-227, 238-257, 263-301, 307-320 |
| tests/test\_common.py                             |        1 |        0 |        0 |        0 |    100% |           |
| tests/test\_drivetrain.py                         |       77 |       60 |        0 |        0 |     22% |18-31, 35-42, 46-68, 72-108 |
| tests/test\_guide.py                              |       48 |       35 |        0 |        0 |     27% |10-13, 17-20, 24-42, 53-69, 73, 84, 95, 108 |
| tests/test\_hugger.py                             |       27 |       19 |        0 |        0 |     30% |8-10, 14-19, 23-29, 33-39 |
| tests/test\_resetall.py                           |       15 |       11 |        0 |        0 |     27% |      7-19 |
| tests/test\_shooter.py                            |       92 |       80 |        0 |        0 |     13% |13-15, 19-50, 54-81, 86-162 |
| ultime/\_\_init\_\_.py                            |        0 |        0 |        0 |        0 |    100% |           |
| ultime/affinecontroller.py                        |       77 |       77 |        2 |        0 |      0% |     1-122 |
| ultime/alert.py                                   |       88 |       53 |       14 |        0 |     34% |17-18, 22, 25, 30-32, 35, 38, 41-51, 62-69, 72-83, 86, 89-98, 101, 104, 108-114, 128-130, 133-134, 137 |
| ultime/auto.py                                    |        5 |        5 |        0 |        0 |      0% |       1-7 |
| ultime/autoproperty.py                            |       57 |       36 |       22 |        1 |     28% |33-35, 39, 52-105 |
| ultime/axistrigger.py                             |        8 |        8 |        2 |        0 |      0% |      1-16 |
| ultime/command.py                                 |       70 |       47 |        4 |        0 |     31% |14-18, 22-50, 55-57, 60, 63, 84-89, 93, 96-100, 103, 106, 109-110, 113-114 |
| ultime/control.py                                 |       15 |       11 |        4 |        0 |     21% |5-7, 11-13, 17-22 |
| ultime/coroutinecommand.py                        |       27 |       27 |        6 |        0 |      0% |      1-41 |
| ultime/dynamicmotion.py                           |       55 |       55 |       14 |        0 |      0% |     1-175 |
| ultime/gyro.py                                    |      123 |       69 |        2 |        0 |     43% |20, 25-26, 41, 44, 47, 50-52, 57-63, 66, 69, 72, 75, 80-84, 87, 90, 93, 96, 103-114, 119, 124, 129, 132, 135-136, 139-154, 163-167, 170, 173, 176, 179, 184-193, 196, 199, 202-203, 206-207, 210, 213 |
| ultime/immutable.py                               |        6 |        2 |        0 |        0 |     67% |      3, 8 |
| ultime/linear/\_\_init\_\_.py                     |        0 |        0 |        0 |        0 |    100% |           |
| ultime/linear/linearsubsystem.py                  |       98 |       63 |       16 |        0 |     31% |21-37, 40-44, 48, 52, 56, 60, 64, 68, 71, 75, 78, 84, 88, 92, 96, 99, 106, 113-118, 121-131, 134-158 |
| ultime/linear/manualmovelinear.py                 |       27 |       13 |        0 |        0 |     52% |10-12, 16-18, 21-24, 27, 30, 33 |
| ultime/linear/movelinear.py                       |       32 |       21 |        8 |        0 |     28% |18-24, 27, 37-39, 42-49, 52-57 |
| ultime/linear/resetlinear.py                      |       42 |       27 |       10 |        0 |     29% |10-12, 16-18, 26-31, 34, 37-48, 51-54, 57 |
| ultime/linearinterpolator.py                      |       25 |       25 |        6 |        0 |      0% |      1-36 |
| ultime/log.py                                     |      103 |       71 |       26 |        0 |     25% |10-11, 18, 21-27, 30-31, 37, 40-42, 45-56, 67-91, 96-102, 105-107, 110, 113-115, 120, 123-124, 127, 135, 138-143, 146, 150, 153-154, 157-158, 161 |
| ultime/module.py                                  |       81 |       21 |       20 |        2 |     77% |15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54, 57, 60, 63, 66, 69, 88, 97, 109->108 |
| ultime/modulerobot.py                             |      149 |      107 |       46 |        0 |     22% |28-33, 36-128, 131-141, 144, 147-148, 151-154, 157, 160-163, 166, 169, 172, 175, 178, 181, 184, 187, 190, 193, 196, 199, 202, 205, 208 |
| ultime/proxy.py                                   |       19 |        0 |        2 |        0 |    100% |           |
| ultime/questnav/\_\_init\_\_.py                   |        0 |        0 |        0 |        0 |    100% |           |
| ultime/questnav/generated/\_\_init\_\_.py         |        0 |        0 |        0 |        0 |    100% |           |
| ultime/questnav/generated/commands\_pb2.py        |       23 |       10 |        2 |        1 |     56% |     33-44 |
| ultime/questnav/generated/data\_pb2.py            |       19 |        6 |        2 |        1 |     67% |     33-40 |
| ultime/questnav/generated/geometry2d\_pb2.py      |       28 |       28 |        2 |        0 |      0% |      7-44 |
| ultime/questnav/generated/geometry3d\_pb2.py      |       26 |       14 |        2 |        1 |     46% |     29-42 |
| ultime/questnav/questnav.py                       |      116 |       92 |       20 |        0 |     18% |86-118, 148-227, 258-289, 298, 314, 325-326, 335, 344, 355-356, 371, 392 |
| ultime/subsystem.py                               |       26 |       18 |        4 |        0 |     27% |10, 13, 16-37 |
| ultime/swerve/\_\_init\_\_.py                     |        0 |        0 |        0 |        0 |    100% |           |
| ultime/swerve/swerve.py                           |      131 |      101 |        8 |        0 |     22% |30-77, 80-95, 101, 104, 109-135, 138, 145-160, 163-164, 167-168, 171, 174, 177, 180, 183, 186, 190-212, 224-229, 232-313 |
| ultime/swerve/swerveconfig.py                     |       67 |        0 |        0 |        0 |    100% |           |
| ultime/switch.py                                  |       54 |        5 |       32 |        5 |     88% |32->35, 35->exit, 53, 57, 67, 70, 73 |
| ultime/tests/\_\_init\_\_.py                      |        9 |        0 |        0 |        0 |    100% |           |
| ultime/tests/test\_alert.py                       |       39 |       34 |        0 |        0 |     13% |8-42, 50-73 |
| ultime/tests/test\_commands.py                    |       53 |       26 |       26 |        0 |     49% |46-77, 81-103 |
| ultime/tests/test\_modules.py                     |       48 |        1 |        0 |        0 |     98% |        17 |
| ultime/tests/test\_properties.py                  |        3 |        0 |        0 |        0 |    100% |           |
| ultime/tests/test\_proxy.py                       |       27 |        0 |        0 |        0 |    100% |           |
| ultime/tests/test\_subsystems.py                  |       17 |        0 |        8 |        0 |    100% |           |
| ultime/tests/test\_switch.py                      |       33 |        0 |        0 |        0 |    100% |           |
| ultime/tests/test\_timethis.py                    |        3 |        0 |        0 |        0 |    100% |           |
| ultime/tests/utils.py                             |       76 |       44 |       10 |        0 |     44% |28-29, 37, 40-44, 47-51, 54-58, 61-65, 68-70, 73-74, 77-85, 88-96, 101-102 |
| ultime/timethis.py                                |       63 |       47 |       16 |        0 |     20% |17-45, 53-57, 61-93, 97-100 |
| ultime/trapezoidalmotion.py                       |       98 |       82 |       42 |        0 |     11% |20-23, 39-63, 76-94, 97-153, 159-162, 165-197, 200-203, 206-207, 210 |
| ultime/vision.py                                  |       90 |       90 |       28 |        0 |      0% |     1-153 |
| **TOTAL**                                         | **4023** | **2460** |  **550** |   **12** | **36%** |           |


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