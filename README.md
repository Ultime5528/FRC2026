# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/Ultime5528/FRC2026/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                         |    Stmts |     Miss |   Branch |   BrPart |   Cover |   Missing |
|--------------------------------------------- | -------: | -------: | -------: | -------: | ------: | --------: |
| commands/\_\_init\_\_.py                     |        0 |        0 |        0 |        0 |    100% |           |
| commands/climber/\_\_init\_\_.py             |        0 |        0 |        0 |        0 |    100% |           |
| commands/climber/hug.py                      |       17 |        8 |        0 |        0 |     53% |9-12, 15, 18, 21, 24 |
| commands/climber/move.py                     |       44 |       10 |        0 |        0 |     77% |27-32, 36-41, 45-50, 53 |
| commands/climber/unhug.py                    |       17 |        8 |        0 |        0 |     53% |9-12, 15, 18, 21, 24 |
| commands/drivetrain/\_\_init\_\_.py          |        0 |        0 |        0 |        0 |    100% |           |
| commands/drivetrain/drive.py                 |       54 |       34 |       14 |        0 |     29% |13-17, 21-24, 37-42, 45, 48-87, 90 |
| commands/drivetrain/driverelative.py         |       37 |       18 |        0 |        0 |     51% |11-13, 17-19, 23-25, 29-31, 34-37, 40, 43 |
| commands/drivetrain/resetgyro.py             |       20 |       11 |        2 |        0 |     41% |11-14, 17-25, 30 |
| commands/drivetrain/resetpose.py             |       13 |        6 |        0 |        0 |     54% |9-12, 15, 18 |
| commands/feeder/\_\_init\_\_.py              |        0 |        0 |        0 |        0 |    100% |           |
| commands/feeder/ejectfuel.py                 |       13 |        6 |        0 |        0 |     54% |7-9, 12, 15, 18 |
| commands/feeder/grabfuel.py                  |       13 |        6 |        0 |        0 |     54% |7-9, 12, 15, 18 |
| commands/guide.py                            |       38 |        7 |        0 |        0 |     82% |29-34, 38-43, 46 |
| commands/pivot/\_\_init\_\_.py               |        0 |        0 |        0 |        0 |    100% |           |
| commands/pivot/maintainpivot.py              |       13 |        6 |        0 |        0 |     54% |7-9, 12, 15, 18 |
| commands/pivot/move.py                       |       38 |        7 |        0 |        0 |     82% |29-34, 38-43, 46 |
| commands/shooter/\_\_init\_\_.py             |        0 |        0 |        0 |        0 |    100% |           |
| commands/shooter/manualshoot.py              |       23 |        9 |        0 |        0 |     61% |8-10, 13, 16, 19, 24, 27-28 |
| commands/shooter/prepareshoot.py             |       16 |        9 |        2 |        0 |     39% |7-10, 13-14, 17, 20-21 |
| commands/shooter/shoot.py                    |       16 |        9 |        2 |        0 |     39% |7-9, 12-16, 19, 22 |
| conftest.py                                  |        1 |        0 |        0 |        0 |    100% |           |
| modules/\_\_init\_\_.py                      |        0 |        0 |        0 |        0 |    100% |           |
| modules/autonomous.py                        |       34 |       15 |        4 |        0 |     50% |20, 25-49, 52, 55-61, 64-65 |
| modules/control.py                           |       12 |        7 |        0 |        0 |     42% |     11-27 |
| modules/dashboard.py                         |       90 |       62 |       12 |        0 |     27% |34-41, 44, 51-101, 104-121, 127-144 |
| modules/hardware.py                          |       31 |       16 |        0 |        0 |     48% |18-35, 38-39 |
| modules/logging.py                           |       24 |       13 |        4 |        0 |     39% |12, 19-28, 31, 35-41 |
| modules/propertysavechecker.py               |       36 |       26 |       16 |        0 |     19% |13-27, 30-48 |
| modules/questvision.py                       |       38 |       22 |        2 |        0 |     40% |22-25, 28-37, 44, 47, 50-64 |
| modules/tagvision.py                         |       34 |       34 |        6 |        0 |      0% |      1-60 |
| ports.py                                     |       30 |        0 |        0 |        0 |    100% |           |
| properties.py                                |       85 |       72 |       18 |        1 |     14% |17-24, 34-58, 62-78, 82-127, 131-158 |
| robot.py                                     |       21 |       10 |        0 |        0 |     52% |     17-37 |
| subsystems/\_\_init\_\_.py                   |        0 |        0 |        0 |        0 |    100% |           |
| subsystems/climber.py                        |       61 |       29 |        2 |        0 |     51% |24-44, 47, 50, 53, 56, 59, 62, 65, 68, 71, 74, 77, 80-81, 84-85, 88-96 |
| subsystems/drivetrain.py                     |      160 |      112 |       12 |        0 |     28% |43-167, 184-195, 200-225, 233, 236, 239, 242, 248-249, 257-266, 274-283, 288-291, 296-307, 310-327, 330-353, 356-363, 369, 372, 389-390, 393, 396-411 |
| subsystems/feeder.py                         |       16 |        5 |        0 |        0 |     69% |13-14, 19, 22, 25 |
| subsystems/guide.py                          |       47 |       23 |        2 |        0 |     49% |18-38, 41-42, 45, 48, 51, 54, 57, 60, 63, 66, 69, 72, 75 |
| subsystems/pivot.py                          |       52 |       24 |        4 |        0 |     50% |20-40, 43-48, 51, 54, 57, 60, 63, 66, 69, 72, 75, 78, 81, 84 |
| subsystems/shooter.py                        |       55 |       31 |        4 |        0 |     41% |23-51, 54-58, 61-62, 65-68, 71, 77-80, 83, 86 |
| tests/\_\_init\_\_.py                        |        0 |        0 |        0 |        0 |    100% |           |
| tests/test\_climber.py                       |      123 |      102 |        0 |        0 |     17% |19-23, 27-30, 34-57, 66-86, 90-91, 100-101, 110-111, 120-141, 147-175, 181-194, 198-204, 208-214 |
| tests/test\_common.py                        |        1 |        0 |        0 |        0 |    100% |           |
| tests/test\_guide.py                         |       40 |       29 |        0 |        0 |     28% |10-13, 17-20, 24-42, 51-61, 65, 71 |
| tests/test\_shooter.py                       |       54 |       44 |        0 |        0 |     19% |11-13, 17-37, 43-63, 69-88 |
| ultime/\_\_init\_\_.py                       |        0 |        0 |        0 |        0 |    100% |           |
| ultime/affinecontroller.py                   |       77 |       77 |        2 |        0 |      0% |     1-122 |
| ultime/alert.py                              |       89 |       53 |       14 |        0 |     35% |19-20, 24, 27, 32-34, 37, 40, 43-53, 64-71, 74-85, 88, 91-100, 103, 106, 110-116, 130-132, 135-136, 139 |
| ultime/auto.py                               |        5 |        5 |        0 |        0 |      0% |       1-7 |
| ultime/autoproperty.py                       |       57 |       36 |       22 |        1 |     28% |33-35, 39, 52-105 |
| ultime/axistrigger.py                        |        8 |        8 |        2 |        0 |      0% |      1-16 |
| ultime/command.py                            |       71 |       47 |        4 |        0 |     32% |15-19, 23-51, 56-58, 61, 64, 85-90, 94, 97-101, 104, 107, 110-111, 114-115 |
| ultime/coroutinecommand.py                   |       27 |       27 |        6 |        0 |      0% |      1-41 |
| ultime/dynamicmotion.py                      |       55 |       55 |       14 |        0 |      0% |     1-175 |
| ultime/gyro.py                               |      124 |       69 |        2 |        0 |     44% |21, 26-27, 42, 45, 48, 51-53, 58-64, 67, 70, 73, 76, 81-85, 88, 91, 94, 97, 104-115, 120, 125, 130, 133, 136-137, 140-155, 164-168, 171, 174, 177, 180, 185-194, 197, 200, 203-204, 207-208, 211, 214 |
| ultime/immutable.py                          |        6 |        2 |        0 |        0 |     67% |      3, 8 |
| ultime/linear/\_\_init\_\_.py                |        0 |        0 |        0 |        0 |    100% |           |
| ultime/linear/linearsubsystem.py             |      100 |       65 |       16 |        0 |     30% |20-34, 37-40, 44, 48, 52, 56, 60, 64, 67, 71, 74, 80, 84, 88, 92, 95-114, 117-127, 130-154, 157-169 |
| ultime/linear/manualmovelinear.py            |       27 |       13 |        0 |        0 |     52% |10-12, 16-18, 21-24, 27, 30, 38 |
| ultime/linear/movelinear.py                  |       30 |       19 |        6 |        0 |     31% |18-24, 27, 37-39, 42-47, 50-55 |
| ultime/linear/resetlinear.py                 |       41 |       26 |       10 |        0 |     29% |10-12, 16-18, 21-25, 28, 31-42, 45-48, 51 |
| ultime/linearinterpolator.py                 |       25 |       25 |        6 |        0 |      0% |      1-36 |
| ultime/log.py                                |      103 |       71 |       26 |        0 |     25% |10-11, 18, 21-27, 30-31, 37, 40-42, 45-56, 67-91, 96-102, 105-107, 110, 113-115, 120, 123-124, 127, 135, 138-143, 146, 150, 153-154, 157-158, 161 |
| ultime/module.py                             |       81 |       21 |       20 |        2 |     77% |15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54, 57, 60, 63, 66, 69, 88, 97, 109->108 |
| ultime/modulerobot.py                        |      149 |      107 |       46 |        0 |     22% |28-33, 36-128, 131-141, 144, 147-148, 151-154, 157, 160-163, 166, 169, 172, 175, 178, 181, 184, 187, 190, 193, 196, 199, 202, 205, 208 |
| ultime/proxy.py                              |       19 |        0 |        2 |        0 |    100% |           |
| ultime/questnav/\_\_init\_\_.py              |        0 |        0 |        0 |        0 |    100% |           |
| ultime/questnav/generated/\_\_init\_\_.py    |        0 |        0 |        0 |        0 |    100% |           |
| ultime/questnav/generated/commands\_pb2.py   |       23 |       10 |        2 |        1 |     56% |     33-44 |
| ultime/questnav/generated/data\_pb2.py       |       19 |        6 |        2 |        1 |     67% |     33-40 |
| ultime/questnav/generated/geometry2d\_pb2.py |       28 |       28 |        2 |        0 |      0% |      7-44 |
| ultime/questnav/generated/geometry3d\_pb2.py |       26 |       14 |        2 |        1 |     46% |     29-42 |
| ultime/questnav/questnav.py                  |      116 |       92 |       20 |        0 |     18% |86-118, 148-227, 258-289, 298, 314, 325-326, 335, 344, 355-356, 371, 392 |
| ultime/subsystem.py                          |       27 |       18 |        4 |        0 |     29% |11, 14, 17-38 |
| ultime/swerve/\_\_init\_\_.py                |        0 |        0 |        0 |        0 |    100% |           |
| ultime/swerve/swerve.py                      |      132 |      101 |        8 |        0 |     22% |31-78, 81-96, 102, 105, 110-136, 139, 146-161, 164-165, 168-169, 172, 175, 178, 181, 184, 187, 191-213, 225-230, 233-314 |
| ultime/swerve/swerveconfig.py                |       67 |        0 |        0 |        0 |    100% |           |
| ultime/switch.py                             |       55 |        6 |       32 |        5 |     87% |31->exit, 43, 55, 59, 69, 72, 75 |
| ultime/tests/\_\_init\_\_.py                 |        9 |        0 |        0 |        0 |    100% |           |
| ultime/tests/test\_alert.py                  |       39 |       34 |        0 |        0 |     13% |8-42, 50-73 |
| ultime/tests/test\_commands.py               |       53 |       26 |       26 |        0 |     49% |46-77, 81-103 |
| ultime/tests/test\_modules.py                |       48 |        1 |        0 |        0 |     98% |        17 |
| ultime/tests/test\_properties.py             |        3 |        0 |        0 |        0 |    100% |           |
| ultime/tests/test\_proxy.py                  |       27 |        0 |        0 |        0 |    100% |           |
| ultime/tests/test\_subsystems.py             |       17 |        0 |        8 |        0 |    100% |           |
| ultime/tests/test\_switch.py                 |       33 |        0 |        0 |        0 |    100% |           |
| ultime/tests/test\_timethis.py               |        3 |        0 |        0 |        0 |    100% |           |
| ultime/tests/utils.py                        |       76 |       44 |       10 |        0 |     44% |28-29, 37, 40-44, 47-51, 54-58, 61-65, 68-70, 73-74, 77-85, 88-96, 101-102 |
| ultime/timethis.py                           |       63 |       47 |       16 |        0 |     20% |17-45, 53-57, 61-93, 97-100 |
| ultime/trapezoidalmotion.py                  |       98 |       82 |       42 |        0 |     11% |20-23, 39-63, 76-94, 97-153, 159-162, 165-197, 200-203, 206-207, 210 |
| ultime/vision.py                             |       91 |       91 |       28 |        0 |      0% |     1-154 |
| **TOTAL**                                    | **3564** | **2156** |  **506** |   **12** | **37%** |           |


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