def generate_fastapi_code_node(state):
    from jinja2 import Template
    api_template = Template("""
from fastapi import APIRouter
router = APIRouter()
{% for func in functions %}
@router.get("/{{ func|lower|replace(' ', '_') }}")
def {{ func|lower|replace(' ', '_') }}():
    return {"message": "{{ func }} endpoint"}
{% endfor %}
    """)
    for module in ['user', 'item']:
        with open(f"output/app/api/routes/{module}.py", "w") as f:
            f.write(api_template.render(functions=[f"get {module}", f"create {module}"]))
    with open("output/app/api/routes/__init__.py", "w") as f:
        f.write("")
    with open("output/app/models/__init__.py", "w") as f:
        f.write("")
    with open("output/app/services/__init__.py", "w") as f:
        f.write("")
    return state