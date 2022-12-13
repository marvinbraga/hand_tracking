import base64
import json
import time

import openai
from decouple import config


class TextCreate:
    engine = "text-davinci-003"
    openai.api_key = config("open_ai_key", cast=str)

    def __init__(self, prompt):
        self._prompt = prompt
        self._result = None

    @property
    def result(self):
        return self._result

    def execute(self):
        response = openai.Completion.create(
            engine=self.engine,
            prompt=self._prompt,
            temperature=0.7,
            max_tokens=256 * 3,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        self._result = response.choices[0].text
        return self


class ImageCreate:
    openai.api_key = config("open_ai_key", cast=str)

    def __init__(self, prompt, path="./data/", size="256x256", number_of_images=1):
        self._size = size
        self._number_of_images = number_of_images
        self._path = path
        self._prompt = prompt
        self._file_name = None

    def _save_image(self, response):
        image_64_encode = json.loads(str(response))["data"][0]["b64_json"]
        image_64_decode = base64.b64decode(image_64_encode)
        self._file_name = self._path + self._prompt.replace(" ", "_") + ".png"
        with open(self._file_name, "wb") as image_result:
            image_result.write(image_64_decode)
        return self

    @property
    def file_name(self):
        return self._file_name

    def execute(self):
        start = time.perf_counter()
        try:
            response = openai.Image.create(
                prompt=self._prompt,
                n=self._number_of_images,
                size=self._size,
                response_format="b64_json",
            )
        finally:
            stopwatch = time.perf_counter() - start
            print(f"Request completed in {stopwatch:.0f}ms")

        self._save_image(response)
        return self


if __name__ == "__main__":
    engines = openai.Engine.list()
    print("\n".join([engine.id for engine in engines.data]))

    print(
        TextCreate(
            prompt="Quais os melhores sites sobre Django e Python?",
        )
        .execute()
        .result,
    )

    print(
        ImageCreate(
            prompt="f1 car hdr 8k ultra realistic futuristic",
            size="1024x1024",
        )
        .execute()
        .file_name,
    )
