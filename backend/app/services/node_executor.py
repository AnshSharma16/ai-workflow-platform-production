from typing import Any
from app.adapters.factory import AdapterFactory
from app.models.workflow_node import WorkflowNode
import logging

class NodeExecutor:

    async def execute(
        self,
        node: WorkflowNode,
        input_data: dict[str, Any],
    ) -> dict[str, Any]:

        logger.info(
            "Node execution started",
            extra={
                "execution_id": str(execution.id),
                "node_id": str(current_node.id),
                "attempt": attempt,
            },
        )
        adapter = AdapterFactory.get_adapter(
            node.node_type
        )

        return await adapter.execute(
            node.config,
            input_data,
        )