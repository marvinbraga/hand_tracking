from pathlib import Path

from invoke import task

from apps.open.base.images import ImageCreate
from apps.open.base.texts import TextCreate

PROJECT_ROOT = Path(__file__).parent.absolute()


@task
def say(c, text):
    print(TextCreate(prompt=text).execute().result)


@task
def img(c, text, size="1024x1024"):
    print(ImageCreate(prompt=text, size=size).execute().file_name)
