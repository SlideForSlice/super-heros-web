from fastapi import FastAPI

app = FastAPI()


@app.get("/articles")
async def get_articles():
    return {"message": "Hello World"}


