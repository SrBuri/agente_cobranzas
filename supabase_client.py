"""
Módulo de conexión y operaciones con la base de datos Supabase.

Este módulo se encarga de:
- Cargar credenciales desde variables de entorno (.env)
- Crear un cliente Supabase
- Proveer funciones utilitarias para obtener datos desde la base
"""

import os
import random

from dotenv import load_dotenv
from supabase import create_client, Client

# Carga las variables de entorno
load_dotenv()

# Carga las variables de entorno
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_API_KEY")

# Carga las variables de entorno
supabase: Client = create_client(supabase_url, supabase_key)

def obtener_cliente_random():
    """
    Obtiene un cliente aleatorio desde la tabla `clientes` en Supabase.

    Returns:
        dict | None: Diccionario con los datos del cliente o None si no hay registros.
    
    Ejemplo de retorno:
        {
            "id_cliente": 1,
            "nombre": "Juan Pérez",
            "contrato": "C-001234",
            "monto_deuda": 100.50,
            "facturas_vencidas": 2,
            "telefono1": "0999999999",
            "segmento": "Residencial"
        }
    """
    
    res = supabase.table("clientes").select("*").execute()
    clientes = res.data
    if clientes:
        return random.choice(clientes)
    else:
        return None