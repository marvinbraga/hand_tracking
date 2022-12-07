import base64
import json
import time

import openai
from decouple import config

openai.api_key = config("open_ai_key", cast=str)

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

prompt_text = "age of empires hdr 8k ultra realistic cyberpunk futuristic"

start = time.perf_counter()
response = openai.Image.create(
    prompt=prompt_text,
    n=1,
    size="256x256",
    response_format="b64_json"
)

request_time = time.perf_counter() - start
print("Request completed in {0:.0f}ms".format(request_time))


image_64_encode = json.loads(str(response))["data"][0]["b64_json"]
image_64_decode = base64.b64decode(image_64_encode)
fileName = './data/' + prompt_text.replace(' ', '_') + '.png'
with open(fileName, 'wb') as image_result:  # create a writable image and write the decoding result
    image_result.write(image_64_decode)
