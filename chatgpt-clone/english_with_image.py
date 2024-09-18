import json
from openai_text_to_text import get_openai_response

from PIL import Image, ImageDraw, ImageFont

COMPARE_AND_CONTRAST_PROMPT = """
        You are a helpful english assistant who can generate question variants.
        **TASK**:
        - Your task is to generate a brief text similar to the example question, and list out the entities and characteristics to make a compare and contrast table.
        **STEPS**:
        - Generate a brief text for the variant question similar to the given input for the given class.
        - Identify and list out the entities and characteristics to make a compare and contrast table.
        **RULES**:
        - You should neither return the same text as the given input nor return the text with the exact same meaning of the given input.
        - You can be creative and generate a text that is in similar structure to the question given in the input.
        - Example: If the input question is about apples and oranges, you can generate something with cars and bikes.
        **INPUT**: {input}
                Sample input be will be:
                {{
                        "class": class in which the student is studying,
                        "question": brief text of the example question,
                        "image_url": image url of the example question
                }}
        **OUTPUT**:
                Output should be a JSON object with the following structure:
                {{
                        "question": "Generated question text",
                        "entities": ["entity1", "entity2"],
                        "characteristics": ["characteristic 1", "characteristic 2"]
                }}
        **EXAMPLE**:
                **Output**:
                {{
                        "question": "What are the differences between rabbits and squirrels?",
                        "entities": ["Rabbit", "Squirrel"],
                        "characteristics": ["Lives in trees", "Hops on the ground"]
                }}
"""

HIERARCHY_GENERATION_PROMPT = """
        You are a helpful english assistant who can generate question variants.
        **TASK**:
        - Your task is to generate a list of labels for a vertical hierarchy image similar to the vertical hierarchy image given in the input for the given class.
        - The labels should be related to each other, and the students should be able to rank them based on the vertical hierarchy from most general to most specific. You can be creative in the domain.
                - Example: If the input image has labels: animals, mammals, etc., you can generate something with vehicles, cars, etc. or something with food, fruits, etc.
        **RULES**:
        - The labels in the output list strictly should not have horizontal hierarchy.
        - The labels in the output list strictly should be in the jumbled order, definitely not in the order of the vertical hierarchy.
        - All the labels should fall under one vertical hierarchy from most specific to most general.
                - Example:
                        - If the hierarchy is about animals, mammals, etc., the output should not have both dogs and cats in the same list as they are at the same level.
                        - If the hierarchy is about vehicles, cars, etc., the output should not have both cars and bikes in the same list as they are at the same level.
        - The labels should be easy to understand for a student of the given class.
        **INPUT**: {input}
                Sample input be will be:
                {{
                        "class": class in which the student is studying,
                        "image_url": image url of the example hierarchy question
                }}
        **OUTPUT**:
                Output should be a JSON object containing the following:
                - A list of labels for a hierarchy image.
        **EXAMPLE**:
                Output:
                {{
                        "labels": ["label1", "label2", "label3"]
                }}
"""

GROUP_LABELS_PROMPT = """
        You are a helpful english assistant who can generate question variants.
        **TASK**:
        - Your task is to generate a list of labels for a group image similar to the group image given in the input for the given class.
        - Some labels should be related to each other, and the students should be able to group them based on the similarity. You can be creative in the domain.
                - Example: If the input image's domain is fruits, you can generate labels for vegetables, or machines, or time, or distance, etc.
        **RULES**:
        - The number of labels in the output should be a multiple of 3.
        - Not all labels should be related to each other. Some labels should be outliers.
                - Example: If the domain is vegetables, you can group carrots, potatoes, tomatoes, and apple where apple and tomatoes are outliers.
        **INPUT**: {input}
                Sample input be will be:
                {{
                        "class": class in which the student is studying,
                        "image_url": image url of the example group question
                }}
        **OUTPUT**:
                Output should be a JSON object containing the following:
                - A list of labels for a group image.
        **EXAMPLE**:
                Output:
                {{
                        "domain": "domain of the labels group image",
                        "labels": ["label1", "label2", "label3"]
                }}
"""


def create_image_with_table(entities: list[str], characteristics: list[str], output_path: str):
    # Image size and background
    img = Image.new('RGB', (600, 225), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Load a font (ensure you have a font file like Arial.ttf in the same directory or specify a path)
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        font = ImageFont.load_default()

    # Table title
    draw.text((20, 20), "Compare and Contrast: " + entities[0] + " vs " + entities[1], font=font, fill=(
        0, 0, 0))

    # Draw the table headers
    draw.text((50, 60), "Characteristic",
              font=font, fill=(0, 0, 0))
    for i, entity in enumerate(entities):
        draw.text((250 + i * 150, 60), entity, font=font, fill=(0, 0, 0))

    # Draw the rows with checkboxes
    for i, characteristic in enumerate(characteristics):
        draw.text((50, 100 + i * 40), characteristic,
                  font=font, fill=(0, 0, 0))
        draw.rectangle([250, 100 + i * 40, 270, 120 + i * 40], outline="black")
        draw.rectangle([400, 100 + i * 40, 420, 120 + i * 40], outline="black")

    # Save the image
    img.save(output_path)


def generate_hierarchy_image(labels: list[str], output_path: str):
    # Parameters
    margin_top = 50
    margin_bottom = 50
    margin_sides = 20
    box_width = 150
    box_height = 50
    y_gap = 20

    # Dynamically calculate image height based on number of labels
    img_height = margin_top + len(labels) * \
        (box_height + y_gap) - y_gap + margin_bottom
    img_width = 200 + box_width + 2 * margin_sides

    # Create image and drawing context
    image = Image.new('RGB', (img_width, img_height), 'white')
    draw = ImageDraw.Draw(image)

    # Load a font
    try:
        # Use Arial or another system font
        font = ImageFont.truetype("arial.ttf", 18)
    except IOError:
        font = ImageFont.load_default()

    # Add "most general" and "most specific" text
    draw.text((margin_sides, margin_top - 40),
              "most general", fill="black", font=font)
    # draw a line from the most general to the most specific
    draw.line((margin_sides + 20, margin_top - 20, margin_sides + 20,
              img_height - margin_bottom + 20), fill="lightgrey", width=2)
    draw.text((margin_sides, img_height - margin_bottom + 30),
              "most specific", fill="black", font=font)

    # Coordinates for the boxes
    x_box = (img_width - box_width) // 2  # Center boxes horizontally

    # Draw boxes and labels
    for i, label in enumerate(labels):
        # Calculate the y position of the current box
        y_box = margin_top + i * (box_height + y_gap)

        # Draw the rectangle (blue box)
        draw.rectangle([x_box, y_box, x_box + box_width,
                       y_box + box_height], fill="#0096FF")

        # Calculate text size and position it in the center of the box
        bbox = draw.textbbox((0, 0), label, font=font)
        text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
        text_x = x_box + (box_width - text_width) // 2
        text_y = y_box + (box_height - text_height) // 2

        # Draw the label text in the box
        draw.text((text_x, text_y), label, fill="white", font=font)

    # Save and show the image
    image.save(output_path)


def generate_compare_and_contrast_image(entities: list[str], characteristics: list[str], output_path: str):
    # Image size and background
    # create dynamic image size based on the number of characteristics
    width = 400 + 50 * len(entities)
    height = 150 + 30 * len(characteristics)
    img = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Load a font (ensure you have a font file like Arial.ttf in the same directory or specify a path)
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        font = ImageFont.load_default()

    # Table title
    draw.text((30, 25), "Compare and Contrast: " + entities[0] + " vs " + entities[1], font=font, fill=(
        0, 0, 0))

    # Draw the table headers
    draw.text((50, 60), "Characteristic",
              font=font, fill=(0, 0, 0))
    for i, entity in enumerate(entities):
        draw.text((250 + i * 150, 60), entity, font=font, fill=(0, 0, 0))

    # Draw the rows with checkboxes
    for i, characteristic in enumerate(characteristics):
        draw.text((50, 100 + i * 40), characteristic,
                  font=font, fill=(0, 0, 0))
        draw.rectangle([250, 100 + i * 40, 270, 120 + i * 40], outline="black")
        draw.rectangle([400, 100 + i * 40, 420, 120 + i * 40], outline="black")

    # Save the image
    img.save(output_path)


def generate_group_labels_image(labels: list[str], output_path: str):
    label_width = 150
    label_height = 50
    padding = 10
    # Calculate the number of rows and columns based on the number of labels
    num_labels = len(labels)
    cols = 3  # Number of columns (fixed as per the image)
    rows = (num_labels + cols - 1) // cols  # Calculate rows needed

    # Compute the image width and height
    image_width = cols * (label_width + padding) + padding
    image_height = rows * (label_height + padding) + padding

    # Create the image
    img = Image.new('RGB', (image_width, image_height), "white")
    draw = ImageDraw.Draw(img)

    # Optional: Load a font, if needed
    # font = ImageFont.truetype("arial.ttf", 20)  # Path to a TTF file if available
    font = ImageFont.load_default()  # Use default font

    for i, label in enumerate(labels):
        row = i // cols
        col = i % cols
        x = col * (label_width + padding) + padding
        y = row * (label_height + padding) + padding

        # Draw the rectangle for each label
        draw.rectangle([x, y, x + label_width, y + label_height],
                       outline="lightblue", width=2)
        draw.rectangle([x, y, x + 20, y + label_height],
                       fill="lightblue")  # Small blue rectangle

        # Draw the text inside the rectangle
        # Get the bounding box of the text
        text_bbox = draw.textbbox((0, 0), label, font=font)
        text_width, text_height = text_bbox[2] - \
            text_bbox[0], text_bbox[3] - text_bbox[1]

        text_x = x + 30 + (label_width - 30 - text_width) / 2
        text_y = y + (label_height - text_height) / 2
        draw.text((text_x, text_y), label, fill="black", font=font)

    img.save(output_path)


def compare_and_contrast_variant_generation():
    prompt = COMPARE_AND_CONTRAST_PROMPT

    input_example = {
        "class": "3",
        "question": "Pumpkins are often thought of as vegetables, but they are actually fruits, like apples. Pumpkins are as popular as apples when it comes to making delicious pies. However, for a quick snack, an apple is a better choice, because you can eat an apple's skin.",
        "image_url": "https://ibb.co/VwwM5qP"
    }
    response = get_openai_response(
        prompt.format(input=json.dumps(input_example)))
    entities = response["entities"]
    characteristics = response["characteristics"]

    print(response)
    generate_compare_and_contrast_image(
        entities, characteristics, 'english_variant_image_gen/compare_and_contrast_table.png')


def hierarchy_variant_generation():
    prompt = HIERARCHY_GENERATION_PROMPT

    input_example = {
        "class": "3",
        "image_url": "https://www.imghippo.com/i/YVK1L1726566277.png"
    }
    response = get_openai_response(
        prompt.format(input=json.dumps(input_example)))
    labels = response["labels"]

    print(response)
    generate_hierarchy_image(
        labels, "english_variant_image_gen/hierarchy.png")


def group_labels_variant_generation():
    prompt = GROUP_LABELS_PROMPT

    input_example = {
        "class": "3",
        "image_url": "https://www.imghippo.com/i/pRZ0J1726570666.png"
    }
    response = get_openai_response(
        prompt.format(input=json.dumps(input_example)))
    labels = response["labels"]

    print(response)
    generate_group_labels_image(
        labels, "english_variant_image_gen/group_labels.png")


compare_and_contrast_variant_generation()
hierarchy_variant_generation()
group_labels_variant_generation()
