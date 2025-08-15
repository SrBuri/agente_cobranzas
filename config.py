"""
Módulo de configuración y utilidades para el modelo conversacional.

- Carga variables de entorno desde `.env`
- Define un callback personalizado para medir latencia de respuesta del LLM
- Función para cargar flujos conversacionales desde archivo
- Función para instanciar y configurar el modelo LLM a utilizar
"""

import os
import time
from dotenv import load_dotenv
from langchain_core.callbacks import BaseCallbackHandler
from langchain_openai import ChatOpenAI
from langchain_litellm import ChatLiteLLM

load_dotenv()

class LatencyCallbackHandler(BaseCallbackHandler):
    """
    Callback para medir tiempos de respuesta del modelo LLM.

    Métricas:
        - TTFT (Time To First Token): Tiempo hasta recibir el primer token
        - TFS (Time To First Sentence): Tiempo hasta recibir la primera oración completa
    """

    def __init__(self):
        self.start_time = None
        self.first_token_time = None
        self.first_sentence_time = None
        self.buffer = ""

    def on_llm_start(self, *args, **kwargs):
        """Inicializa el contador de tiempo al iniciar el LLM."""
        self.start_time = time.time()
        self.first_token_time = None
        self.first_sentence_time = None
        self.buffer = ""

    def on_llm_new_token(self, token, *args, **kwargs):
        """
        Se ejecuta cada vez que el modelo envía un nuevo token.
        Calcula TTFT y TFS en tiempo real.
        """
        now = time.time()

        # Primer token
        if self.first_token_time is None:
            self.first_token_time = now - self.start_time
            print(f"\n⏱ TTFT: {self.first_token_time:.2f}s")

        self.buffer += token

        # Primera oración
        if self.first_sentence_time is None and self.buffer.strip().endswith((".", "?", "!")):
            self.first_sentence_time = now - self.start_time
            print(f"⏱ TFS: {self.first_sentence_time:.2f}s")

    def on_llm_end(self, *args, **kwargs):
        """Se ejecuta cuando el modelo termina de responder."""
        print("✅ Streaming completado\n")


def cargar_flujo(path="flujo.txt"):
    """
    Carga un flujo conversacional desde un archivo de texto.

    Args:
        path (str): Ruta del archivo de flujo.

    Returns:
        str: Contenido del archivo.
    """
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def get_model():
    """
    Configura e instancia el modelo de lenguaje.

    Returns:
        ChatLiteLLM: Objeto de modelo configurado para streaming y con medición de latencia.
    """
    def get_model():
    """
    Configura e instancia el modelo de lenguaje.

    Returns:
        ChatLiteLLM: Objeto de modelo configurado para streaming y con medición de latencia.
    """
    return ChatLiteLLM(
        model="openrouter/openai/gpt-oss-120b",
        temperature=0.3,
        openrouter_api_key=os.getenv("OPENROUTER_API_KEY"),
        streaming=True,
        callbacks=[LatencyCallbackHandler()],
        effort="low",
        exclude=True
    )
