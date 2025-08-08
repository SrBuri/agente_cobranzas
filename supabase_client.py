import os
import random

from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_API_KEY")

supabase: Client = create_client(supabase_url, supabase_key)

def obtener_cliente_random():
    res = supabase.table("clientes").select("*").execute()
    clientes = res.data
    if clientes:
        return random.choice(clientes)
    else:
        return None