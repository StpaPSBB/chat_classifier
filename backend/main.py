from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from routers import classifier_router

app = FastAPI()
app.include_router(classifier_router.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)