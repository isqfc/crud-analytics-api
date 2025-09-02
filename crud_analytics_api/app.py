from http import HTTPStatus
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from crud_analytics_api.sales import router as sales_router
from crud_analytics_api.schemas import Message

app = FastAPI()
app.include_router(sales_router.router)


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
