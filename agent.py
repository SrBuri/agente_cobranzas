import json
from typing import Any, List, TypedDict, Annotated

from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage
from langchain_core.messages import AnyMessage
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from config import cargar_flujo, get_model
from supabase_client import obtener_cliente_random
from tools import tools

chat = get_model()
cliente = obtener_cliente_random()
flujo = cargar_flujo()
flujo = (flujo
    .replace("{nombre}", cliente["nombre"])
    .replace("{contrato}", cliente["contrato"])
    .replace("{facturas}", str(cliente["facturas_vencidas"]))
    .replace("{deuda}", str(cliente["monto_deuda"]))
    .replace("{telefono}", cliente["telefono1"])
    .replace("{segmento}", cliente["segmento"])
)

class State(TypedDict):
    messages: Annotated[List[AnyMessage], add_messages]

prompt = ChatPromptTemplate.from_messages([
    ("system", flujo),
    ("placeholder", "{messages}")
])

agent = prompt | chat.bind_tools(tools)

def recibir_input(State):
    user_input = input("👤 Cliente: ")
    State["messages"].append(HumanMessage(content=user_input))
    return State

def ejecutar_agente(State):
    print(State["messages"])
    output = agent.invoke(State)
    respuesta = str(output.content)
    State["messages"].append(output)
    if respuesta == "":
        return State
    else:
        print(f"\n🤖 Daniela: {respuesta}\n")
    return State

def verificar_cierre(State):
    frases_cierre = [
        "que tenga un buen día",
        "hasta luego",
        "nos despedimos",
        "¡hasta la próxima!",
        "le agradezco su tiempo",
        "deseo un buen día",
        "que tenga un excelente día"
    ]
    if any(frase in State["messages"][-1].content.lower() for frase in frases_cierre):
        return "finalizar"
    return "recibir_input"


def decision_combined(State: dict[str, Any]) -> str:
    if verificar_cierre(State) == "finalizar":
        return "finalizar"
    decision = tools_condition(State)
    if decision == "__end__":
        return "recibir_input"
    return decision

graph = StateGraph(State)
graph.add_node("recibir_input", recibir_input)
graph.add_node("ejecutar_agente", ejecutar_agente)
graph.add_node("tools", ToolNode(tools))
graph.add_node("finalizar", lambda State: print("✅ Conversación finalizada."))

graph.set_entry_point("recibir_input")
graph.add_edge("recibir_input", "ejecutar_agente")
graph.add_conditional_edges("ejecutar_agente", decision_combined, {
    "recibir_input": "recibir_input",
    "finalizar": "finalizar",
    "tools": "tools"
})
graph.add_edge("tools", "ejecutar_agente")
graph.set_finish_point("finalizar")

app = graph.compile()

""" with open("grafo.png", "wb") as f:
    f.write(app.get_graph().draw_mermaid_png())
print("✅ Diagrama guardado como grafo.png") """