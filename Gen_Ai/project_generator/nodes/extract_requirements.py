def extract_requirements_node(state):
    from openai import OpenAI
    client = OpenAI()
    prompt = f"""
    Extract only FUNCTIONAL requirements from the following SRS:
    {state.pdf_text}
    Return as a bullet list.
    """
    response = client.chat.completions.create(
        model="gpt-4", 
        messages=[{"role": "user", "content": prompt}]
    )
    requirements_text = response.choices[0].message.content
    state.functional_requirements = requirements_text.split("\n")
    return state