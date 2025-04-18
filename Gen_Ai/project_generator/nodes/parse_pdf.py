from langchain_community.document_loaders import PyPDFLoader


from PyPDF2 import PdfReader
async def parse_pdf_node(state):
    loader = PyPDFLoader("C:/Users/ddilip/Documents/GEN_AI/Final_Project/chatgpt/Employee_Handbook.pdf")
    pages = []
    async for page in loader.alazy_load():
        pages.append(page)
    reader = loader
    text = ""
    print("Aditya")
    print(f"{pages[0].metadata}\n")
    print(pages[0].page_content)
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return {'pdf_text': text}
