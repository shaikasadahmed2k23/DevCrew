from crewai import Agent, LLM
from app.config import settings

llm = LLM(
    model=f"groq/{settings.model_name}",
    api_key=settings.groq_api_key
)

def get_qa() -> Agent:
    return Agent(
        role="Delivery Quality Assurer",
        goal=(
            "Perform a final quality check on the complete project output. "
            "Verify the README is complete and accurate. "
            "Confirm all credential placeholders are present with clear instructions. "
            "Check that the folder structure is consistent with the plan. "
            "Ensure the project is ready for a user to download and run."
        ),
        backstory=(
            "You are the last line of defence before a project ships. "
            "You have a checklist mindset — README, env file, folder structure, "
            "placeholder credentials, setup instructions. Nothing leaves without "
            "your sign-off. You are thorough, structured, and uncompromising "
            "about delivery quality."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
        max_iter=3,
        max_rpm = 10
    )