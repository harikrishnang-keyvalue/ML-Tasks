import json
import time
import numpy as np
import matplotlib.pyplot as plt

with open("response.json", "r") as f:
    response = json.load(f)
end_time = time.time()

for question in response['questions']:
    diagrams = question.get('diagrams')
    if diagrams:
        for diagram in diagrams:
            if diagram:
                exec(diagram)
