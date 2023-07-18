import uvicorn
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from handlers import start_router, insurance_router
from core.config import db_url


app = FastAPI()


register_tortoise(
    app,
    db_url=db_url,
    modules={'models': ['db.base']},
    generate_schemas=True,
    add_exception_handlers=True,
)

# Include all routers
app.include_router(start_router)
app.include_router(insurance_router)

if __name__ == "__main__":
    uvicorn.run("loader:app", host='0.0.0.0', port=8000)
