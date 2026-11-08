from uuid import UUID

from fastapi import APIRouter, Depends, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.execution import ExecutionCreate, ExecutionResponse
from app.schemas.node_execution import NodeExecutionResponse
from app.services.workflow_execution_service import (
    run_workflow_in_background,
    WorkflowExecutionService,
)


router = APIRouter(
    prefix="/workflows/{workflow_id}/executions",
    tags=["Executions"],
)


@router.post(
    "",
    response_model=ExecutionResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def start_execution(
    workflow_id: UUID,
    data: ExecutionCreate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = WorkflowExecutionService(db)

    execution = await service.start_execution(
        workflow_id=workflow_id,
        current_user=current_user,
        input_data=data.input_data,
    )
    
    background_tasks.add_task(
    run_workflow_in_background,
    execution.id,
    )

    await db.commit()

    return execution


@router.get(
    "",
    response_model=list[ExecutionResponse],
)
async def list_executions(
    workflow_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):

    service = WorkflowExecutionService(db)

    executions = await service.list_for_workflow(
        workflow_id=workflow_id,
        current_user=current_user,
    )

    return executions


@router.get(
    "/{execution_id}",
    response_model=ExecutionResponse,
)
async def get_execution(
    execution_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = WorkflowExecutionService(db)

    execution = await service.get_execution(
        execution_id=execution_id,
        current_user=current_user,
    )

    return execution

@router.get(
    "/{execution_id}/nodes",
    response_model=list[NodeExecutionResponse],
)
async def list_node_executions(
    execution_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = WorkflowExecutionService(db)

    node_executions = await service.list_node_executions(
        execution_id=execution_id,
        current_user=current_user,
    )

    return node_executions