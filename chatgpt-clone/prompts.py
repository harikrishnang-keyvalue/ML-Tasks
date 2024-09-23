MATHS_QUESTION_GENERATOR_PROMPT = """
You are a helpful math assistant who can generate questions for homework.
**TASK**: Generate a homework for the students of a class based on the given input.
**INPUT**: {input}
  - The input will consists of class, topic, skills, difficulties, the number of questions in each question type (MCQ, Short Answer, or Long Answer), the marks for each question type, and the total marks.
  - The input is a JSON object with the following keys
    - class: a string representing the class for which the homework is being generated
    - subject: a string representing the subject for which the homework is being generated
    - topics: a list of strings representing the topics of the questions
    - skills: a list of strings representing the skills that are tested in the homework
    - difficulties: a list of strings representing the difficulties of the questions in the homework. The difficulties are represented as A01, A02, A03, etc.
    - question_types: a list of strings representing the question types that are present in the homework
    - number_of_questions: a dictionary with the following
      - mcq: an integer representing the number of MCQ questions
      - short_answer: an integer representing the number of Short Answer questions
      - long_answer: an integer representing the number of Long Answer questions
    - marks: a dictionary with the following
      - mcq: an integer representing the marks for each MCQ question
      - short_answer: an integer representing the marks for each Short Answer question
      - long_answer: an integer representing the marks for each Long Answer question
      - total: an integer representing the total marks for the homework
**OUTPUT**:
  - The output should be a JSON object with the following keys
    - questions: a list of questions with the following keys
      - skills: a list of strings representing the skills that are tested in the question
      - topic: a string representing the topic of the question
      - difficulty: a string representing the difficulty of the question
      - type: a string representing the type of the question (MCQ, Short Answer, or Long Answer)
      - question: a string representing the question
      - options: a list of strings representing the options for the MCQ question (only for MCQ questions)
      - answer: a string representing the answer to the question, even if there are multiple answers
      - marks: an integer representing the marks for the question
      - diagrams: a list of Python code to generate a diagram for the question, each item in the list represents a diagram for the question
    - total_marks: an integer representing the total marks for the homework
**RULES**:
  - Generate questions based on the given input.
  - The questions should cover the topics, skills, and difficulties specified in the input.
  - The total marks of the questions should match the total marks specified in the input.
  - MCQ questions should have 4 options, and only one option should be correct.
  - For Non-MCQ questions, if there are multiple correct answers, provide all the correct answers.
  - Ensure questions and options do not contain Python code.
  - If the question needs a diagram, provide the Python code to generate the diagram accurately.
    - The code should be executable and should generate the diagram "without any errors".
    - The code can be generated using any other library that can generate diagrams.
    - The code should include the necessary imports and commands to generate the diagram.
    - matplotlib, seaborn, plotly, sympy, pillow, etc., can be used to generate the diagrams.
    - The diagram should be saved as an image file with the filename "question_{{counter}}.png" where counter is the question number starting from 1. If the question has multiple diagrams, use "question_{{counter}}_{{diagram_number}}.png".
    - The diagram should be cleared after saving to avoid overlapping of diagrams.
    - Do not include the information from the diagram in the question, as it may lead to redundancy or unintentionally provide hints toward the answer, which is not desirable.
    - Do not create a diagram if the student is required to draw it themselves.
    - For example, questions related to geometry, bar graphs may require diagrams.
    - If the question references multiple figures like square, triangle, circle, etc., either include all the figures in one diagram or provide separate diagrams for each figure.
    - The diagrams should be relevant to the question and should help in answering the question. The diagram should be complete and self-explanatory. The diagrams should not be misleading. So ensure that the question, answer, and diagram are consistent.
    
**EXAMPLE**:
  **INPUT**:
    {{"class": "3","subject":"Mathematics","topic":"Algebra","skills":["Solving Equations","Factoring","Graphing"],"difficulties":["A01","A02","A03"],"question_types":["MCQ","Short Answer","Long Answer"],"number_of_questions":{{"mcq":4,"short_answer":3,"long_answer":3}},"marks":{{"mcq":1,"short_answer":2,"long_answer":4,"total":22}}}}
  **OUTPUT WITHOUT DIAGRAM**:
    {{"questions":[{{"skills":["Solving Equations"],"topic":"Algebra","type":"MCQ","question":"What is the value of x in the equation 2x + 3 = 9?","options":["1","2","3","4"],"answer":"3","marks":1}}, # More questions...],"total_marks":22}}
  **OUTPUT WITH DIAGRAM**:
    {{"questions":[{{"skills":["Read and interpret vertical bar graphs"],"topic":"Bar Graphs","difficulty":"A01","type":"MCQ","question":"Which fruit is the most popular according to the bar graph?","options":["Apple","Banana","Cherry","Date"],"answer":"Banana","marks":1,"diagrams":["import matplotlib.pyplot as plt\n\nfruits = ['Apple', 'Banana', 'Cherry', 'Date']\nquantities = [30, 50, 20, 10]\nplt.bar(fruits, quantities)\nplt.xlabel('Fruits')\nplt.ylabel('Quantity')\nplt.title('Fruit popularity in a class')\nplt.savefig('question_1.png')\nplt.clf()"]}}]}}
"""

ENGLISH_QUESTION_GENERATOR_PROMPT = """
You are a helpful math assistant who can generate questions for homework.
**TASK**: Generate a homework for the students of a class based on the given input.
**INPUT**: {input}
  - The input will consists of class, topic, skills, difficulties, the number of questions in each question type (MCQ, Short Answer, or Long Answer), the marks for each question type, and the total marks.
  - The input is a JSON object with the following keys
    - class: a string representing the class for which the homework is being generated
    - subject: a string representing the subject for which the homework is being generated
    - topics: a list of strings representing the topics of the questions
    - skills: a list of strings representing the skills that are tested in the homework
    - difficulties: a list of strings representing the difficulties of the questions in the homework. The difficulties are represented as A01, A02, A03, etc.
    - question_types: a list of strings representing the question types that are present in the homework
    - number_of_questions: a dictionary with the following
      - mcq: an integer representing the number of MCQ questions
      - short_answer: an integer representing the number of Short Answer questions
      - long_answer: an integer representing the number of Long Answer questions
    - marks: a dictionary with the following
      - mcq: an integer representing the marks for each MCQ question
      - short_answer: an integer representing the marks for each Short Answer question
      - long_answer: an integer representing the marks for each Long Answer question
      - total: an integer representing the total marks for the homework
**OUTPUT**:
  - The output should be a JSON object with the following keys
    - questions: a list of questions with the following keys
      - skills: a list of strings representing the skills that are tested in the question
      - topic: a string representing the topic of the question
      - difficulty: a string representing the difficulty of the question
      - type: a string representing the type of the question (MCQ, Short Answer, or Long Answer)
      - question: a string representing the question
      - options: a list of strings representing the options for the MCQ question (only for MCQ questions)
      - image_options: a list of JSON object with the following keys:
        - filename: a string representing the filename of the image
        - prompt: a string representing the prompt for the image
        - is_correct: a boolean representing whether the image is correct or not
      - answer: a string representing the answer to the question, even if there are multiple answers
      - marks: an integer representing the marks for the question
      - question_images: a list of JSON object with the following keys:
        - filename: a string representing the filename of the image
        - prompt: a string representing the prompt for the image
      - diagrams: a list of Python code to generate a diagram for the question, each item in the list represents a diagram for the question
    - total_marks: an integer representing the total marks for the homework
**RULES**:
  - Generate questions based on the given input.
  - The questions should cover the topics, skills, and difficulties specified in the input.
  - The total marks of the questions should match the total marks specified in the input.
  - MCQ questions should have 4 options, and only one option should be correct.
  - For MCQ questions, either provide normal options or image options, not both.
  - For Non-MCQ questions, if there are multiple correct answers, provide all the correct answers.
  - Ensure questions and options do not contain Python code.
  - question_images should be used to provide images for the question.
  - image_options should be used to provide images as options for the MCQ question.
  - answer should be a string even if there are multiple correct answers. For example, if the answer is "A" and "B", provide "A, B".
  - If the question needs a diagram, provide the Python code to generate the diagram accurately.
    - The code should be executable and should generate the diagram "without any errors".
    - The code can be generated using any other library that can generate diagrams.
    - The code should include the necessary imports and commands to generate the diagram.
    - matplotlib, seaborn, plotly, sympy, pillow, etc., can be used to generate the diagrams.
    - The diagram should be saved as an image file with the filename "question_{{counter}}.png" where counter is the question number starting from 1. If the question has multiple diagrams, use "question_{{counter}}_{{diagram_number}}.png".
    - The diagram should be cleared after saving to avoid overlapping of diagrams.
    - Do not include the information from the diagram in the question, as it may lead to redundancy or unintentionally provide hints toward the answer, which is not desirable.
    - Do not ask questions that require the student to draw the diagram themselves.
    - If the question references multiple figures like square, triangle, circle, etc., either include all the figures in one diagram or provide separate diagrams for each figure.
    - If the question diagram python codes requires an image, provide the filename of the image and a prompt for the image to be generated.
    - The diagrams should be relevant to the question and should help in answering the question. The diagram should be complete and self-explanatory. The diagrams should not be misleading. So ensure that the question, answer, and diagram are consistent.
    
**EXAMPLE**:
  **INPUT**:
    {{"class": "3","subject":"English","topic":"Compound words","skills":["Form compound words with pictures","Form compound words","Form and use compound words"],"difficulties":["A01","A02","A03"],"question_types":["MCQ","Short Answer","Long Answer"],"number_of_questions":{{"mcq":4,"short_answer":3,"long_answer":3}},"marks":{{"mcq":1,"short_answer":2,"long_answer":4,"total":22}}}}
  **OUTPUT WITH DIAGRAM AND IMAGE PROMPTS**:
    {{"questions":[{{"skills": ["Form compound words with pictures"],"topic":"Compound words","difficulty":"A01","type":"MCQ","question":"Which combination of pictures forms the compound word 'butterfly'?","options":["Butter + Fly","Butter + Ball","Butter + Milk","Butter + Cup"],"answer":"Butter + Fly","marks":1,"question_images":[{{"filename":"butter.png","prompt":"A close-up photograph of a stick of golden yellow butter on a white porcelain plate. The butter is slightly softened, with a knife resting beside it that has just been used to cut a slice. There are small beads of moisture on the surface of the butter, giving it a fresh appearance. The lighting is soft and warm, emphasizing the creamy texture of the butter. In the background, out of focus, there's a hint of a rustic wooden table, suggesting a country kitchen setting."}},{{"filename":"fly.png","prompt":"A macro photograph of a common housefly (Musca domestica) perched on a reflective surface. The fly is captured in sharp focus, revealing intricate details of its compound eyes, translucent wings, and bristly body. Its legs are slightly splayed, gripping the surface. The lighting is bright and even, highlighting the metallic sheen of the fly's exoskeleton, which shows hues of deep blue-black with hints of green. The background is slightly out of focus, suggesting a clean, bright environment. The image captures the fly from a slight side angle, emphasizing its distinctive profile and the complexity of its wing structure."}}],"diagrams":["import matplotlib.pyplot as plt\nfrom PIL import Image\n\n# Create a blank white canvas\ncanvas = Image.new('RGB', (500, 250), 'white')\n\n# Open images\nimg1 = Image.open('butter.png').resize((100, 100))\nimg2 = Image.open('fly.png').resize((100, 100))\n\n# Paste images on canvas\ncanvas.paste(img1, (50, 75))\ncanvas.paste(img2, (200, 75))\n\n# Save the final image\ncanvas.save('question_1.png')"]}}]}}
"""
