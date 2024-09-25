from typing import List, Optional

from fastapi import APIRouter, Depends, Query

from letta.schemas.job import Job
from letta.server.rest_api.utils import get_letta_server
from letta.server.server import SyncServer

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("/", response_model=List[Job], operation_id="list_jobs")
def list_jobs(
    server: "SyncServer" = Depends(get_letta_server),
    source_id: Optional[str] = Query(None, description="Only list jobs associated with the source."),
):
    """
    List all jobs.
    """
    actor = server.get_current_user()

    # TODO: add filtering by status
    jobs = server.list_jobs(user_id=actor.id)
    if source_id:
        # can't be in the ORM since we have source_id stored in the metadata_
        jobs = [job for job in jobs if job.metadata_.get("source_id") == source_id]
    return jobs


@router.get("/active", response_model=List[Job], operation_id="list_active_jobs")
def list_active_jobs(
    server: "SyncServer" = Depends(get_letta_server),
):
    """
    List all active jobs.
    """
    actor = server.get_current_user()

    return server.list_active_jobs(user_id=actor.id)


@router.get("/{job_id}", response_model=Job, operation_id="get_job")
def get_job(
    job_id: str,
    server: "SyncServer" = Depends(get_letta_server),
):
    """
    Get the status of a job.
    """

    return server.get_job(job_id=job_id)
