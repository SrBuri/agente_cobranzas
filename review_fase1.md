# Evaluación de Modelos LLM para el Agente

| Modelo                                         | Observaciones                                                                                  | Velocidad   | Uso de Tools | Seguimiento de Flujo | Recomendación            |
|-----------------------------------------------|------------------------------------------------------------------------------------------------|-------------|--------------|----------------------|--------------------------|
| openai/gpt-4.1-mini                            |  Sigue el flujo; buen tiempo de respuesta           | Rápido      | Sí      | Sí                   | Seguir probando  |
| openai/gpt-oss-120b                            | Funcionó perfecto                                                                              | Rápido       | Sí           | Sí                   | **Seguir probando**      |
| google/gemini-2.5-flash-lite                   | No sigue bien el flujo; tiempos de respuesta buenos                                            | Rápido      | Parcial      | No                   | Descartar                |
| openai/gpt-5-nano                              | Muy lento; no sigue bien el flujo                                                               | Lento       | Parcial      | No                   | Descartar                |
| z-ai/glm-4.5                                   | Funciona medianamente bien (++); un poco lento; no decir que segmento pertenece                | Medio-Lento | Sí           | Parcial              | Seguir probando          |
| z-ai/glm-4.5-air                               | Funciona medianamente bien (++++) ; un poco lento; debe finalizar bien                         | Medio-Lento | Sí           | Parcial              | **Seguir probando**      |
| z-ai/glm-4-32b                                 | No funciona bien; no sigue el flujo; no utiliza herramientas                                   | Lento       | No           | No                   | Descartar                |
| qwen/qwen3-30b-a3b-instruct-2507               | No soporta *tools*                                                                             | Medio       | No           | -                    | Descartar                |
| qwen/qwen3-235b-a22b-2507                      | Lento en ocasiones; no sigue del todo bien el flujo                                            | Medio-Lento | Sí           | Parcial              | Descartar  |
| google/gemini-2.5-flash-lite-preview-06-17     | No sigue el flujo; rápido pero "tonto"                                                         | Rápido      | Parcial      | No                   | Descartar                |
| openai/gpt-4.1-nano                            | No sigue el flujo; "tonto"                                                                      | Rápido      | Parcial      | No                   | Descartar                |
| qwen/qwen-plus                                 | Gentil; un poco lento; no sigue el flujo; hay que recordarle cosas                             | Medio-Lento | Parcial      | No                   | Descartar                |
| qwen/qwen-turbo                                | No sigue el flujo; no utiliza herramientas                                                     | Medio       | No           | No                   | Descartar                |

## Leyenda
- **Velocidad:** estimación basada en pruebas (Rápido, Medio, Lento).
- **Uso de Tools:** capacidad de invocar herramientas correctamente (Sí, Parcial, No).
- **Seguimiento de Flujo:** capacidad de seguir el flujo conversacional esperado.
- **Recomendación:**  
  - **Seguir probando** → Alto potencial, vale la pena más pruebas.  
  - Mantener en observación → Promedio, requiere ajustes.  
  - Descartar → Bajo rendimiento o incompatibilidad.
