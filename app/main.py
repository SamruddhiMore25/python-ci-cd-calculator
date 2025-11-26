from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")


def compute(a: float, b: float, op: str) -> float:
    if op == "add":
        return a + b
    if op == "sub":
        return a - b
    if op == "mul":
        return a * b
    if op == "div":
        if b == 0:
            raise ValueError("Division by zero")
        return a / b
    raise ValueError(f"Unknown operation: {op}")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "result": None,
            "error": None,
            "a": "",
            "b": "",
            "op": "add",
        },
    )


@app.post("/calculate", response_class=HTMLResponse)
async def calculate(
    request: Request,
    a: str = Form(...),
    b: str = Form(...),
    op: str = Form(...),
):
    error = None
    result = None

    try:
        a_val = float(a)
        b_val = float(b)
        result = compute(a_val, b_val, op)
    except ValueError as e:
        error = str(e)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "result": result,
            "error": error,
            "a": a,
            "b": b,
            "op": op,
        },
    )
