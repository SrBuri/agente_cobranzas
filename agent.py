from langchain.schema import (
    SystemMessage,
    HumanMessage,
)
from config import cargar_flujo, get_model
from supabase_client import obtener_cliente_random
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from tools import tools

flujo = cargar_flujo()
chat = get_model()

cliente_activo = obtener_cliente_random()

flujo_personalizado = (
    flujo
    .replace("{nombre}", cliente_activo["nombre"])
    .replace("{contrato}", cliente_activo["contrato"])
    .replace("{facturas}", str(cliente_activo["facturas_vencidas"]))
    .replace("{deuda}", str(cliente_activo["monto_deuda"]))
    .replace("{telefono}", cliente_activo["telefono1"])
    .replace("{segmento}", cliente_activo["segmento"])
)

system = SystemMessage(content=flujo_personalizado)

prompt = ChatPromptTemplate.from_messages([
    system,
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

messages = [
    SystemMessage(content=flujo_personalizado)
]

agent = create_openai_functions_agent(
    llm=chat,
    tools=tools,
    prompt=prompt
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    return_intermediate_steps=True,
    handle_parsing_errors=True
)

def responder(usuario: str) -> str:
    messages.append(HumanMessage(content=usuario))
    respuesta = agent_executor.invoke({"input": usuario, "chat_history": messages})
    messages.append(HumanMessage(content=respuesta["output"]))
    return respuesta["output"]

def cerrar(respuesta: str) -> bool:
    frases_cierre = [
        "que tenga un buen día",
        "hasta luego",
        "nos despedimos",
        "¡hasta la próxima!",
        "Le agradezco su tiempo",
        "deseo un buen día",
        "Que tenga un excelente día"
    ]
    return any(frase in respuesta.lower() for frase in frases_cierre)

def obtener_cliente():
    return cliente_activo