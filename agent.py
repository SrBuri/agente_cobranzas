from langchain.schema import (
    SystemMessage,
    HumanMessage,
)
from config import cargar_flujo, get_model
from supabase_client import obtener_cliente_random

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
)

messages = [
    SystemMessage(content=flujo_personalizado),
]

def responder(usuario: str) -> str:
    messages.append(HumanMessage(content=usuario))
    respuesta = chat.invoke(messages)
    messages.append(respuesta)
    return respuesta.content

def cerrar(respuesta: str) -> bool:
    frases_cierre = [
        "gracias por su tiempo",
        "que tenga un buen día",
        "hasta luego",
        "nos despedimos",
        "¡hasta la próxima!",
        "Le agradezco su tiempo"
        "deseo un buen día"
    ]
    return any(frase in  respuesta.lower() for frase in frases_cierre)

def obtener_cliente():
    return cliente_activo