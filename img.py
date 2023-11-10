import re
import requests
import json
import os

def is_english(text):
    return not bool(re.search('[\u0E00-\u0E7F]', text))

def translate(data):
    req = requests.get(f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=en&dt=t&q={requests.utils.quote(data)}")
    
    translated_data = req.json()[0][0][0]
    print(f"Translated from {translated_data} to English")
    return translated_data
    
def api(data):
    url = "https://stablediffusionapi.com/api/v3/text2img"

    payload = json.dumps({
    "key": "Pj8wwm70uBTwKPoMQMFuMGHiwICeQackbNnrSsuehGJwtVFqjgoF0iDmwdGN",
    "prompt": data,
    "negative_prompt": None,
    "width": "512",
    "height": "512",
    "samples": "1",
    "num_inference_steps": "20",
    "seed": None,
    "guidance_scale": 7.5,
    "safety_checker": "yes",
    "multi_lingual": "no",
    "panorama": "no",
    "self_attention": "no",
    "upscale": "no",
    "embeddings_model": None,
    "webhook": None,
    "track_id": None
    })

    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    response = response.json()

    print(response['output'][0])
    uri = response['output'][0]
    filename = uri.split('/')[-1]
    r = requests.get(uri, allow_redirects=True)
    open(filename, 'wb').write(r.content)



data = input("Enter your prompt: ")

if data:
    # If the text is not English, translate it first
    if not is_english(data):
        data = translate(data)
    print(data)
    api(data)

else:
    print("No input provided!")