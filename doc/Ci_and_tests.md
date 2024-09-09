# Ci files and testing

Each target needs at least some simple testing to verify that the core requirements work as intended.
These tests should run in the CI pipeline to verify that no code gets broken.
Due to the fact that the repository contains multiple targets, the CI pipeline is split into multiple jobs.
Each target specific job has its own workflow file.

## Individual target workflows

As mentioned each target has its own workflow file.
To demonstrate how they should work we will use the python target as an example.

```yaml
on:
  workflow_call:
    
jobs:
  python_matrix:
    env:
      PYTHONIOENCODING: 'utf-8'
      PYTHONLEGACYWINDOWSSTDIO: 'utf-8'
      PYTHONUTF8: '1'
    strategy:
      fail-fast: false
      matrix:
        os: ["ubuntu-20.04", "ubuntu-22.04", "macos-latest", "windows-latest"]
        pythonVersion: ["3.11", "3.10", "3.9", "3.8"]

    name: ${{ matrix.os }} - python ${{ matrix.pythonVersion }}
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v3
        with:
          python-version: ${{ matrix.pythonVersion }}
          cache: 'pipenv'

      - name: install pipenv
        run: pip install pipenv
      - name: install deps in venv
        run: pipenv install
      - name: update pipenv
        run: pipenv update
      - name: list pipenv packages
        run: pipenv graph

      - name: generate the sources
        run: pipenv run python ./genSources.py --no-post-gen -o output python

      - name: test the project
        working-directory: output
        run: python -m unittest tests/tests.py

      - uses: actions/upload-artifact@v3
        if: failure()
        with:
          name: build-artifact-${{ matrix.os }}-${{ matrix.buildType }}-msys-${{ matrix.useMsys }}
          path: build
```

As you can see the workflow is run on workflow call.
This means other workflow files are responsible for calling this workflow.

All workflow files should run on multiple operating systems to ensure that platform specific bugs are caught early.
The matrix also specifies all the tooling versions that are tested.
In this case the test is run on several python version to make sure that the code is compatible with all of them.

The workflow itself is pretty simple.
It first installs all dependencies, generates the output and then runs the test command to verify that the output is correct.

This can get very complex like the cpp17 example since it has to do a lot of things on windows.
