import dotenv
import os
import random
import requests
import time

dotenv.load_dotenv()
FLUX_MODEL = 'flux-dev'


def get_result_url(id: str):
    result_url = "https://api.bfl.ml/v1/get_result"
    querystring = {"id": id}
    response = requests.get(result_url, params=querystring)

    print(response.json())


def generate_image(seed: int, prompt: str):
    image_generation_url = "https://api.bfl.ml/v1/" + FLUX_MODEL
    print(f"url: {image_generation_url}")
    payload = {
        "prompt": prompt,
        "width": 1024,
        "height": 1024,
        "prompt_upsampling": False,
        "steps": 28,
        "guidance": 3.5,
        "seed": seed,
    }
    print(f"payload: {payload}")
    headers = {
        "Content-Type": "application/json",
        "X-Key": os.environ["FLUX_API_KEY"]
    }
    response = requests.post(image_generation_url,
                             json=payload, headers=headers)

    print(response.json())
    return response.json()


seed = random.randint(0, 2147483647)
print(f"Seed: {seed}")
prompt = "Create a front-facing image of a horse from the Chinese zodiac as a mascot for an educational platform for students from primary 1 to 6. This mascot is in Stage 1, depicted as a young foal with a rounded face, short neck, and compact body, featuring a light brown coat and black hooves. The horse has 4 legs and zero hands, with each leg clearly visible in a natural sitting position. Its ears are short and slightly curved, and it has a short, tufted mane and a small tail. The eyes are large, round, and dark brown, reflecting innocence and curiosity. The foal’s overall appearance is simple and without any accessories, suitable for a primary 1 to 6 audience to understand its young age. The background should be plain, using soft pastel colors to keep the focus on the horse. The horse is expressing {emotion}."
response = generate_image(
    seed, prompt.format(emotion="happiness"))

time.sleep(5)
get_result_url(response["id"])
