from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from api.auth import router as auth_router
from api.sales import router as sales_router
from api.users import router as users_router

app = FastAPI()
app.include_router(sales_router.router)
app.include_router(users_router.router)
app.include_router(auth_router.router)


# w key reference
@app.get('/', status_code=HTTPStatus.OK)
def read_root():
   """ 
   Show some interesting endpoints 
   Returns:
        A interactable user interface - HTMLResponse
   """

   sales_routes = [f"<li><a href={r.path}>{r.path}</a> - {r.methods}</li>" for r in sales_router.router.routes if r.methods == {'GET'}]
   html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <title>API Online</title>
    </head>
    <body>
    
    <h1>Endpoints</h1>
    <p>Interesting Sales Endpoints.</p>
    <ul>
        {''.join(sales_routes)}
    </ul>
    </body>
    </html>
    """
   return HTMLResponse(content=html)
