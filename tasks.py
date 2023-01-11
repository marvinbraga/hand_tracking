from pathlib import Path

from invoke import task

from apps.open.base.codes import CodeCreate
from apps.open.base.images import ImageCreate, ImageVariation
from apps.open.base.texts import TextCreate

PROJECT_ROOT = Path(__file__).parent.absolute()


@task
def say(c, text):
    print(TextCreate(prompt=text).execute().result)


@task
def img(c, text, size="1024x1024"):
    print(ImageCreate(prompt=text, size=size).execute().file_name)


@task
def var(c, text, base, size="1024x1024"):
    print(
        ImageVariation(
            prompt=f"variation_{text}",
            size=size,
            image_filename=base,
        )
        .execute()
        .file_name,
        "\n",
    )


@task
def code(c, text):
    print(CodeCreate(prompt=text).execute().result)
