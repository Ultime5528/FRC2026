# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/Ultime5528/FRC2026/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                              |    Stmts |     Miss |   Branch |   BrPart |   Cover |   Missing |
|-------------------------------------------------- | -------: | -------: | -------: | -------: | ------: | --------: |
| commands/\_\_init\_\_.py                          |        0 |        0 |        0 |        0 |    100% |           |
| commands/alignshoot.py                            |       17 |        2 |        0 |        0 |     88% |     27-28 |
| commands/autonomous/\_\_init\_\_.py               |        0 |        0 |        0 |        0 |    100% |           |
| commands/autonomous/autopath.py                   |       24 |        0 |        0 |        0 |    100% |           |
| commands/autonomous/rushtomiddle.py               |       47 |       25 |        0 |        0 |     47% |19-26, 30-37, 41-48, 52-59, 68-81 |
| commands/autonomous/shootandclimb.py              |       33 |       19 |        0 |        0 |     42% |15-17, 21-23, 31-44 |
| commands/autonomous/towerclimb.py                 |       31 |       12 |        0 |        0 |     61% |21-23, 27-29, 32-38 |
| commands/climber/\_\_init\_\_.py                  |        0 |        0 |        0 |        0 |    100% |           |
| commands/climber/maintainclimber.py               |        9 |        4 |        0 |        0 |     56% |  9-11, 14 |
| commands/climber/move.py                          |       44 |       10 |        0 |        0 |     77% |27-32, 36-41, 45-50, 53 |
| commands/drivetrain/\_\_init\_\_.py               |        0 |        0 |        0 |        0 |    100% |           |
| commands/drivetrain/aligntotower.py               |       31 |       18 |        6 |        0 |     35% |14-17, 20, 23-38, 41, 44-45 |
| commands/drivetrain/auto/\_\_init\_\_.py          |        0 |        0 |        0 |        0 |    100% |           |
| commands/drivetrain/auto/alignpreciseafterpath.py |       34 |       19 |        4 |        0 |     39% |16-22, 25-37, 40-44, 47, 61 |
| commands/drivetrain/auto/followpathprecise.py     |       10 |        5 |        0 |        0 |     50% |      9-14 |
| commands/drivetrain/auto/pathfindfollowpath.py    |       10 |        5 |        0 |        0 |     50% |      9-14 |
| commands/drivetrain/auto/pathfindprecise.py       |       11 |        5 |        0 |        0 |     55% |     10-15 |
| commands/drivetrain/drive.py                      |       54 |       34 |       14 |        0 |     29% |13-17, 21-24, 37-42, 45, 48-87, 90 |
| commands/drivetrain/drivealign.py                 |       41 |       24 |        8 |        0 |     35% |13-17, 21-24, 39-43, 46-66, 69 |
| commands/drivetrain/driverelative.py              |       39 |       19 |        0 |        0 |     51% |13-17, 21-25, 29-33, 37-41, 48-51, 54-55, 58 |
| commands/drivetrain/forwardposition.py            |       20 |        9 |        0 |        0 |     55% |12-15, 18, 21, 24, 27-28 |
| commands/drivetrain/resetgyro.py                  |       17 |        9 |        2 |        0 |     42% |10-12, 15-22, 25 |
| commands/drivetrain/resetpose.py                  |       13 |        6 |        0 |        0 |     54% |9-12, 15, 18 |
| commands/feeder/\_\_init\_\_.py                   |        0 |        0 |        0 |        0 |    100% |           |
| commands/feeder/ejectfuel.py                      |       13 |        6 |        0 |        0 |     54% |7-9, 12, 15, 18 |
| commands/feeder/grabfuel.py                       |       13 |        6 |        0 |        0 |     54% |7-9, 12, 15, 18 |
| commands/guide/\_\_init\_\_.py                    |        0 |        0 |        0 |        0 |    100% |           |
| commands/guide/checkguide.py                      |       17 |       10 |        6 |        0 |     30% |10-13, 16-27 |
| commands/guide/move.py                            |       45 |       13 |        2 |        0 |     68% |29-31, 35-37, 42-50, 53-57 |
| commands/hugandclimb.py                           |        8 |        1 |        0 |        0 |     88% |        15 |
| commands/hugger/\_\_init\_\_.py                   |        0 |        0 |        0 |        0 |    100% |           |
| commands/hugger/hug.py                            |       17 |        8 |        0 |        0 |     53% |9-12, 15, 18, 21, 24 |
| commands/hugger/unhug.py                          |       17 |        8 |        0 |        0 |     53% |9-12, 15, 18, 21, 24 |
| commands/pivot/\_\_init\_\_.py                    |        0 |        0 |        0 |        0 |    100% |           |
| commands/pivot/maintainpivot.py                   |       13 |        6 |        0 |        0 |     54% |7-9, 12, 15, 18 |
| commands/pivot/move.py                            |       19 |        3 |        2 |        0 |     76% |     12-15 |
| commands/resetall.py                              |       10 |        1 |        0 |        0 |     90% |        13 |
| commands/retractandunhug.py                       |        8 |        1 |        0 |        0 |     88% |        15 |
| commands/shooter/\_\_init\_\_.py                  |        0 |        0 |        0 |        0 |    100% |           |
| commands/shooter/manualshoot.py                   |       23 |       11 |        2 |        0 |     48% |10-12, 15, 18, 21, 26, 29-33 |
| commands/shooter/prepareshoot.py                  |       18 |       10 |        2 |        0 |     40% |13-17, 20-21, 24, 27-28 |
| commands/shooter/shoot.py                         |       19 |       11 |        2 |        0 |     38% |8-11, 14-20, 23, 26 |
| conftest.py                                       |        1 |        0 |        0 |        0 |    100% |           |
| modules/\_\_init\_\_.py                           |        0 |        0 |        0 |        0 |    100% |           |
| modules/autonomous.py                             |       29 |       13 |        4 |        0 |     48% |17, 24-32, 37-43, 46-47 |
| modules/control.py                                |       32 |       17 |        0 |        0 |     47% |     23-84 |
| modules/dashboard.py                              |      109 |       75 |       14 |        0 |     28% |40-48, 51, 57-149, 155-175, 181-198 |
| modules/hardware.py                               |       33 |       17 |        0 |        0 |     48% |19-37, 40-41 |
| modules/logging.py                                |       21 |       12 |        4 |        0 |     36% |11, 18-27, 31-37 |
| modules/positionestimator.py                      |       45 |       35 |       18 |        0 |     16% |17-30, 33-53, 56-62, 65-78 |
| modules/propertysavechecker.py                    |       36 |       26 |       16 |        0 |     19% |13-27, 30-48 |
| modules/questvision.py                            |       34 |       18 |        4 |        0 |     42% |23-26, 31-37, 48, 51, 54-58 |
| modules/shootercalcmodule.py                      |      163 |      102 |       26 |        1 |     34% |71->76, 85-105, 109, 129-152, 155, 159-164, 172, 175, 178, 181-198, 201-202, 207-210, 213-216, 219-229, 232-235, 241-244, 247-269, 272-281, 286, 292-302 |
| modules/sysidmodule.py                            |       16 |        8 |        0 |        0 |     50% |    12-100 |
| modules/tagvision.py                              |       21 |        5 |        0 |        0 |     76% |27, 31, 34-36 |
| ports.py                                          |       32 |        0 |        0 |        0 |    100% |           |
| properties.py                                     |       85 |       72 |       18 |        1 |     14% |17-24, 34-58, 62-78, 82-127, 131-158 |
| robot.py                                          |       32 |       16 |        0 |        0 |     50% |     22-68 |
| subsystems/\_\_init\_\_.py                        |        0 |        0 |        0 |        0 |    100% |           |
| subsystems/climber.py                             |       56 |       30 |        4 |        0 |     43% |26-56, 59-60, 63, 66, 69, 72, 75, 78, 81, 84, 87, 90, 93, 96-102 |
| subsystems/drivetrain.py                          |      193 |      131 |       12 |        0 |     30% |49-217, 220, 223, 226, 243-254, 259-284, 292, 295, 298, 301, 307-308, 316-325, 333-342, 347-350, 355-366, 369-389, 392-415, 418-425, 431, 434-435, 438, 455-458, 461, 464, 467, 471, 476, 481-485 |
| subsystems/feeder.py                              |       20 |        8 |        0 |        0 |     60% |14-20, 27, 30, 33 |
| subsystems/guide.py                               |       55 |       25 |        2 |        0 |     53% |25-49, 52-53, 56, 59, 62, 65, 68, 71, 74, 77, 80, 83, 86, 89 |
| subsystems/hugger.py                              |       20 |        7 |        0 |        0 |     65% |16-18, 21-22, 25-26 |
| subsystems/pivot.py                               |       81 |       44 |       10 |        0 |     41% |36-70, 73-76, 79-84, 87, 90, 93, 96, 99, 102, 105, 108, 111, 114, 117-126, 129, 132-135 |
| subsystems/shooter.py                             |      115 |       75 |       24 |        0 |     29% |39-75, 78-79, 82-108, 111-134, 137-138, 141-148, 151-159, 162-168, 171, 176-184, 187, 190 |
| tests/\_\_init\_\_.py                             |        0 |        0 |        0 |        0 |    100% |           |
| tests/test\_climber.py                            |      135 |      112 |        0 |        0 |     17% |17-19, 23-26, 30-53, 64-117, 123-124, 137-138, 151-152, 165-166, 179-180, 193-194, 207-208, 221-222, 235-236, 247-266, 272-310, 316-329 |
| tests/test\_common.py                             |        1 |        0 |        0 |        0 |    100% |           |
| tests/test\_drivetrain.py                         |       20 |       15 |        0 |        0 |     25% |     41-65 |
| tests/test\_guide.py                              |       49 |       36 |        0 |        0 |     27% |10-13, 17-20, 24-42, 53-74, 78, 89, 100, 113 |
| tests/test\_hugger.py                             |       27 |       19 |        0 |        0 |     30% |8-10, 14-19, 23-29, 33-39 |
| tests/test\_resetall.py                           |       15 |       11 |        0 |        0 |     27% |      7-19 |
| tests/test\_shooter.py                            |      102 |       90 |        0 |        0 |     12% |13-15, 19-60, 64-92, 97-174 |
| tests/test\_shootercalcmodule.py                  |       75 |       38 |        4 |        0 |     49% |24-53, 58-86, 97-137 |
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
| ultime/gyro.py                                    |      137 |       81 |        2 |        0 |     40% |20, 25-26, 41, 44, 47, 50-52, 57-63, 66, 69, 72, 75, 78-79, 82-94, 99-103, 106, 109, 112, 115, 122-133, 138, 143, 148, 151, 154-155, 158-173, 182-186, 189, 192, 195, 198, 203-212, 215, 218, 221-222, 225-226, 229, 232 |
| ultime/immutable.py                               |        6 |        2 |        0 |        0 |     67% |      3, 8 |
| ultime/linear/\_\_init\_\_.py                     |        0 |        0 |        0 |        0 |    100% |           |
| ultime/linear/linearsubsystem.py                  |       98 |       63 |       16 |        0 |     31% |21-37, 40-44, 48, 52, 56, 60, 64, 68, 71, 75, 78, 84, 88, 92, 96, 99, 106, 113-118, 121-131, 134-158 |
| ultime/linear/manualmovelinear.py                 |       27 |       13 |        0 |        0 |     52% |10-12, 16-18, 21-24, 27, 30, 33 |
| ultime/linear/movelinear.py                       |       32 |       21 |        8 |        0 |     28% |18-24, 27, 37-39, 42-49, 52-57 |
| ultime/linear/resetlinear.py                      |       42 |       27 |       10 |        0 |     29% |10-12, 16-18, 26-31, 34, 37-48, 51-54, 57 |
| ultime/linearinterpolator.py                      |       25 |       17 |        6 |        0 |     26% |6-8, 11-12, 15-16, 19, 22, 25-36 |
| ultime/log.py                                     |      103 |       69 |       26 |        0 |     26% |18, 21-27, 30-31, 37, 40-42, 45-56, 67-92, 97-103, 106-108, 111, 114-116, 121, 124-125, 128, 136, 139-144, 147, 151, 154-155, 158-159, 162 |
| ultime/module.py                                  |       81 |       22 |       20 |        3 |     75% |14, 17, 20, 23, 26, 29, 32, 35, 38, 41, 44, 47, 50, 53, 56, 59, 62, 65, 68, 87, 96, 108->107, 117 |
| ultime/modulerobot.py                             |      156 |      114 |       48 |        0 |     21% |28-34, 37-130, 133-143, 146, 149-150, 153-157, 160, 163-171, 174, 177, 180, 183, 186, 189, 192, 195, 198, 201, 204, 207, 210, 213, 216 |
| ultime/proxy.py                                   |       19 |        0 |        2 |        0 |    100% |           |
| ultime/questnav/\_\_init\_\_.py                   |        0 |        0 |        0 |        0 |    100% |           |
| ultime/questnav/generated/\_\_init\_\_.py         |        0 |        0 |        0 |        0 |    100% |           |
| ultime/questnav/generated/commands\_pb2.py        |       23 |       10 |        2 |        1 |     56% |     32-43 |
| ultime/questnav/generated/data\_pb2.py            |       19 |        6 |        2 |        1 |     67% |     32-39 |
| ultime/questnav/generated/geometry2d\_pb2.py      |       28 |       28 |        2 |        0 |      0% |      7-44 |
| ultime/questnav/generated/geometry3d\_pb2.py      |       26 |       14 |        2 |        1 |     46% |     29-42 |
| ultime/questnav/questnav.py                       |      234 |      190 |       42 |        0 |     16% |21-28, 93-134, 137-151, 156, 185-214, 245-273, 276-280, 283-288, 297-298, 301-302, 305-306, 309-310, 321-323, 326-328, 346-351, 365-397, 427-509, 540-571, 580, 596, 607-608, 617, 626, 637-638, 653, 674 |
| ultime/subsystem.py                               |       22 |       12 |        4 |        0 |     38% |10-11, 14, 17-21, 24-28, 31 |
| ultime/swerve/\_\_init\_\_.py                     |        0 |        0 |        0 |        0 |    100% |           |
| ultime/swerve/swerve.py                           |      134 |      104 |       10 |        0 |     21% |30-77, 80-95, 101, 104, 109-135, 138, 145-163, 166-167, 170-171, 174, 177, 180, 183, 186, 189, 193-215, 227-232, 235-316 |
| ultime/swerve/swerveconfig.py                     |       67 |        0 |        0 |        0 |    100% |           |
| ultime/switch.py                                  |       54 |        5 |       32 |        5 |     88% |32->35, 35->exit, 53, 57, 67, 70, 73 |
| ultime/tests/\_\_init\_\_.py                      |        9 |        0 |        0 |        0 |    100% |           |
| ultime/tests/test\_alert.py                       |       40 |       34 |        0 |        0 |     15% |9-43, 51-74 |
| ultime/tests/test\_commands.py                    |       53 |       26 |       26 |        0 |     49% |46-77, 81-103 |
| ultime/tests/test\_modules.py                     |       41 |        1 |        0 |        0 |     98% |        17 |
| ultime/tests/test\_properties.py                  |        3 |        0 |        0 |        0 |    100% |           |
| ultime/tests/test\_proxy.py                       |       27 |        0 |        0 |        0 |    100% |           |
| ultime/tests/test\_subsystems.py                  |       17 |        0 |        8 |        0 |    100% |           |
| ultime/tests/test\_switch.py                      |       33 |        0 |        0 |        0 |    100% |           |
| ultime/tests/test\_timethis.py                    |        3 |        0 |        0 |        0 |    100% |           |
| ultime/tests/utils.py                             |       76 |       44 |       10 |        0 |     44% |28-29, 37, 40-44, 47-51, 54-58, 61-65, 68-70, 73-74, 77-85, 88-96, 101-102 |
| ultime/timethis.py                                |       63 |       47 |       16 |        0 |     20% |17-45, 53-57, 61-93, 97-100 |
| ultime/trapezoidalmotion.py                       |       98 |       82 |       42 |        0 |     11% |20-23, 39-63, 76-94, 97-153, 159-162, 165-197, 200-203, 206-207, 210 |
| ultime/vision.py                                  |       86 |       55 |       26 |        0 |     28% |25-30, 36, 39, 42, 47-48, 51-57, 60-63, 68-74, 79-87, 92-97, 102-141, 144-147, 150 |
| **TOTAL**                                         | **4662** | **2783** |  **640** |   **14** | **37%** |           |


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