import locale
from fuzzywuzzy import process
from spellchecker import SpellChecker

# Establecer la configuración regional para pesos colombianos (COP)
locale.setlocale(locale.LC_ALL, 'es_CO.UTF-8')

# Menú del restaurante
menu = {
    "pizza": 8000,
    "hamburguesa": 18000,
    "ensalada": 12000,
    "pasta": 22000,
    "sushi": 20000,
}

spell = SpellChecker()

# Función para procesar la orden con búsqueda fuzzy y corrección ortográfica
def procesar_orden_inteligente(text, menu):
    palabras = text.lower().split()
    orden = {}

    for palabra in palabras:
        # Excepción especial para la palabra 'hamburguesa'
        if palabra == 'hamburguesa':
            correccion = 'hamburguesa'
        else:
            # Corrección ortográfica
            correccion = spell.correction(palabra)

            # Verificar si la corrección ortográfica es diferente a la palabra original y no es None
            if correccion is not None and correccion != palabra:
                print(f"Advertencia: La palabra '{palabra}' podría estar mal escrita. ¿Quisiste decir '{correccion}'?")
        
        # Verificar si la palabra corregida está en el menú
        if correccion in menu:
            item = correccion
        else:
            # Verificar si la corrección ortográfica es válida antes de la búsqueda fuzzy
            if correccion is not None and correccion.lower() in menu:
                item = correccion.lower()
            else:
                print(f"Advertencia: No se pudo corregir la palabra '{palabra}'.")
                return None, None  # Salir de la función y volver a solicitar la orden

        if item in orden:
            orden[item] += 1
        else:
            orden[item] = 1

    if not orden:
        return "Lo siento, no entendí tu pedido. Por favor, menciona un plato del menú.", None

    total = sum(menu[item] * cantidad for item, cantidad in orden.items())
    return orden, total

# Bucle principal para permitir atender a múltiples clientes
while True:
    # Mensaje de bienvenida
    print("Bienvenido al chatbot de restaurante.")

    # Inicializar el total acumulado
    total_acumulado = 0

    # Bucle para permitir pedidos de un cliente
    while True:
        orden_usuario = input("¿Qué te gustaría pedir?: ")

        # Procesar la orden usando la función
        orden, subtotal = procesar_orden_inteligente(orden_usuario, menu)

        while orden is None:
            orden_usuario = input("Por favor, menciona un plato del menú: ")
            orden, subtotal = procesar_orden_inteligente(orden_usuario, menu)

        print(f"Has ordenado:")
        for item, cantidad in orden.items():
            print(f"{cantidad} {item}")

        # Mostrar el subtotal en formato COP
        subtotal_cop = locale.currency(subtotal, grouping=True)
        print(f"Subtotal de esta orden: {subtotal_cop}")

        # Actualizar el total acumulado
        total_acumulado += subtotal

        # Mostrar el total acumulado en formato COP
        total_acumulado_cop = locale.currency(total_acumulado, grouping=True)
        print(f"Total acumulado hasta ahora: {total_acumulado_cop}")

        respuesta_continuar = input("¿Deseas agregar algo más? (sí/no): ").lower()
        while respuesta_continuar not in ['sí', 'si', 'SI', 'Si', 'Sí', 'no', 'NO', 'No']:
            print("Opción no válida. Por favor, responde con 'sí' o 'no'.")
            respuesta_continuar = input("¿Deseas agregar algo más? (sí/no): ").lower()

        if respuesta_continuar == 'no':
            # Cobrar y verificar el pago
            print(f"El total de tu orden es: {total_acumulado_cop}")
            monto_pago = float(input("Por favor, ingresa el monto con el que vas a pagar: $"))

            while monto_pago < total_acumulado:
                print("El monto ingresado no es suficiente para cubrir el total de la orden.")
                monto_pago = float(input("Por favor, ingresa un monto suficiente para pagar: $"))

            vuelto = monto_pago - total_acumulado

            # Mostrar el cambio en formato COP
            vuelto_cop = locale.currency(vuelto, grouping=True)
            print(f"Gracias por tu pago. Tu cambio es: {vuelto_cop}")
            break  # Salir del bucle de atención al cliente actual

    respuesta_nuevo_cliente = input("¿Deseas atender a otro cliente? (sí/no): ").lower()
    if respuesta_nuevo_cliente not in ['sí', 'si', 'SI', 'Si']:
        print("Gracias por atender a los clientes. Hasta luego.")    
        break  # Salir del bucle principal y finalizar el programa

