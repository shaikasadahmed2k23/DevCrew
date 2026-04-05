from crewai import Agent, LLM
from app.config import settings

llm = LLM(
    model=f"groq/{settings.model_name}",
    api_key=settings.groq_api_key
)

CREWAI_PATTERN = """
CORRECT CrewAI pattern — follow EXACTLY:

# FILE: agents.py
import os
from crewai import Agent, LLM
from dotenv import load_dotenv
load_dotenv()

llm = LLM(
    model=f"groq/{os.getenv('MODEL_NAME', 'llama-3.1-8b-instant')}",
    api_key=os.getenv('GROQ_API_KEY')
)

researcher = Agent(
    role='Senior Researcher',
    goal='Research the given topic thoroughly',
    backstory='An expert researcher with years of experience',
    llm=llm,
    verbose=True
)

writer = Agent(
    role='Content Writer',
    goal='Write clear engaging content based on research',
    backstory='A skilled writer who turns research into content',
    llm=llm,
    verbose=True
)

# FILE: tasks.py
from crewai import Task
from agents import researcher, writer

research_task = Task(
    description='Research this topic in depth: {topic}',
    expected_output='A detailed research summary about {topic}',
    agent=researcher
)

write_task = Task(
    description='Write a blog post using the research about {topic}',
    expected_output='A well-structured blog post about {topic}',
    agent=writer,
    context=[research_task]
)

# FILE: crew.py
from crewai import Crew, Process
from agents import researcher, writer
from tasks import research_task, write_task

def run_crew(topic: str):
    crew = Crew(
        agents=[researcher, writer],
        tasks=[research_task, write_task],
        process=Process.sequential,
        verbose=True
    )
    result = crew.kickoff(inputs={'topic': topic})
    return result

# FILE: main.py
from crew import run_crew

if __name__ == '__main__':
    topic = input('Enter topic: ')
    result = run_crew(topic)
    print(result)

# FILE: requirements.txt
crewai>=1.0.0
litellm>=1.0.0
python-dotenv>=1.0.0

# FILE: .env.example
GROQ_API_KEY=your_groq_api_key_here
MODEL_NAME=llama-3.1-8b-instant

STRICT RULES FOR CREWAI:
- NEVER subclass Agent — always instantiate directly
- NEVER pass agent as a string — always pass the Agent object
- ALWAYS import LLM from crewai — never use ChatGroq
- ALWAYS use groq/ prefix: model=f"groq/{os.getenv('MODEL_NAME')}"
- NEVER mix Flask or FastAPI into agents.py or tasks.py
- NEVER call Task as a function — it is a class, instantiate it
- context= in Task must be a list of Task objects, never empty unless first task
"""

LANGCHAIN_PATTERN = """
CORRECT LangChain Node.js pattern — follow EXACTLY:

# FILE: backend/app.js
const express = require('express');
const multer = require('multer');
const path = require('path');
const { processQuestion } = require('./services/langChainService');
require('dotenv').config();

const app = express();
const upload = multer({ dest: 'uploads/' });

app.use(express.json());
app.use(express.static(path.join(__dirname, '../frontend/public')));

app.post('/api/ask', upload.single('pdf'), async (req, res) => {
  try {
    const pdfPath = req.file.path;
    const question = req.body.question;
    const answer = await processQuestion(pdfPath, question);
    res.json({ answer });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.listen(process.env.PORT || 3000, () => {
  console.log('Server running on port', process.env.PORT || 3000);
});

# FILE: backend/services/langChainService.js
const { ChatGroq } = require('@langchain/groq');
const { PDFLoader } = require('@langchain/community/document_loaders/fs/pdf');
const { RecursiveCharacterTextSplitter } = require('langchain/text_splitter');
const { HuggingFaceTransformersEmbeddings } = require('@langchain/community/embeddings/hf_transformers');
const { MemoryVectorStore } = require('langchain/vectorstores/memory');
const { RetrievalQAChain } = require('langchain/chains');
require('dotenv').config();

async function processQuestion(pdfPath, question) {
  const loader = new PDFLoader(pdfPath);
  const docs = await loader.load();

  const splitter = new RecursiveCharacterTextSplitter({
    chunkSize: 500,
    chunkOverlap: 50,
  });
  const splitDocs = await splitter.splitDocuments(docs);

  const embeddings = new HuggingFaceTransformersEmbeddings();
  const vectorStore = await MemoryVectorStore.fromDocuments(splitDocs, embeddings);

  const llm = new ChatGroq({
    apiKey: process.env.GROQ_API_KEY,
    model: process.env.MODEL_NAME || 'llama-3.1-8b-instant',
  });

  const chain = RetrievalQAChain.fromLLM(llm, vectorStore.asRetriever());
  const result = await chain.call({ query: question });
  return result.text;
}

module.exports = { processQuestion };

# FILE: frontend/public/index.html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>PDF Chatbot</title>
  <style>
    body { font-family: sans-serif; max-width: 600px; margin: 40px auto; padding: 0 20px; }
    input, button { margin: 10px 0; padding: 8px; width: 100%; }
    button { background: #4f46e5; color: white; border: none; cursor: pointer; border-radius: 6px; }
    #answer { background: #f3f4f6; padding: 16px; border-radius: 8px; margin-top: 16px; }
  </style>
</head>
<body>
  <h1>PDF Chatbot</h1>
  <form id="chatForm">
    <label>Upload PDF:</label>
    <input type="file" id="pdfFile" accept=".pdf" required>
    <label>Your Question:</label>
    <input type="text" id="question" placeholder="Ask anything about the PDF..." required>
    <button type="submit">Ask</button>
  </form>
  <div id="answer" style="display:none"></div>
  <script>
    document.getElementById('chatForm').addEventListener('submit', async (e) => {
      e.preventDefault();
      const formData = new FormData();
      formData.append('pdf', document.getElementById('pdfFile').files[0]);
      formData.append('question', document.getElementById('question').value);
      const res = await fetch('/api/ask', { method: 'POST', body: formData });
      const data = await res.json();
      const answerDiv = document.getElementById('answer');
      answerDiv.style.display = 'block';
      answerDiv.textContent = data.answer || data.error;
    });
  </script>
</body>
</html>

# FILE: package.json
{
  "name": "pdf-chatbot",
  "version": "1.0.0",
  "scripts": {
    "start": "node backend/app.js",
    "dev": "nodemon backend/app.js"
  },
  "dependencies": {
    "@langchain/groq": "^0.0.14",
    "@langchain/community": "^0.0.40",
    "langchain": "^0.1.0",
    "express": "^4.18.2",
    "multer": "^1.4.5",
    "dotenv": "^16.3.1"
  },
  "devDependencies": {
    "nodemon": "^3.0.1"
  }
}

# FILE: .env.example
GROQ_API_KEY=your_groq_api_key_here
# Get your free Groq API key from: https://console.groq.com
MODEL_NAME=llama-3.1-8b-instant
PORT=3000

# FILE: README.md
# PDF Chatbot — LangChain + Groq

## What it does
Upload any PDF and ask questions about it. Powered by LangChain and Groq.

## Setup
1. Install Node.js (v18+)
2. Run: npm install
3. Copy .env.example to .env: copy .env.example .env
4. Add your GROQ_API_KEY to .env (free key at https://console.groq.com)
5. Run: npm start
6. Open: http://localhost:3000

## How to get your Groq API key
1. Go to https://console.groq.com
2. Sign up for free
3. Go to API Keys section
4. Create a new key and copy it to your .env file

STRICT RULES FOR LANGCHAIN NODEJS:
- ALWAYS use require() — never use import/export (CommonJS only)
- NEVER use PyPDFLoader — that is Python only
- Use PDFLoader from @langchain/community
- Use MemoryVectorStore — it works without external dependencies
- Use HuggingFaceTransformersEmbeddings — works offline
- NEVER mix import and require in same file
- ALWAYS use @langchain/groq for ChatGroq
- NEVER import from 'langchain/chat-groq' — wrong path
- NEVER use FAISS in Node.js — use MemoryVectorStore instead
"""

VANILLA_PATTERN = """
CORRECT Vanilla Python pattern:

# FILE: main.py
import os
from dotenv import load_dotenv
from groq import Groq
load_dotenv()

client = Groq(api_key=os.getenv('GROQ_API_KEY'))

def ask(prompt: str) -> str:
    response = client.chat.completions.create(
        model=os.getenv('MODEL_NAME', 'llama-3.1-8b-instant'),
        messages=[{'role': 'user', 'content': prompt}]
    )
    return response.choices[0].message.content

if __name__ == '__main__':
    while True:
        user_input = input('You: ')
        if user_input.lower() == 'quit':
            break
        print(f'AI: {ask(user_input)}')

# FILE: requirements.txt
groq>=0.4.0
python-dotenv>=1.0.0

# FILE: .env.example
GROQ_API_KEY=your_groq_api_key_here
MODEL_NAME=llama-3.1-8b-instant

STRICT RULES FOR VANILLA:
- Use the groq Python SDK directly
- No LangChain, no CrewAI
- Keep it minimal and clean
"""

NODEJS_PATTERN = """
CORRECT Node.js pattern:

# FILE: index.js
require('dotenv').config();
const Groq = require('groq-sdk');

const groq = new Groq({ apiKey: process.env.GROQ_API_KEY });

async function ask(prompt) {
    const completion = await groq.chat.completions.create({
        model: process.env.MODEL_NAME || 'llama-3.1-8b-instant',
        messages: [{ role: 'user', content: prompt }],
    });
    return completion.choices[0].message.content;
}

async function main() {
    const answer = await ask('Hello, what can you do?');
    console.log(answer);
}

main();

# FILE: package.json
{
  "name": "devcrew-project",
  "version": "1.0.0",
  "main": "index.js",
  "scripts": { "start": "node index.js" },
  "dependencies": {
    "groq-sdk": "^0.4.0",
    "dotenv": "^16.0.0"
  }
}

# FILE: .env.example
GROQ_API_KEY=your_groq_api_key_here
MODEL_NAME=llama-3.1-8b-instant

STRICT RULES FOR NODEJS:
- Use groq-sdk npm package
- Use async/await throughout
- Never use Python syntax
"""


def _get_pattern_for_stack(stack: str) -> str:
    stack = stack.lower()
    if stack == "crewai":
        return CREWAI_PATTERN
    elif stack == "langchain":
        return LANGCHAIN_PATTERN
    elif stack in ["vanilla", "vanilla python"]:
        return VANILLA_PATTERN
    elif stack in ["nodejs", "node.js", "node"]:
        return NODEJS_PATTERN
    else:
        return LANGCHAIN_PATTERN


def get_coder(chosen_stack: str = "crewai") -> Agent:
    pattern = _get_pattern_for_stack(chosen_stack)
    stack_name = chosen_stack.upper()

    return Agent(
        role="Senior Software Engineer",
        goal=(
            f"Write complete, working {stack_name} code for every file in the project plan. "
            f"Follow the {stack_name} reference pattern EXACTLY. "
            f"Never mix patterns from different stacks."
        ),
        backstory=(
            f"You are a senior engineer specialising in {stack_name} projects. "
            f"You follow the reference pattern below strictly and never deviate. "
            f"You write complete files with no stubs or TODOs. "
            f"You never mix imports or patterns from different frameworks.\n\n"
            f"YOUR {stack_name} REFERENCE PATTERN:\n{pattern}"
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
        max_iter=10,
        max_rpm=10
    )


# from crewai import Agent, LLM
# from app.config import settings

# llm = LLM(
#     model=f"groq/{settings.model_name}",
#     api_key=settings.groq_api_key
# )

# CREWAI_EXAMPLE = """
# CORRECT CrewAI pattern to follow exactly:

# # FILE: agents.py
# import os
# from crewai import Agent, LLM
# from dotenv import load_dotenv
# load_dotenv()

# llm = LLM(
#     model=f"groq/{os.getenv('MODEL_NAME', 'llama-3.1-8b-instant')}",
#     api_key=os.getenv('GROQ_API_KEY')
# )

# researcher = Agent(
#     role='Senior Researcher',
#     goal='Research the given topic thoroughly and find key facts',
#     backstory='An expert researcher with years of experience finding accurate information',
#     llm=llm,
#     verbose=True
# )

# writer = Agent(
#     role='Content Writer',
#     goal='Write a clear, engaging blog post based on research findings',
#     backstory='A skilled writer who turns research into compelling content',
#     llm=llm,
#     verbose=True
# )

# # FILE: tasks.py
# from crewai import Task
# from agents import researcher, writer

# research_task = Task(
#     description='Research the following topic in depth: {topic}. Find key facts, trends, and insights.',
#     expected_output='A detailed research summary with key facts and insights about {topic}',
#     agent=researcher
# )

# write_task = Task(
#     description='Using the research provided, write a comprehensive blog post about {topic}.',
#     expected_output='A well-structured blog post of at least 500 words about {topic}',
#     agent=writer,
#     context=[research_task]
# )

# # FILE: crew.py
# from crewai import Crew, Process
# from agents import researcher, writer
# from tasks import research_task, write_task

# def run_crew(topic: str):
#     crew = Crew(
#         agents=[researcher, writer],
#         tasks=[research_task, write_task],
#         process=Process.sequential,
#         verbose=True
#     )
#     result = crew.kickoff(inputs={'topic': topic})
#     return result

# # FILE: main.py
# from crew import run_crew

# if __name__ == '__main__':
#     topic = input('Enter the topic to research and write about: ')
#     result = run_crew(topic)
#     print('\\n=== FINAL OUTPUT ===')
#     print(result)

# # FILE: requirements.txt
# crewai>=1.0.0
# litellm>=1.0.0
# python-dotenv>=1.0.0
# langchain-groq>=0.1.0

# # FILE: .env.example
# GROQ_API_KEY=your_groq_api_key_here
# # Get your free Groq API key from: https://console.groq.com
# MODEL_NAME=llama-3.1-8b-instant

# # FILE: README.md
# # Project Name

# ## Setup
# 1. Clone this repo
# 2. Create virtual env: python -m venv venv
# 3. Activate: venv\\Scripts\\activate (Windows) or source venv/bin/activate (Mac/Linux)
# 4. Install deps: pip install -r requirements.txt
# 5. Copy .env.example to .env: copy .env.example .env
# 6. Add your GROQ_API_KEY to .env (get free key at https://console.groq.com)
# 7. Run: python main.py
# """


# def get_coder() -> Agent:
#     return Agent(
#         role="Senior Software Engineer",
#         goal=(
#             "Write complete, working code for every file in the project plan. "
#             "When building CrewAI projects, follow the EXACT pattern provided — "
#             "never subclass Agent, never pass agent as a string, always instantiate "
#             "Agent objects directly with role, goal, backstory, and llm parameters."
#         ),
#         backstory=(
#             "You are a senior engineer who specialises in CrewAI projects. "
#             "You have memorised the correct CrewAI patterns and never deviate from them. "
#             "You know that Agent must be instantiated directly, not subclassed. "
#             "You know that Task.agent must be an Agent object, not a string. "
#             "You know that Crew takes lists of Agent and Task objects directly. "
#             "You always use LLM from crewai with groq/ prefix for the model name. "
#             "You write complete files with no stubs or TODOs. "
#             f"\n\nCREWAI REFERENCE PATTERN:\n{CREWAI_EXAMPLE}"
#         ),
#         llm=llm,
#         verbose=True,
#         allow_delegation=False,
#         max_iter=10,
#         max_rpm=10
#     )


# # from crewai import Agent, LLM
# # from app.config import settings

# # llm = LLM(
# #     model=f"groq/{settings.model_name}",
# #     api_key=settings.groq_api_key
# # )

# # def get_coder() -> Agent:
# #     return Agent(
# #         role="Senior Software Engineer",
# #         goal=(
# #             "Write complete, production-ready code for every file in the project plan. "
# #             "Follow the planner's folder structure exactly. "
# #             "For any API keys or secrets, use placeholder comments like "
# #             "# REPLACE WITH YOUR KEY — and add a comment explaining where to get it. "
# #             "Output each file's full path and complete contents."
# #         ),
# #         backstory=(
# #             "You are a full-stack senior engineer with deep expertise in Python, "
# #             "Node.js, and web technologies. You write clean, well-commented, "
# #             "production-quality code. You never leave incomplete functions or "
# #             "TODO stubs — every file you write is fully implemented. "
# #             "You are meticulous about imports, dependencies, and file paths."
# #         ),
# #         llm=llm,
# #         verbose=True,
# #         allow_delegation=False,
# #         max_iter=10,
# #         max_rpm=10
# #     )