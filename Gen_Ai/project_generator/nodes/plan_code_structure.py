def plan_code_structure_node(state):
    import os
    os.makedirs("output/app/api/routes", exist_ok=True)
    os.makedirs("output/app/models", exist_ok=True)
    os.makedirs("output/app/services", exist_ok=True)
    os.makedirs("output/tests", exist_ok=True)
    return state