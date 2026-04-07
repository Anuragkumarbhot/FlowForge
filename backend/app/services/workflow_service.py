from app.db.database import workflows_collection
from app.queue.redis_queue import enqueue_task


async def create_workflow(data: dict):

    result = await workflows_collection.insert_one(data)

    return {
        "workflow_id": str(result.inserted_id)
    }


async def trigger_workflow(workflow_id: str):

    workflow = await workflows_collection.find_one(
        {"_id": workflow_id}
    )

    if not workflow:
        return {"error": "Workflow not found"}

    # Send to worker queue
    enqueue_task(
        "execute_workflow",
        workflow
    )

    return {
        "message": "Workflow triggered"
    }
