from fastapi import FastAPI

app = FastAPI(title="DDD Rentals API", description="API for the DDD Rentals project")

@app.get("/health")
def health_check():
    return {"ok": True}