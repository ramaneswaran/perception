import uvicorn

if __name__ == "__main__":
    uvicorn.run("perception.main:app",reload=True)
