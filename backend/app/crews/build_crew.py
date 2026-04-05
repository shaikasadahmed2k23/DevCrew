
from crewai import Crew, Task, Process
from app.agents.goal_analyst import get_goal_analyst
from app.agents.tech_advisor import get_tech_advisor
from app.agents.planner import get_planner
from app.agents.coder import get_coder
from app.agents.tester import get_tester
from app.agents.qa import get_qa
import time

AGENT_DELAY = 25


def _crewai_plan_requirement():
    return (
        "CRITICAL: This must be a CrewAI project. "
        "The folder structure MUST include:\n"
        "- agents.py: Define Agent objects using crewai.Agent\n"
        "- tasks.py: Define Task objects using crewai.Task\n"
        "- crew.py: Assemble Crew using crewai.Crew with crew.kickoff()\n"
        "- main.py: Entry point that runs the crew\n"
        "- requirements.txt: Must include crewai, langchain-groq, python-dotenv\n"
        "- .env.example: Must include GROQ_API_KEY and MODEL_NAME\n"
        "- README.md: Setup instructions for this CrewAI project"
    )


def _crewai_code_requirement():
    return (
        "CRITICAL: You are building a CREWAI PROJECT. Generate these files with real working code:\n\n"
        "1. agents.py — from crewai import Agent, LLM\n"
        "   Create each agent with: role, goal, backstory, llm\n"
        "   Use: llm = LLM(model='groq/llama-3.1-8b-instant', api_key=os.getenv('GROQ_API_KEY'))\n\n"
        "2. tasks.py — from crewai import Task\n"
        "   Each task needs: description, expected_output, agent\n\n"
        "3. crew.py — from crewai import Crew, Process\n"
        "   Assemble all agents and tasks, call crew.kickoff()\n\n"
        "4. main.py — imports crew.py and runs it\n\n"
        "5. requirements.txt — include: crewai, langchain-groq, python-dotenv, litellm\n\n"
        "6. .env.example — include: GROQ_API_KEY=your_key_here, MODEL_NAME=llama-3.1-8b-instant\n\n"
        "7. README.md — full setup instructions for this CrewAI project\n\n"
        "The project must SOLVE THE USER'S GOAL using CrewAI agents — not just be a script."
    )


def run_devcrew(user_goal: str, chosen_stack: str = "crewai") -> dict:

    is_crewai = chosen_stack.lower() == "crewai"

    goal_analyst = get_goal_analyst()
    tech_advisor = get_tech_advisor()
    planner = get_planner()
    coder = get_coder(chosen_stack=chosen_stack)
    tester = get_tester()
    qa = get_qa()

    task_analyse = Task(
        description=(
            f"The user wants to build:\n\n{user_goal}\n\n"
            f"Analyse this goal. Extract in under 250 words:\n"
            f"1. One-sentence project summary\n"
            f"2. Key inputs\n"
            f"3. Key outputs\n"
            f"4. Constraints\n"
            f"5. Target users\n"
            f"6. Assumptions"
        ),
        expected_output=(
            "A concise project brief under 250 words: "
            "Summary, Inputs, Outputs, Constraints, Users, Assumptions."
        ),
        agent=goal_analyst
    )

    if is_crewai:
        advise_description = (
            f"The user has explicitly chosen CrewAI as their stack.\n\n"
            f"Your job is to CONFIRM this choice — do NOT recommend alternatives.\n"
            f"Explain in 3 bullet points why CrewAI is a good fit for this project.\n"
            f"End with: PROCEED WITH CREWAI\n\n"
            f"Keep response under 100 words."
        )
        advise_expected = "3 bullet points why CrewAI fits, ending with PROCEED WITH CREWAI."
    else:
        advise_description = (
            f"The user chose: {chosen_stack}\n\n"
            f"Evaluate if {chosen_stack} is the best fit in under 150 words.\n"
            f"If yes — 3 bullet points why.\n"
            f"If no — recommend alternative with 3 reasons.\n"
            f"State verdict: PROCEED WITH {chosen_stack.upper()} or ALTERNATIVE RECOMMENDED."
        )
        advise_expected = f"Verdict under 150 words for {chosen_stack}."

    task_advise = Task(
        description=advise_description,
        expected_output=advise_expected,
        agent=tech_advisor,
        context=[task_analyse]
    )

    plan_description = (
        f"Create a concise implementation plan. Max 300 words.\n\n"
        f"{_crewai_plan_requirement() if is_crewai else f'Plan a {chosen_stack} project with appropriate structure.'}\n\n"
        f"Include:\n"
        f"1. Complete folder structure\n"
        f"2. Dependencies list\n"
        f"3. Environment variables needed\n"
        f"4. Setup steps (numbered, one line each)"
    )

    task_plan = Task(
        description=plan_description,
        expected_output=f"A concise plan under 300 words with folder structure, deps, env vars, setup steps.",
        agent=planner,
        context=[task_analyse, task_advise]
    )

    code_description = (
        f"Write complete working code for every file in the plan.\n\n"
        f"{_crewai_code_requirement() if is_crewai else f'Build this as a proper {chosen_stack} project.'}\n\n"
        f"Rules:\n"
        f"1. Start each file with: # FILE: path/to/filename.ext\n"
        f"2. Write FULL working code — no stubs, no TODOs\n"
        f"3. For API keys write: YOUR_KEY_HERE with a comment\n"
        f"4. Output all files sequentially"
    )

    task_code = Task(
        description=code_description,
        expected_output=(
            f"Complete {'CrewAI' if is_crewai else chosen_stack} project files, "
            f"each starting with # FILE: path/to/file."
        ),
        agent=coder,
        context=[task_analyse, task_plan]
    )

    task_test = Task(
        description=(
            f"Review the code files. Check for:\n"
            f"1. Broken imports\n"
            f"2. Incomplete functions\n"
            f"3. Missing files from the plan\n"
            f"{'4. Verify agents.py, tasks.py, crew.py all exist and use CrewAI properly' if is_crewai else ''}\n\n"
            f"List: FILE | PROBLEM | FIX\n"
            f"If none: ALL FILES PASSED REVIEW\n"
            f"Max 150 words."
        ),
        expected_output="Issues list under 150 words, or ALL FILES PASSED REVIEW.",
        agent=tester,
        context=[task_plan, task_code]
    )

    task_qa = Task(
        description=(
            f"Final check in under 100 words:\n"
            f"1. README.md present\n"
            f"2. .env.example present\n"
            f"3. Credentials have placeholders\n"
            f"{'4. agents.py, tasks.py, crew.py all present' if is_crewai else ''}\n\n"
            f"End with exactly:\n"
            f"DEVCREW BUILD COMPLETE - READY FOR DOWNLOAD"
        ),
        expected_output=(
            "Checklist under 100 words ending with: "
            "DEVCREW BUILD COMPLETE - READY FOR DOWNLOAD"
        ),
        agent=qa,
        context=[task_test]
    )

    all_tasks = [task_analyse, task_advise, task_plan, task_code, task_test, task_qa]
    task_names = ["goal_analysis", "tech_advice", "plan", "code", "test_report", "qa_summary"]
    results = {}

    for i, task in enumerate(all_tasks):
        crew = Crew(
            agents=[goal_analyst, tech_advisor, planner, coder, tester, qa],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )

        max_retries = 5
        for attempt in range(max_retries):
            try:
                result = crew.kickoff()
                results[task_names[i]] = str(result.raw) if result else ""
                break
            except Exception as e:
                error_str = str(e)
                if "rate_limit_exceeded" in error_str:
                    wait_time = 30 * (attempt + 1)
                    print(f"\n⏳ Rate limit on task {i+1}. Waiting {wait_time}s (attempt {attempt+1}/{max_retries})...\n")
                    time.sleep(wait_time)
                else:
                    raise e
        else:
            results[task_names[i]] = ""

        if i < len(all_tasks) - 1:
            print(f"\n⏸️  Waiting {AGENT_DELAY}s before next agent...\n")
            time.sleep(AGENT_DELAY)

    return {
        "goal_analysis": results.get("goal_analysis", ""),
        "tech_advice": results.get("tech_advice", ""),
        "plan": results.get("plan", ""),
        "code": results.get("code", ""),
        "test_report": results.get("test_report", ""),
        "qa_summary": results.get("qa_summary", ""),
        "final_output": results.get("qa_summary", "")
    }



# from crewai import Crew, Task, Process
# from app.agents.goal_analyst import get_goal_analyst
# from app.agents.tech_advisor import get_tech_advisor
# from app.agents.planner import get_planner
# from app.agents.coder import get_coder
# from app.agents.tester import get_tester
# from app.agents.qa import get_qa
# import time


# AGENT_DELAY = 25


# def run_devcrew(user_goal: str, chosen_stack: str = "crewai") -> dict:

#     goal_analyst = get_goal_analyst()
#     tech_advisor = get_tech_advisor()
#     planner = get_planner()
#     coder = get_coder()
#     tester = get_tester()
#     qa = get_qa()

#     task_analyse = Task(
#         description=(
#             f"The user wants to build the following project:\n\n"
#             f"{user_goal}\n\n"
#             f"Analyse this goal deeply. Extract:\n"
#             f"1. What the project does (in one clear sentence)\n"
#             f"2. Key inputs the system takes\n"
#             f"3. Key outputs the system produces\n"
#             f"4. Any constraints or preferences mentioned\n"
#             f"5. The target users\n"
#             f"6. Any missing information that must be assumed\n\n"
#             f"Produce a structured project brief. Keep it concise — max 300 words."
#         ),
#         expected_output=(
#             "A concise project brief under 300 words with sections: "
#             "Project Summary, Inputs, Outputs, Constraints, Target Users, Assumptions."
#         ),
#         agent=goal_analyst
#     )

#     task_advise = Task(
#         description=(
#             f"The user has chosen to build with: {chosen_stack}\n\n"
#             f"Based on the project brief, evaluate in maximum 200 words:\n"
#             f"1. Is {chosen_stack} the best fit?\n"
#             f"2. If yes — 3 short bullet points why.\n"
#             f"3. If no — recommend alternative with 3 short bullet points.\n"
#             f"4. Final verdict: PROCEED WITH {chosen_stack.upper()} "
#             f"or ALTERNATIVE RECOMMENDED.\n"
#             f"Be concise. No long paragraphs."
#         ),
#         expected_output=(
#             "A verdict under 200 words: PROCEED or ALTERNATIVE RECOMMENDED "
#             "with 3 bullet point reasons."
#         ),
#         agent=tech_advisor,
#         context=[task_analyse]
#     )

#     task_plan = Task(
#         description=(
#             f"Create a concise implementation plan. Max 400 words.\n\n"
#             f"Include:\n"
#             f"1. Folder structure (files and folders only, no descriptions)\n"
#             f"2. Dependencies list\n"
#             f"3. Environment variables needed\n"
#             f"4. Setup steps (numbered, one line each)\n\n"
#             f"Be brief. The Coder agent will fill in the details."
#         ),
#         expected_output=(
#             "A concise plan under 400 words with folder structure, "
#             "dependencies, env vars, and setup steps."
#         ),
#         agent=planner,
#         context=[task_analyse, task_advise]
#     )

#     task_code = Task(
#         description=(
#             f"Write complete code for every file in the plan.\n\n"
#             f"CRITICAL REQUIREMENT: The user chose '{chosen_stack}' as their stack.\n\n"
#             f"{'If the stack is crewai, the generated project MUST itself use CrewAI agents to accomplish the goal. This means the output project should have: agents defined using crewai Agent class, tasks defined using crewai Task class, a crew assembled using crewai Crew class, and a main.py that runs crew.kickoff(). The project should solve the user goal BY USING CrewAI agents, not just be a regular Python script.' if chosen_stack == 'crewai' else f'Build this project using {chosen_stack} best practices.'}\n\n"
#             f"Rules:\n"
#             f"1. Start each file with: # FILE: path/to/filename.ext\n"
#             f"2. Write FULL file contents — no stubs or TODOs\n"
#             f"3. For secrets use: YOUR_KEY_HERE with a comment explaining where to get it\n"
#             f"4. Include README.md and .env.example\n"
#             f"5. Keep each file focused and minimal\n\n"
#             f"Output files sequentially."
#         ),
#         expected_output=(
#             f"All project files built with {chosen_stack}, each starting with "
#             f"# FILE: path/to/file, plus README.md and .env.example."
#         ),
#         agent=coder,
#         context=[task_analyse, task_advise, task_plan]
#     )
#     task_test = Task(
#         description=(
#             f"Review the code files. Check for:\n"
#             f"1. Broken imports\n"
#             f"2. Incomplete functions\n"
#             f"3. Missing files from the plan\n\n"
#             f"List issues as: FILE | PROBLEM | FIX (one line each).\n"
#             f"If none found: ALL FILES PASSED REVIEW.\n"
#             f"Keep response under 200 words."
#         ),
#         expected_output=(
#             "Issues list under 200 words, or ALL FILES PASSED REVIEW."
#         ),
#         agent=tester,
#         context=[task_plan, task_code]
#     )

#     task_qa = Task(
#         description=(
#             f"Final check. Confirm in under 150 words:\n"
#             f"1. README.md present and complete\n"
#             f"2. .env.example present\n"
#             f"3. All credentials have placeholders\n"
#             f"4. Folder structure matches plan\n\n"
#             f"End your response with exactly:\n"
#             f"DEVCREW BUILD COMPLETE - READY FOR DOWNLOAD"
#         ),
#         expected_output=(
#             "Confirmation checklist under 150 words ending with: "
#             "DEVCREW BUILD COMPLETE - READY FOR DOWNLOAD"
#         ),
#         agent=qa,
#         # context=[task_plan, task_code, task_test]
#         context=[task_test]
#     )

#     all_tasks = [
#         task_analyse,
#         task_advise,
#         task_plan,
#         task_code,
#         task_test,
#         task_qa
#     ]

#     results = {}
#     task_names = [
#         "goal_analysis",
#         "tech_advice",
#         "plan",
#         "code",
#         "test_report",
#         "qa_summary"
#     ]

#     for i, task in enumerate(all_tasks):
#         crew = Crew(
#             agents=[
#                 goal_analyst, tech_advisor, planner,
#                 coder, tester, qa
#             ],
#             tasks=[task],
#             process=Process.sequential,
#             verbose=True
#         )

#         max_retries = 5
#         for attempt in range(max_retries):
#             try:
#                 result = crew.kickoff()
#                 results[task_names[i]] = str(result.raw) if result else ""
#                 break
#             except Exception as e:
#                 error_str = str(e)
#                 if "rate_limit_exceeded" in error_str:
#                     wait_time = 30 * (attempt + 1)
#                     print(
#                         f"\n⏳ Rate limit on task {i+1}. "
#                         f"Waiting {wait_time}s "
#                         f"(attempt {attempt+1}/{max_retries})...\n"
#                     )
#                     time.sleep(wait_time)
#                 else:
#                     raise e
#         else:
#             results[task_names[i]] = ""

#         if i < len(all_tasks) - 1:
#             print(f"\n⏸️  Waiting {AGENT_DELAY}s before next agent...\n")
#             time.sleep(AGENT_DELAY)

#     return {
#         "goal_analysis": results.get("goal_analysis", ""),
#         "tech_advice": results.get("tech_advice", ""),
#         "plan": results.get("plan", ""),
#         "code": results.get("code", ""),
#         "test_report": results.get("test_report", ""),
#         "qa_summary": results.get("qa_summary", ""),
#         "final_output": results.get("qa_summary", "")
#     }