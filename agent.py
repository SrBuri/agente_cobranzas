"""
Módulo que define el agente conversacional y su flujo de interacción.

- Carga y personaliza el flujo inicial con datos de un cliente aleatorio.
- Define el estado de la conversación y nodos de ejecución.
- Implementa funciones para recibir input, ejecutar el modelo y decidir flujo.
"""

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

# Instancia del modelo y cliente aleatorio
chat = get_model()
cliente = obtener_cliente_random()


# Personalización del flujo con datos del cliente
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
    """
    Estado de la conversación.

    Attributes:
        messages (list): Lista de mensajes intercambiados en la sesión.
    """
    messages: Annotated[List[AnyMessage], add_messages]

# Plantilla de prompt inicial
prompt = ChatPromptTemplate.from_messages([
    ("system", flujo),
    ("placeholder", "{messages}")
])

# Configuración del agente con herramientas
agent = prompt | chat.bind_tools(tools)

def warmup_model():
    """Envia un mensaje invisible al modelo para precargar conexión y contexto."""
    print("⚡ Precargando modelo...")
    _ = agent.invoke({"messages": [HumanMessage(content="...")]})
    print("✅ Modelo precargado\n")

def recibir_input(State):
    """Solicita entrada del usuario (cliente) y la agrega al estado."""
    user_input = input("\n👤 Cliente: ")
    State["messages"].append(HumanMessage(content=user_input))
    return State

def ejecutar_agente(State):
    """Ejecuta el modelo con el estado actual y muestra la respuesta."""
    #print("\n🤖 Daniela:")
    output = agent.invoke(State)
    respuesta = str(output.content)
    State["messages"].append(output)
    if respuesta == "":
        return State
    else:
        print(f"\n🤖 Daniela: {respuesta}\n")
    return State

def verificar_cierre(State):
    """Verifica si la última respuesta del agente indica cierre de conversación."""
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
    """Determina el siguiente paso de ejecución."""
    if verificar_cierre(State) == "finalizar":
        return "finalizar"
    decision = tools_condition(State)
    if decision == "__end__":
        return "recibir_input"
    return decision

# Definición del grafo de estados
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

# Precarga del modelo
warmup_model()
app = graph.compile()

""" with open("grafo.png", "wb") as f:
    f.write(app.get_graph().draw_mermaid_png())
print("✅ Diagrama guardado como grafo.png") """