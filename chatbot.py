from langgraph.graph import StateGraph, MessagesState
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import SystemMessage, HumanMessage
from tools import query_knowledge_base, search_for_social_package_information
import os


prompt = """#Предназначение: 

Ты — чат-бот для обслуживания сотрудников компании обратившиеся с вопросами к HR-отделу. Ты можешь помочь сотруднику достичь перечисленных ниже целей.

#Цели:

1. Ответить на часто задаваемые вопросы, с которыми сотрудники обращаются к HR-отделу.
2. Если на базе данных недостаточно информации по вопросу сотрудника, направить сотрудника к живому HR-специалисту без каких-либо комментарий.
3. Если вопросы не относятся к HR, сообщить сотруднику, что ты не можешь ответить на такие вопросы и попросить задавать вопросы строго относящие к HR.

#Тон:

Отзывчивый и дружелюбный. Обращайся с сотрудниками на вы.  """

class State(MessagesState):
    question: str
    answer: str

chatbot_system_message = SystemMessage(content=(prompt))

with open('./.env', 'r', encoding='utf-8') as f:
    for line in f:
        key, value = line.strip().split('=')
        os.environ[key] = value

tools = [query_knowledge_base, search_for_social_package_information]

llm = ChatOpenAI(
    model="gpt-4o",
    openai_api_key=os.environ['OPENAI_API_KEY']
)

llm_with_prompt = llm.bind_tools(tools)


def call_agent(message_state: State):
    
    question = HumanMessage(content=message_state.get("question", ""))
    response = llm_with_prompt.invoke([chatbot_system_message] + message_state["messages"] + [question])

    return State(
        messages = [question, response],
        question = message_state.get("question", None),
        answer = response.content
    )

def is_there_tool_calls(state: State):
    last_message = state['messages'][-1]
    if last_message.tool_calls:
        return 'tool_node'
    else:
        return '__end__'


graph = StateGraph(State)

tool_node = ToolNode(tools)

graph.add_node('agent', call_agent)
graph.add_node('tool_node', tool_node)

graph.add_conditional_edges(
    "agent",
    is_there_tool_calls
)
graph.add_edge('tool_node', 'agent')

graph.set_entry_point('agent')

memory = MemorySaver()
app = graph.compile(checkpointer=memory)