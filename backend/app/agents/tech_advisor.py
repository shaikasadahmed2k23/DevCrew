from crewai import Agent, LLM
from app.config import settings

llm = LLM(
    model=f"groq/{settings.model_name}",
    api_key=settings.groq_api_key
)

def get_tech_advisor() -> Agent:
    return Agent(
        role="Tech Stack Advisor",
        goal=(
            "Analyse the user's project goal and honestly evaluate whether "
            "CrewAI is the best fit. If yes, explain why and confirm. "
            "If another stack is better, recommend it clearly with reasoning, "
            "then let the user choose."
        ),
        backstory=(
            "You are a pragmatic solutions architect who has built projects "
            "across every major tech stack. You have no bias — you only care "
            "about what is the best tool for the job. You are honest even if "
            "it means recommending against CrewAI. You present options clearly "
            "and let the user decide."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
        max_iter=5,
        max_rpm=10
    )