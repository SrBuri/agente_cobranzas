# Agente de Cobranza - Daniela 🤖

Agente conversacional para gestiones de cobro automatizadas usando LangChain, OpenAI y Supabase.

## Características
- Sigue flujo de cobranzas (cobro total, descuentos, convenios)
- Usa herramientas conectadas a Supabase
- Registra compromisos de pago y objeciones
- Personaliza mensajes según el cliente

## Estructura
- `main.py`: entrada principal
- `agente.py`: lógica del agente
- `tools.py`: herramientas (tools LangChain)
- `supabase_client.py`: conexión con Supabase
- `flujo_daniela.md`: prompt y reglas del flujo
