import openai

from apps.open.base.images import ImageCreate, ImageVariation
from apps.open.base.texts import TextCreate

engines = openai.Engine.list()
print("\n".join(sorted(engine.id for engine in engines.data)))

print(
    TextCreate(
        prompt="Quais os melhores sites sobre Django e Python?",
    )
    .execute()
    .result,
)


image = (
    ImageCreate(
        prompt="age of empires hdr 8k ultra realistic futuristic",
        size="1024x1024",
    )
    .execute()
    .file_name
)

print("Image Created:", image, "\n")

file_name = (
    TextCreate(prompt=f"Extraia apenas o nome do arquivo, sem a extensão: {image}")
    .execute()
    .result.strip()
)
print(
    "Image Variation:",
    ImageVariation(
        prompt=f"variation_{file_name}",
        size="1024x1024",
        image_filename=image,
    )
    .execute()
    .file_name,
    "\n",
)
