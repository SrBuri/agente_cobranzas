from supabase import create_client, Client
import os
from dotenv import load_dotenv
import random

load_dotenv

supabase_url = os.getenv("supabase_url")
supabase_key = os.getenv("supabase_api_key")

supabase: Client = create_client(supabase_url, supabase_key)

def obtener_cliente_random():
    res = supabase.table("clientes").select("*").execute()
    clientes = res.data
    if clientes:
        return random.choice(clientes)
    else:
        return None