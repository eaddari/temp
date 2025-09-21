import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from source.repo_downloader.endpoints.status import router as status_router
from source.repo_downloader.endpoints.repo_download_api import router as download_repository

from source.upload_repo_on_blob.src.endpoints.endpoint_uploader import router as upload_router

from source.fetch_repo_from_blob.endpoints.api import router as fetch_repo_router


app = FastAPI(
    title="DocGen API",
    description="Web App to generate documentation with AI"
)

app.include_router(status_router)
app.include_router(download_repository)
app.include_router(upload_router)
app.include_router(fetch_repo_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

"""
Main entry point for running the DocGen API server.

Configures and starts the uvicorn server on host 0.0.0.0:8081
with info level logging.
"""
if __name__ == '__main__':
    server_configuration = uvicorn.Config(
        app,
        host="0.0.0.0",
        port=8081,
        log_level="info"
    )

    server = uvicorn.Server(server_configuration)
    server.run()