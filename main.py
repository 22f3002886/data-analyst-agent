from fastapi import FastAPI, UploadFile, File
from utils.task_parser import classify_task
from utils.scraper import scrape_wikipedia_table
from utils.analyzer import basic_analysis

app = FastAPI()

@app.post("/api/")
async def analyze(file: UploadFile = File(...)):
    content = await file.read()
    task = content.decode("utf-8")

    task_type = classify_task(task)

    if task_type == "scrape":
        try:
            df = scrape_wikipedia_table(task)
            answers = basic_analysis(df)
            return answers  # 👈 return just this array!
        except Exception as e:
            return {"error": str(e)}

    # Fallback for unsupported tasks (optional)
    return {"error": f"Unsupported task type: {task_type}"}