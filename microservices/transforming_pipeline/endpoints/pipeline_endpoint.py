from fastapi import APIRouter
from source.splitter import ManageTransforming
from endpoints.schemas import PipelineRequest

router = APIRouter(prefix="/v5", tags=["Transforming Pipeline"])

@router.post("/transforming_pipeline")
async def run_pipeline(request: PipelineRequest):
    print(f"Received request: {request}")
    try:
        pipeline = ManageTransforming(request.input_path, request.keep_comments)
        data = await pipeline.run_steps(request.steps)
        print(f"Step names: {request.steps}")
        return {
            "status": "success",
            "message": "Pipeline executed successfully.",
            "data": data
        }
    except Exception as e:
        return {
            "status": "error",
            "message": "Failed to run pipeline.",
            "data": None,
            "error": str(e)
        }