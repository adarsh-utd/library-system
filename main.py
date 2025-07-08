import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from router.user import router as user_router
from router.book import router as book_router
app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(book_router)

if __name__=="__main__":
    uvicorn.run(app=app,host="localhost",port=8000)
