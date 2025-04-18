
from langgraph.graph import StateGraph, END
from dataclasses import dataclass
from typing import Optional, List
from langchain_community.document_loaders import PyPDFLoader
from PyPDF2 import PdfReader
from project_generator.schema import SRSState
from project_generator.nodes.parse_pdf import parse_pdf_node
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import langchain
import os
from langchain_groq import ChatGroq
from pathlib import Path

os.environ["GROQ_API_KEY"] = "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"

# Replace 'new-model-name' with the actual new model name recommended by Groq
llm = ChatGroq(
    model_name="mistral-saba-24b",
    temperature=0,
    api_key=os.environ["GROQ_API_KEY"]
)

@dataclass
class SRSState:
    pdf_text: Optional[str] = None
    requirements: Optional[List[str]] = None
    validated: bool = False
    code_structure: Optional[dict] = None
    db_code: Optional[str] = None
    fastapi_code: Optional[str] = None
    model: Optional[any] = None  
    project_path: Optional[str] = None
    srs_analysis: Optional[str] = None
    code_snapshot: Optional[str] = None
    retrying: bool = False
    test_output: Optional[str] = None
    llm_calls: Optional[int] = None
    code_generation_success: Optional[bool] = None
    pdf_text: Optional[str] = None
    requirements: Optional[List[str]] = None
    validated: bool = False
    code_structure: Optional[dict] = None
    db_code: Optional[str] = None
    fastapi_code: Optional[str] = None
    

async def parse_pdf_node(state: SRSState) -> SRSState:
    loader = PyPDFLoader("C:/Users/ddilip/Documents/GEN_AI/Final_Project/Gen_Ai/Python_gen_ai.pdf")
    pages = []
    async for page in loader.alazy_load():
        pages.append(page)
    text = ""
    for page in pages:
        text += page.page_content + "\n"
    state.pdf_text = text
    return state

async def extract_requirements_node(state: SRSState) -> SRSState:
    print("Extracting requirements...")
    if not state.pdf_text:
        print("No PDF text available.")
        return state
    prompt = f"Extract key functional backend requirements from this SRS text:\n\n{state.pdf_text}"
    
    # Corrected input type
    extracted_text = await llm.ainvoke(prompt)
    
    # Optionally, split if the LLM returns a big text block
    state.requirements = extracted_text.content.strip().split("\n")
    return state

async def generate_code_node(state: SRSState) -> SRSState:
    
    print("Generating FastAPI code...")
    print(f"Generating modular route, service, and schema code...")
    if not state.model:
        state.model = ChatOpenAI(
            model="llama-3-70b-vision",
            temperature=0.25,
            openai_api_key=os.getenv("GROQ_API_KEY"),
            openai_api_base="https://api.groq.com/openai/v1",
        )
    project_path = "C:/Users/ddilip/Documents/GEN_AI/Final_Project/Gen_Ai/project"
    models_path = project_path / "app" / "models" / "models.py"
    tests_path = project_path / "tests"
    srs = state.srs_analysis
    last_code = state.code_snapshot or ""
    models_code = models_path.read_text() if models_path.exists() else "# models.py not found"
    test_files = []
    if tests_path.exists():
        for file in tests_path.glob("*.py"):
            test_files.append(f"\n# {file.name}\n" + file.read_text())
    test_info = "\n---\nThese are the tests that will be run against your code:\n" + "\n".join(test_files) if test_files else ""
    is_retry = state.retrying
    prev_test_output = state.test_output or ""
    base_prompt = f"""
You are a professional FastAPI engineer working in a production-grade environment.
You are tasked with generating clean, modular, production-level code for the following folders:
- app/api/routes/
- app/services/
- app/schemas/
The SQLAlchemy models you must build on are:
{models_code}
The system you are building is based on the following Software Requirements:
{srs}
{test_info}
Use this stack:
- FastAPI
- PostgreSQL (via SQLAlchemy ORM)
- Pydantic for schemas
- Alembic for migrations
- Pytest for testing
Compulsory:
- All database interaction must use SQLAlchemy ORM
- Use correct DB session patterns (e.g., Dependency Injection if needed)
- Use PostgreSQL-compatible datatypes and logic
- Do NOT generate boilerplate or placeholder logic
- Write real business logic that will pass the tests
- Follow clean code practices, proper naming, separation of concerns
- All return values should be valid, structured, and realistic
- Ensure routes are connected to FastAPI app in `main.py`
- Prefix each router with its appropriate API path:
  - /api/dashboard
  - /api/lms
  - /api/pods
  - /api/auth
Format your response with:
**app/path/to/file.py**
```python
<code>
```
Only include valid code files. No extra text or explanation.
"""
    prompt = retry_prompt if is_retry else base_prompt
    response = await state.model.ainvoke([
    SystemMessage(content="You are a professional backend engineer."),
    HumanMessage(content=prompt)
    ])
    lm_calls = (state.llm_calls or 0) + 1
    pattern = r"\*\*(.*?)\*\*\s*```(?:python)?\s*([\s\S]*?)\s*```"
    matches = re.findall(pattern, response.content)
    if not matches:
        print(f"No code blocks matched. LLM may not have followed format.")
    for rel_path, code in matches:
        try:
            file_path = project_path / rel_path.strip()
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, "w") as f:
                f.write(code.strip())
            print(f" Generated: {file_path}")
        except Exception as e:
            print(f"Failed to write {rel_path}: {e}")
    
    state.code_generation_success = True
    state.llm_calls = lm_calls
    return state


builder = StateGraph(SRSState)
builder.add_node("parse_pdf", parse_pdf_node)
builder.add_node("extract_requirements", extract_requirements_node)
builder.add_node("generate_code", generate_code_node)
builder.set_entry_point("parse_pdf")
builder.add_edge("parse_pdf", "extract_requirements")
builder.add_edge("extract_requirements", "generate_code")
builder.add_edge("generate_code", END)
