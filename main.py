from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"greeting": "Hello, World!", "message": "Welcome to FastAPI!"}


@app.get('/sim_test')
def sim_test(id:str = None):
    if id:
        return {id}
    else:
        return {"Hello world"}
