from fastapi import FastAPI

from app.api.routes.auth import router as auth_router
from app.api.routes.health import router as health_router
from app.api.routes.workspaces import router as workspace_router
from app.api.routes.workflows import router as workflow_router
from app.api.routes.workflow_nodes import router as workflow_node_router
from app.api.routes.workflow_edges import router as workflow_edge_router
from app.api.routes.executions import router as execution_router
from app.core.exceptions import AppException
from app.core.exception_handlers import app_exception_handler
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)


app = FastAPI(
    title="AI Workflow Automation API",
    version="0.1.0",
)

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(workspace_router)
app.include_router(workflow_router)
app.include_router(workflow_node_router)
app.include_router(workflow_edge_router)
app.include_router(execution_router)

app.add_exception_handler(
    AppException,
    app_exception_handler,
)


@app.get("/")
async def root():
    
    return {
        "message": "AI Workflow Automation API"
    }