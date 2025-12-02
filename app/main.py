from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.db import SessionLocal, Calculation, init_db

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Create DB tables at startup
init_db()


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
    db = SessionLocal()
    history = db.query(Calculation).order_by(Calculation.id.desc()).limit(10).all()

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "result": None,
            "error": None,
            "a": "",
            "b": "",
            "op": "add",
            "history": history,
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

    db = SessionLocal()

    try:
        a_val = float(a)
        b_val = float(b)
        result = compute(a_val, b_val, op)

        # Save calculation to DB
        calc = Calculation(
            a=a_val,
            b=b_val,
            operator=op,
            result=result,
        )
        db.add(calc)
        db.commit()

    except ValueError as e:
        error = str(e)

    # Fetch latest history
    history = db.query(Calculation).order_by(Calculation.id.desc()).limit(10).all()

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "result": result,
            "error": error,
            "a": a,
            "b": b,
            "op": op,
            "history": history,
        },
    )


# ✅ NEW: route to clear entire history
@app.post("/clear_history")
async def clear_history():
    db = SessionLocal()
    db.query(Calculation).delete()
    db.commit()
    db.close()

    # Redirect back to home page
    return RedirectResponse(url="/", status_code=303)
