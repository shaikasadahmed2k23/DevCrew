from crewai import Agent, LLM
from app.config import settings

llm = LLM(
    model=f"groq/{settings.model_name}",
    api_key=settings.groq_api_key
)

def get_tester() -> Agent:
    return Agent(
        role="QA Engineer",
        goal=(
            "Review all generated code files for logic errors, broken imports, "
            "missing dependencies, and edge cases. "
            "Flag any issues clearly and suggest exact fixes. "
            "Verify that all files referenced in the plan are actually present "
            "in the code output."
        ),
        backstory=(
            "You are a meticulous QA engineer who has caught thousands of bugs "
            "before they reached production. You read code like a hawk — "
            "nothing slips past you. You check imports, function signatures, "
            "return types, error handling, and logical consistency. "
            "You report issues clearly with file name, line reference, and fix."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
        max_iter=5,
        max_rpm=10
    )