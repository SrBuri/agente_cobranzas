import dateparser
from langchain.tools import Tool, tool

from supabase_client import supabase


@tool
def consultar_cliente(contrato: str) -> str:
    """
    Consulta los datos de un cliente por su número de contrato.
    Usa este formato: 'C-001234'
    """
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

@tool
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

@tool
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

@tool
def interpretar_fecha(fecha_natural: str) -> str:
    """
    Convierte expresiones como 'mañana', 'el viernes', 'en 3 días'
    en una fecha exacta en formato YYYY-MM-DD.
    """
    resultado = dateparser.parse(fecha_natural, languages=['es'])
    if resultado:
        return resultado.strftime("%Y-%m-%d")
    return "No se pudo interpretar la fecha"

@tool
def verificar_medio_pago(name_canal: str) -> str:
    """
    verifica que el medio de pago este disponible
    """
    canales_valido = ["Servipagos", "Mi Vecino", "Banco del Barrio", "Red de Servicios Facilito", "Western Union", "Banco del Pacífico", "Banco Guayaquil", "Banco Machala", "Banco Pichincha", "Banco Bolivariano"]
    if name_canal.strip().title() in canales_valido:
        return "Canal valido"
    else:
        return (f"'{name_canal}' no es un canal autorizado. "
            "Los canales válidos son: "
            + ", ".join(canales_valido) + "."
        )

@tool
def actualizar_datos_cliente(datos: str) -> str:
    """
    Actualiza los datos de contacto del cliente.
    Formato esperado: "contrato=C-001234;telefono1=0999999999,telefono2=1151565;direccion=Calle Falsa 123;referencias=Frente al colegio San Marcos"
    Todos los campos excepto 'contrato' son opcionales.
    """
    try:
        partes = dict(p.split("=") for p in datos.split(";") if "=" in p)
        contrato = partes.get("contrato")
        if not contrato:
            return "Falta el número de contrato."

        cliente = supabase.table("clientes").select("id_cliente").eq("contrato", contrato).single().execute().data
        if not cliente:
            return "Contrato no encontrado."

        updates = {}
        if "telefono" in partes:
            updates["telefono1"] = partes["telefono1"]
        if "telefono2" in partes:
            updates["telefono2"] = partes["telefono2"]
        if "direccion" in partes:
            updates["direccion"] = partes["direccion"]
        if "referencias" in partes:
            updates["referencias"] = partes["referencias"]

        if not updates:
            return "No se proporcionaron datos para actualizar."

        supabase.table("clientes").update(updates).eq("id_cliente", cliente["id_cliente"]).execute()
        return "Datos actualizados correctamente."
    except Exception as e:
        return f"Error al actualizar datos: {str(e)}"

tools = [
    Tool.from_function(
        func=consultar_cliente,
        name="ConsultarCliente",
        description="Consulta los datos de un cliente por su número de contrato. Usa este formato: 'C-001234'"
    ),
    Tool.from_function(
        func=registrar_compromiso,
        name="RegistrarCompromiso",
        description="Registra un compromiso de pago solo si el cliente confirma. Esta herramienta solo puede usarse una vez por sesión.. Formato: 'contrato=C-001234;monto=30.5;fecha=2025-08-01;canal=Servipagos'"
    ),
    Tool.from_function(
        func=registrar_objecion,
        name="RegistrarObjecion",
        description="Registra una objeción del cliente. Esta herramienta solo puede usarse una vez por sesión.. Luego de usarla, no se debe volver a insistir en el pago. Formato: 'contrato=C-001234;tipo=Falta de dinero;mensaje=Estoy desempleado'"
    ),
    Tool.from_function(
        func=interpretar_fecha,
        name="InterpretarFechaRelativa",
        description=(
            "Convierte expresiones naturales de tiempo como 'mañana', 'el viernes' o 'en 3 días' "
            "en una fecha exacta con formato 'YYYY-MM-DD'. Úsalo cuando el cliente mencione "
            "una fecha de pago relativa."
        )
    ),
    Tool.from_function(
        func=verificar_medio_pago,
        name="VerificarMedioDePago",
        description=(
            "Valida si el canal de pago proporcionado por el cliente es válido." 
            "Úsalo cuando el cliente diga por dónde va a pagar."
        )
    ),
    Tool.from_function(
    func=actualizar_datos_cliente,
    name="ActualizarDatosCliente",
    description=(
        "Actualiza datos de contacto del cliente como teléfono, dirección o referencias. "
        "Formato: 'contrato=C-001234;telefono1=0999999999;telefono2=1955156;direccion=Av. Quito 123;referencias=Frente al colegio San Marcos'"
    )
)
]