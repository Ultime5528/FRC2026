# FRC2026

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/Ultime5528/FRC2025/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/Ultime5528/FRC2025/blob/python-coverage-comment-action-data/htmlcov/index.html) ![LoC Badge](https://raw.githubusercontent.com/ultime5528/FRC2025/image-data/badge.svg)

## Execution

* Simulation : `python -m robotpy sim`
* Deployment : `python -m robotpy deploy --skip-tests`
* Run tests : `python -m robotpy test -- --exitfirst --timeout=60 --session-timeout=300`
* Run tests with coverage : `python -m robotpy coverage test -- --exitfirst`
* Create coverage HTML report : `coverage html`
* Sync dependencies : `python -m robotpy sync`
* Format code with black `python -m black .`
* Save autoproperties : `python properties.py saveonce`
* Save loop autoproperties : `python properties.py saveloop`
* PyNetConsole : `python -m netconsole 10.55.28.2`


## Environment setup
* Download the latest Miniconda version on your computer with the following link (https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe)
* Open Anaconda Prompt
* Run the following commands to make sure everything is up-to-date:
```commandline
  conda config --add channels conda-forge
  conda config --set channel_priority strict
  conda update conda
  conda update python
```
* Run the following command to create an environment named "frc2026":
```commandline
  conda create -n frc2026 python=3.14.2
```
* Add the environment to the interpreter on PyCharm
* Run the following commands on the PyCharm terminal to install the requirements
```commandline
  pip install robotpy
  conda install libprotobuf 
  python -m robotpy sync
```

* Run the following command to convert the proto to python files
```commandline
  python -m grpc_tools.protoc -I=ultime/questnav/protos --python_out=ultime/questnav/generated ultime/questnav/protos/*.proto

```

(In a new project, execute `python -m robotpy init` instead.)


## Writing Conventions 
* All code must be written in the English language
* Follow PyCharm style recommendations
* Commit names must be clear and informative
* Progress must be tracked with GitHub Projects (https://github.com/orgs/Ultime5528/projects/8)
* File names use lowercase without spaces
* Class names use PascalCase
* Function names use camelCase
* Variable names use snake_case
* Function and command names start with an action verb (get, set, move, start, stop...)
* Commands and subsystems inherit from SafeCommand and SafeSubsystem
* Ports  
    * Must be added to ports.py
    * Respect the naming convention : "subsystem" _ "component type" _ "precision"
    * Example : drivetrain_motor_left
* Autoproperties 
  * Respect the naming convention : "variable type" _ "precision"
  * Example : speed_slow, height_max, distance_max
