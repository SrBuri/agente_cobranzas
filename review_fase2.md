# Evaluación Comparativa de Modelos LLM para el Agente

Este documento resume el desempeño de varios modelos LLM evaluados según:
- **TTFT (Time To First Token)**: tiempo en segundos hasta recibir el primer token.
- **TFS (Time For Sentence)**: tiempo promedio en segundos para completar una respuesta.
- **Fluidez y coherencia** en el seguimiento del flujo conversacional.
- **Uso de herramientas** (*tools*) cuando es necesario.

---

## Tabla de Comparación

| Modelo              | Pros                                                                                                      | Contras                                                                                         | TTFT promedio | TFS promedio | Observación final |
|---------------------|-----------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------|--------------|--------------|-------------------|
| **openai/gpt-4.1-mini** | - Muy buen tiempo de respuesta (1–2 s promedio).<br>- Sigue el flujo de la conversación de forma natural.<br>- Respuestas completas y educadas.<br>- No repite información innecesaria. | - Pausa larga ocasional (4.1 s).| ~1.7 s       | ~1.8 s       | Buen balance de rapidez y coherencia. |
| **openai/gpt-oss-120b** | - Muy coherente y natural.<br>- Uso correcto de énfasis y formato.<br>- Preguntas claras y ordenadas.<br>- Sin repeticiones innecesarias. | - Tiempo inicial más alto (precarga ~4.4 s).<br>- Mejorar un poco el flujo (que lo siga completo). | ~1.6 s       | ~1.9 s       | Excelente calidad de respuesta. |
| **z-ai/glm-4.5**     | - Mantiene estructura del flujo.<br>- Retoma contexto.<br>- Cortés. | - Repite bloques de información.<br>- Varias pausas largas (5+ s).<br>- Menos conciso. | ~2.3 s       | ~4.3 s       | Funciona pero requiere optimización de prompts para evitar redundancia y pausas largas. |
| **z-ai/glm-4.5-air** | - Buen manejo del flujo.<br>- Confirmaciones claras.<br>- Preguntas precisas. | - Pausas innecesarias ocasionales.| ~1.9 s       | ~2.9 s       | Buena calidad; ligeramente más lento. Necesita optimizacion |

---

## Conclusiones

- **Prioridad de pruebas:**
  - **openai/gpt-oss-120b** → Mayor coherencia y naturalidad, buen manejo de flujo.  

- **Backup rápido:**
  - **openai/gpt-4.1-mini** → Muy veloz y con buen seguimiento de flujo. 

- **Uso condicionado:**
  - **z-ai/glm-4.5** → Funcional, pero necesita optimización para reducir pausas largas y repeticiones.
  - **z-ai/glm-4.5-air** → Flujo sólido y claridad buenos, pero necesita optimización para reducir pausas largas y repeticiones.