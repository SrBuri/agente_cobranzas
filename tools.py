from supabase_client import supabase
from langchain.tools import Tool
from datetime import datetime, timedelta
import dateparser

def consultar_cliente(contrato: str) -> str:
    res = supabase.table("clientes").select("*").eq("contrato", contrato).eq("activo", True).execute()
    data = res.data
    if not data:
        return "No se encontró ningún cliente con ese contrato."
    cliente = data[0]
    return (
        f"Nombre: {cliente['nombre']}, "
        f"Deuda: {cliente['monto_deuda']} USD, "
        f"Facturas vencidas: {cliente['facturas_vencidas']}, "
        f"Teléfono: {cliente['telefono1']}"
    )

def registrar_compromiso(datos: str) -> str:
    """
    Formato esperado: "contrato=C-001234;monto=30.5;fecha=2025-08-01;canal=Servipagos"
    """
    try:
        partes = dict(p.split("=") for p in datos.split(";"))
        contrato = partes["contrato"]
        monto = partes["monto"]
        fecha = partes["fecha"]
        canal = partes["canal"]
        
        cliente = supabase.table("clientes").select("id_cliente").eq("contrato", contrato).single().execute().data
        if not cliente:
            return "Contrato no encontrado"
        
        supabase.table("compromisos_pago").insert({
            "cliente_id": cliente["id_cliente"],
            "monto_acordado": monto,
            "fecha_pago": fecha,
            "canal_pago": canal
        }).execute()
        
        return "Compromiso registrado correctamente."
    except Exception as e:
        return f"Error al registrar el compromiso {str(e)}"

def registrar_objecion(datos: str) -> str:
    """
    Formato: "contrato=C-001234;tipo=Falta de dinero;mensaje=Estoy desempleado"
    """
    try:
        partes = dict(p.split("=") for p in datos.split(";"))
        contrato = partes["contrato"]
        tipo = partes["tipo"]
        mensaje = partes["mensaje"]
        
        cliente = supabase.table("clientes").select("id_cliente").eq("contrato", contrato).single().execute().data
        if not cliente:
            return "Contrato no encontrado"
        
        supabase.table("objeciones_cliente").insert({
            "cliente_id": cliente["id_cliente"],
            "tipo_objecion": tipo,
            "mensaje": mensaje
        }).execute()
        
        return "Objeción registrada correctamente."
    except Exception as e:
        return f"Error al registrar objeción: {str(e)}"

def interpretar_fecha(fecha_natural: str) -> str:
    """
    Convierte expresiones como 'mañana', 'el viernes', 'en 3 días'
    en una fecha exacta en formato YYYY-MM-DD.
    """
    resultado = dateparser.parse(fecha_natural, languages=['es'])
    if resultado:
        return resultado.strftime("%Y-%m-%d")
    return "No se pudo interpretar la fecha"

tools = [
    Tool.from_function(
        func=consultar_cliente,
        name="ConsultarCliente",
        description="Consulta los datos de un cliente por su número de contrato. Usa este formato: 'C-001234'"
    ),
    Tool.from_function(
        func=registrar_compromiso,
        name="RegistrarCompromiso",
        description="Registra un compromiso de pago solo si el cliente confirma. Formato: 'contrato=C-001234;monto=30.5;fecha=2025-08-01;canal=Servipagos'"
    ),
    Tool.from_function(
        func=registrar_objecion,
        name="RegistrarObjecion",
        description="Registra una objeción reportada por el cliente. Formato: 'contrato=C-001234;tipo=Falta de dinero;mensaje=Estoy desempleado'"
    ),
    Tool.from_function(
        func=interpretar_fecha,
        name="InterpretarFechaRelativa",
        description=(
            "Convierte expresiones naturales de tiempo como 'mañana', 'el viernes' o 'en 3 días' "
            "en una fecha exacta con formato 'YYYY-MM-DD'. Úsalo cuando el cliente mencione "
            "una fecha de pago relativa."
        )
    )
]