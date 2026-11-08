from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.workflow import WorkflowCreate, WorkflowResponse
from app.services.workflow_service import WorkflowService


router = APIRouter(
    prefix="/workspaces/{workspace_id}/workflows",
    tags=["Workflows"],
)


@router.post(
    "",
    response_model=WorkflowResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_workflow(
    workspace_id: UUID,
    data: WorkflowCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = WorkflowService(db)

    workflow = await service.create(
        data=data,
        workspace_id=workspace_id,
        current_user=current_user,
    )

    await db.commit()

    return workflow


@router.get(
    "",
    response_model=list[WorkflowResponse],
)
async def list_workflows(
    workspace_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = WorkflowService(db)

    workflows = await service.list_for_workspace(
        workspace_id=workspace_id,
        current_user=current_user,
    )

    return workflows