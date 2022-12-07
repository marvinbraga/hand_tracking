import base64
import json
import time

import openai
from decouple import config

# # list engines
# engines = openai.Engine.list()
#
# # print the first engine's id
# print("engines: ", engines.data[0].id)
#
# # create a completion
# completion = openai.Completion.create(engine="ada", prompt="Hello world")
#
# # print the completion
# print("completation: ", completion.choices[0].text)


class ImageCreate:
    openai.api_key = config("open_ai_key", cast=str)

    def __init__(self, prompt, path="./data/", size="256x256", number_of_images=1):
        self._size = size
        self._number_of_images = number_of_images
        self._path = path
        self._prompt = prompt

    def _save_image(self, response):
        image_64_encode = json.loads(str(response))["data"][0]["b64_json"]
        image_64_decode = base64.b64decode(image_64_encode)
        file_name = self._path + self._prompt.replace(' ', '_') + '.png'
        with open(file_name, 'wb') as image_result:
            image_result.write(image_64_decode)
        return self

    def execute(self):
        start = time.perf_counter()
        try:
            response = openai.Image.create(
                prompt=self._prompt,
                n=self._number_of_images,
                size=self._size,
                response_format="b64_json"
            )
        finally:
            stopwatch = time.perf_counter() - start
            print("Request completed in {0:.0f}ms".format(stopwatch))

        self._save_image(response)


ImageCreate(
    prompt="f1 car hdr 8k ultra realistic futuristic",
    size="1024x1024",
).execute()
