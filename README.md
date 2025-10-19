# ThinkTrek AI Assistant 🤖🌱

An intelligent Rasa chatbot designed to help high school students explore biology topics and build capstone projects using the OpenStax Biology 2e textbook and OpenAI.

---

## 🚀 Features
- Summarizes textbook content by chapter and section
- Answers biology questions using GPT-3.5 and S3 content
- Suggests creative, topic-based capstone ideas
- Offers Socratic thinking mode and motivation prompts

---

## 🧠 Built With
- [Rasa Open Source](https://rasa.com/)
- [OpenAI API](https://platform.openai.com/)
- [AWS S3](https://aws.amazon.com/s3/)
- [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/)
- [Python 3.8+](https://www.python.org/)

---

## ⚙️ Setup Instructions

### 1. Clone the repository
git clone https://github.com/your-username/thinktrek-ai.git
cd thinktrek-ai

### 2. Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt

### 3. Add your .env file
cp .env.example .env
Then fill in your OpenAI and AWS credentials

### 4. Train the model
rasa train

### 5. Run the assistant
rasa run actions & rasa shell


