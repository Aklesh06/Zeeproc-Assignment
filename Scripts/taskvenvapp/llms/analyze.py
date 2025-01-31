from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langgraph.graph import Graph

llm = ChatOpenAI(model="gpt-4", temperature=0)

prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that categorizes tasks based on their description."),
    ("user", "Categorize the following task description: {description}. Possible categories: Bug, Feature Request, Improvement, Other."),
])

def preprocess_description(description: str) -> str:
    return description.strip()

def query_llm(description: str) -> str:
    prompt = prompt_template.format_messages(description=description)
    response = llm.invoke(prompt)
    return response.content

def extract_category(response: str) -> str:
    return response.split(":")[-1].strip()

workflow = Graph()
workflow.add_node("preprocess", preprocess_description)
workflow.add_node("query", query_llm)
workflow.add_node("extract", extract_category)

workflow.add_edge("preprocess", "query")
workflow.add_edge("query", "extract")

workflow.set_entry_point("preprocess")
workflow.set_finish_point("extract")

analyzer = workflow.compile()