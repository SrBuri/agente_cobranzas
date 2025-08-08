from agent import app

def main():
    print("📞 Llamando automáticamente al siguiente cliente aleatorio:\n")
    print("🟢 Iniciando sesión de cobranza con Daniela...\n")

    app.invoke({"messages": []}, {"recursion_limit": 100}, verbose=True)

if __name__ == "__main__":
    main()