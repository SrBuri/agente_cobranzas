from agent import responder, cerrar
from agent import obtener_cliente

def main():
    cliente = obtener_cliente()
    print("📞 Llamando automáticamente al siguiente cliente aleatorio:\n")
    print(f"👤 Nombre: {cliente['nombre']}")
    print("🟢 Iniciando sesión de cobranza con Daniela...\n")

    while True:
        user_input = input("👤 Cliente: ")
        if user_input.lower() in ["salir", "exit"]:
            break
        
        respuesta = responder(user_input)
        print(f"\n🤖 Daniela: {respuesta}\n")
        if cerrar(respuesta):
            print("La conversacion ha finalizado")
            break

if __name__ == "__main__":
    main()