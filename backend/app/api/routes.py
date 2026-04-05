import os
import uuid
import asyncio
from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
from app.crews.build_crew import run_devcrew
from app.zip_packager import create_zip, get_project_name

router = APIRouter()

build_store = {}


class GoalRequest(BaseModel):
    goal: str
    chosen_stack: Optional[str] = "crewai"


class BuildStatus(BaseModel):
    build_id: str
    status: str
    message: str
    progress: Optional[int] = 0
    result: Optional[dict] = None


def run_build_task(build_id: str, goal: str, chosen_stack: str):
    try:
        build_store[build_id]["status"] = "running"

        agent_stages = [
            (10, "Goal Analyst is understanding your project..."),
            (25, "Tech Advisor is evaluating the best stack..."),
            (42, "Planner is designing the folder structure..."),
            (60, "Coder is writing all project files..."),
            (80, "Tester is reviewing the code..."),
            (92, "QA Agent is doing the final quality check..."),
        ]

        original_run = run_devcrew.__wrapped__ if hasattr(run_devcrew, '__wrapped__') else None

        import threading

        stage_index = [0]

        def update_progress():
            import time
            for i, (pct, msg) in enumerate(agent_stages):
                if build_store[build_id]["status"] != "running":
                    break
                build_store[build_id]["progress"] = pct
                build_store[build_id]["message"] = msg
                time.sleep(25)

        progress_thread = threading.Thread(target=update_progress, daemon=True)
        progress_thread.start()

        result = run_devcrew(
            user_goal=goal,
            chosen_stack=chosen_stack
        )

        build_store[build_id]["message"] = "Packaging your project into a ZIP file..."
        build_store[build_id]["progress"] = 96

        project_name = get_project_name(result.get("goal_analysis", ""))

        zip_path = create_zip(
            code_output=result.get("code", ""),
            qa_summary=result.get("qa_summary", ""),
            goal_analysis=result.get("goal_analysis", ""),
            project_name=project_name,
            chosen_stack=chosen_stack
        )

        build_store[build_id]["status"] = "complete"
        build_store[build_id]["message"] = "DEVCREW BUILD COMPLETE - READY FOR DOWNLOAD"
        build_store[build_id]["progress"] = 100
        build_store[build_id]["zip_path"] = zip_path
        build_store[build_id]["project_name"] = project_name
        build_store[build_id]["result"] = {
            "goal_analysis": result.get("goal_analysis", ""),
            "tech_advice": result.get("tech_advice", ""),
            "plan": result.get("plan", ""),
            "test_report": result.get("test_report", ""),
            "qa_summary": result.get("qa_summary", ""),
        }

    except Exception as e:
        build_store[build_id]["status"] = "failed"
        build_store[build_id]["message"] = f"Build failed: {str(e)}"
        build_store[build_id]["progress"] = 0
        
@router.get("/health")
def health_check():
    return {"status": "ok", "message": "DevCrew API is running"}


@router.post("/build", response_model=BuildStatus)
def start_build(request: GoalRequest, background_tasks: BackgroundTasks):
    """
    Starts a new build in the background.
    Returns a build_id the frontend uses to poll progress.
    """
    if not request.goal or len(request.goal.strip()) < 10:
        raise HTTPException(
            status_code=400,
            detail="Please describe your project in at least 10 characters."
        )

    build_id = str(uuid.uuid4())

    build_store[build_id] = {
        "status": "queued",
        "message": "Build queued. Starting your crew...",
        "progress": 0,
        "zip_path": None,
        "project_name": None,
        "result": None
    }

    background_tasks.add_task(
        run_build_task,
        build_id=build_id,
        goal=request.goal,
        chosen_stack=request.chosen_stack or "crewai"
    )

    return BuildStatus(
        build_id=build_id,
        status="queued",
        message="Build queued. Starting your crew...",
        progress=0
    )


@router.get("/build/{build_id}/status", response_model=BuildStatus)
def get_build_status(build_id: str):
    """
    Polls the status of a running build.
    Frontend calls this every few seconds to update the UI.
    """
    if build_id not in build_store:
        raise HTTPException(
            status_code=404,
            detail="Build ID not found."
        )

    build = build_store[build_id]

    return BuildStatus(
        build_id=build_id,
        status=build["status"],
        message=build["message"],
        progress=build["progress"],
        result=build.get("result")
    )


@router.get("/build/{build_id}/download")
def download_zip(build_id: str):
    """
    Returns the ZIP file for a completed build.
    """
    if build_id not in build_store:
        raise HTTPException(
            status_code=404,
            detail="Build ID not found."
        )

    build = build_store[build_id]

    if build["status"] != "complete":
        raise HTTPException(
            status_code=400,
            detail="Build is not complete yet."
        )

    zip_path = build.get("zip_path")

    if not zip_path or not os.path.exists(zip_path):
        raise HTTPException(
            status_code=404,
            detail="ZIP file not found. Please try building again."
        )

    project_name = build.get("project_name", "devcrew_project")

    return FileResponse(
        path=zip_path,
        media_type="application/zip",
        filename=f"{project_name}.zip"
    )


@router.delete("/build/{build_id}")
def delete_build(build_id: str):
    """
    Cleans up a build from memory.
    """
    if build_id not in build_store:
        raise HTTPException(
            status_code=404,
            detail="Build ID not found."
        )

    build = build_store.pop(build_id)

    zip_path = build.get("zip_path")
    if zip_path and os.path.exists(zip_path):
        os.remove(zip_path)

    return {"message": "Build deleted successfully."}
    
# from fastapi import APIRouter

# router = APIRouter()

# @router.get("/health")
# def health_check():
#     return {"status": "ok"}
