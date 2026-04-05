from crewai import Agent, LLM
from app.config import settings

llm = LLM(
    model=f"groq/{settings.model_name}",
    api_key=settings.groq_api_key
)

def get_planner() -> Agent:
    return Agent(
        role="Project Planner",
        goal=(
            "Take the fully understood project goal and break it down into "
            "a precise implementation plan. Define the complete folder structure, "
            "list every file that needs to be created, and describe what each "
            "file must contain. Output a structured plan the Coder agent can "
            "follow exactly."
        ),
        backstory=(
            "You are a lead software architect who specialises in project "
            "scaffolding and system design. You think in folder structures, "
            "module boundaries, and clean separation of concerns. "
            "Your plans are so clear that a junior developer could follow them "
            "without any questions."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
        max_iter=5
    )