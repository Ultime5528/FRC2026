import tomllib

with open("pyproject.toml", "rb") as f:
    content = tomllib.load(f)
    print(content)
    robotpy_version = content["tool"]["robotpy"]["robotpy_version"]

print(f"Detected robotpy version: {robotpy_version}")

reqs = f"""flake8==7.1.1
robotpy=={robotpy_version}
"""

print(reqs)

with open("test_requirements.txt", "w") as f:
    f.write(reqs)
