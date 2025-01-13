from fastapi import FastAPI
import uvicorn
from starlette.middleware.cors import CORSMiddleware

from app.scrape.processes.scrape_process import ScrapeProcess

from app.auth.router import router as auth_router
from app.scrape.router import router as scrape_router
from app.config import client, env, fastapi_config, scrape_queue

scrape_process = ScrapeProcess(scrape_queue, env)
scrape_process.start()

app = FastAPI(**fastapi_config)


@app.on_event("shutdown")
def shutdown_db_client():
    client.close()


app.add_middleware(
    CORSMiddleware,
    allow_origins=env.CORS_ORIGINS,
    allow_methods=env.CORS_METHODS,
    allow_headers=env.CORS_HEADERS,
    allow_credentials=True,
)

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(scrape_router, prefix="/scrape", tags=["Scrape"])


def run():
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == '__main__':
    run()
