import vertexai
import os
import base64
from vertexai.generative_models import GenerativeModel, Part
import vertexai.vision_models

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gcp-secret.json"
project_id = "subtle-chimera-424908-r4"
vertexai.init(project=project_id, location="us-central1")


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


model = GenerativeModel(model_name="gemini-1.5-flash")
prompt = """You are an expert at performing OCR on handwritten text.
        **Task:** Optical Character Recognition and LaTex Conversion
        **Input:** An image containing handwritten homework in the subject {subject}.
        **Subject Specifics:**
                * **Math:** May include geometric shapes, symbols, English language steps, and mathematical formulas.
                * **Science:** May include diagrams, chemical formulas, and scientific terms.
                * **English:** May include grammar, punctuation, and sentence structure.
        **Output:** A complete LaTex document containing the extracted expression from the handwritten homework.
        **Rules:**
                * You must represent the input content as it is. Do not correct any errors in the handwriting.
                * If the handwriting is unclear, return the error message "Error: Image is unclear".
                * If the input image is not a handwritten homework, return the error message "Error: Image is not of a handwritten homework".
"""

response = model.generate_content(
    [
        Part.from_uri(
            "gs://vertexai-test-subtle-chimera-424908-r4/test_1.JPEG",
            mime_type="image/jpeg",
        ),
        Part.from_uri(
            "gs://vertexai-test-subtle-chimera-424908-r4/test_2.JPEG",
            mime_type="image/jpeg",
        ),
        prompt.format(subject="Math"),
    ]
)

print(response.text)
