from pydantic import BaseModel
from typing import Optional, Any, List, Dict
class SRSState(BaseModel):
    pdf_text: Optional[str] = None
    requirements: Optional[List[str]] = None
    validated: bool = False
    code_structure: Optional[Dict] = None
    db_code: Optional[str] = None
    fastapi_code: Optional[str] = None
    model: Optional[Any] = None  
    project_path: Optional[str] = None
    srs_analysis: Optional[str] = None
    code_snapshot: Optional[str] = None
    retrying: bool = False
    test_output: Optional[str] = None
    llm_calls: Optional[int] = None
    code_generation_success: Optional[bool] = None
