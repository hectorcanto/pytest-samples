# Effective testing with Python

Samples of pytest tests and a slide presentation explaining how to
do effecting testing with Pytest and Python. Slides are in Spanish and
English.

This project was created for PyConEs 2021 and used later for other
venues. It has been continued as a central repository of test samples
in Python with pytest and other tools

It has a Markdown based presentation in Spanish and English plus
a set of test samples using a bare minimum source code.

Check out the test samples at [tests/](tests/)
Check out the slides at `slides` (markdown or PDF)
Check out the dummy code at [source/](source/)

Apart from tests samples, it also has some advanced tests configuration, see
[tests/confest.py](tests/conftest.py) for more detail.

Feel free to refer or reuse this content.
Attribution is appreciated

## Glossary

- fixture: generated artifact to use in a test, could be data, an object, ...
- factory: function to generate a fixture
- sut: system under testing

## Usage

```bash
pytest
pytest -m unit
```

## External documentation

[Pytest docs](https://docs.pytest.org/)
[Markdown slides for RevealJS](https://github.com/dadoomer/markdown-slides)

## Development

### Project Structure

- [source/](source/): dummy code
- [tests/](tests/)
  - Usual folders by domain and type:
    - types: smoke for sanity tests, unit, integration, api ..
    - domain: depends on your project
    - folder naming is used to run tests by tag later (python -m yourtag)

#### Test samples

- [Smoke tests](tests/smoke/)
- [Unit tests](tests/unit/)
  - delayed assert: sometimes is useful to run several tests over the same execution,
    but we still want to see them as separated ones

## Recommended plugins and libraries

Highly recommended:

- Faker: fake data generator
- factoryboy and polifactory: Mother or Object factory libraries
- freezegun: stops and moves time at will, use with caution
- lambdapowertools: AWS lambda utils
- any time library like timeago, arrow, pendulum ...

Some are already installed, see [Pipfile](Pipfile)

- deep diff: advanced diff library that allow you to customize your diff,
   especially for complex structures like dicts. Among other features you
   can ignore keys, take order into account or not, ect.
- *time diff and ranges*: arrow, pendulum, deloream, maya, moment, timeago, when.
- Some are really  useful to complex time ranges or concepts like: a week from
   today, next monday, last Sunday of the previous month, etc.
