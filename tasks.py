from pathlib import Path

from invoke import task

from apps.open.test_open_ai import TextCreate

PROJECT_ROOT = Path(__file__).parent.absolute()


@task
def say(c, text):
    print(TextCreate(prompt=text).execute().result)
