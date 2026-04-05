from crewai import Agent, LLM
from app.config import settings

llm = LLM(
    model=f"groq/{settings.model_name}",
    api_key=settings.groq_api_key
)

def get_goal_analyst() -> Agent:
    return Agent(
        role="Goal Analyst",
        goal=(
            "Deeply understand the user's project idea by asking smart, "
            "targeted clarifying questions. Extract inputs, outputs, constraints, "
            "scale, and any technical preferences until the goal is crystal clear."
        ),
        backstory=(
            "You are a senior software consultant with 15 years of experience "
            "turning vague ideas into precise technical specifications. "
            "You never assume — you always ask until you fully understand. "
            "You are patient, thorough, and structured in your thinking."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
        max_iter=5,
        max_rpm=10
    )