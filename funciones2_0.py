import random

# Constantes
puntos_iniciales = 30
max_vida = 150

# Clases de personajes con vida predeterminada
clases = {
    1: ("Novato", 120),  # Más vida
    2: ("Superviviente", 80),  # vida media
    3: ("Soy Leyenda", 50)   # Menos vida
}

# Armas y sus puntos
armas = {
    1: ("pistola", 0), # basico
    2: ("subfusible", 30), # intermedio
    3: ("escopeta", 50), # avanzado
    4: ("ametralladora", 100) # mayor
}

# Áreas de impacto con sus puntos para los jugadores
puntos_impacto = {
    "cabeza": 100,
    "pecho": 50,
    "piernas": 30
}

# Áreas de impacto y daño para ataques del zombie
ataques = {
    "mordisco": 30,
    "arañazo": 20,
    "golpe": 15
}

# Función para obtener un número entero dentro de un rango
def obtener_numero(mensaje, min_val, max_val):
    while True:
        try:
            valor = int(input(mensaje))
            #comprueba si el valor esta dentro del rango permitido.
            if min_val <= valor <= max_val:
                return valor
            else:
                print(f"Por favor, ingresa un número entre {min_val} y {max_val}.")
            #comprueba si no es un numero entero
        except ValueError:
            print("ERROR. Por favor ingresa un número.")

# Función para elegir clase del personaje
def elegir_clase_personaje():
    print("\nElige la dificultad de tu personaje:")
    print("1: Novato (Vida: 150)")
    print("2: Superviviente (Vida: 80)")
    print("3: Soy Leyenda (Vida: 50)")
    while True:
        clase_opcion = obtener_numero("Ingresa 1 para Novato , 2 para Superviviente o 3 para Soy Leyenda : ", 1, 3)
        if clase_opcion in clases:
            clase, vida = clases[clase_opcion]
            return clase, vida

# Función para configurar al personaje
def configurar_personaje():
    print("🧟‍♂️💀 Configuración de Superviviente Iniciada 💀🧟‍♂️")
    nombre = input("Nombre del personaje: ")
    
    # Elegir clase y vida predeterminada
    clase, vida = elegir_clase_personaje()
    
    # Mostrar las armas disponibles y su costo
    print(f"\nElige un arma: tienes {puntos_iniciales} puntos.")
    for num, (arma, costo) in armas.items():
        print(f"{num}: {arma.capitalize()} (Costo en puntos: {costo})")

    # Obtener opción de arma y verificar si el jugador tiene suficientes puntos
    while True:
        arma_opcion = obtener_numero("Ingresa el número del arma: ", 1, 4)
        arma, costo_arma = armas[arma_opcion]
        
        # Verificar si el jugador tiene puntos suficientes para comprar el arma
        if puntos_iniciales >= costo_arma:
            puntos = puntos_iniciales - costo_arma
            return {
                "nombre": nombre,
                "clase": clase,
                "vida": vida,
                "puntos": puntos,
                "arma": arma
            }
        else:
            print("No tienes suficientes puntos para esta arma. Elige otra.")


# Función de compra de objetos (arma o vendas)
def comprar(personaje: dict[str, int | str]) -> None:
    print("\n¿Qué deseas comprar?")
    print("1: Comprar otra arma")
    print("2: Comprar vendas ")
    print("3: No comprar nada")

    opcion = obtener_numero("Ingresa 1 para comprar arma, 2 para comprar vendas o 3 para no comprar: ", 1, 3)

    if opcion == 1:
        print(f"\nElige un arma: tienes {personaje["puntos"]} puntos:")

        for num, (arma, puntos) in armas:
            print(f"{num}: {arma.capitalize()} (Costo en puntos: {puntos})")
        
        arma_opcion = obtener_numero("Ingresa el número del arma: ", 1, len(armas))
        arma, costo_arma = armas[arma_opcion]
        
        if personaje['puntos'] >= costo_arma:
            personaje['puntos'] -= costo_arma
            personaje['arma'] = arma  # Equipar nueva arma
            print(f"\nHas comprado la {arma} y ahora tienes {personaje['puntos']} puntos restantes.")
        else:
            print("\nNo tienes suficientes puntos para comprar esta arma.")

    elif opcion == 2:
        print(f"\nElige la cantidad de curación que deseas, tienes: {personaje['vida']} vida")
        print("1: 10 puntos de vida (Costo: 20 puntos)")
        print("2: 20 puntos de vida (Costo: 40 puntos)")
        print("3: 30 puntos de vida (Costo: 60 puntos)")

        curacion_opcion = obtener_numero("Ingresa el número de la cantidad de curación: ", 1, 3)
        curacion_valores = {1: (10, 20), 2: (20, 40), 3: (30, 60)}
        curacion, costo_vendas = curacion_valores[curacion_opcion]

        if personaje['puntos'] >= costo_vendas:
            personaje['vida'] += curacion
            if personaje['vida'] > max_vida:
                personaje['vida'] = max_vida  # No exceder la vida máxima
            personaje['puntos'] -= costo_vendas
            print(f"\nHas comprado vendas. Tu vida se ha incrementado en {curacion} puntos.")
            print(f"Ahora tienes {personaje['vida']} de vida y {personaje['puntos']} puntos restantes.")
        else:
            print("\nNo tienes suficientes puntos para comprar estas vendas.")

# Función de combate para un personaje
def combate(personaje: dict[str, int | str]) -> None:
    impacto = random.choice(list(puntos_impacto.keys()))
    puntos_ganados = puntos_impacto[impacto]
    personaje['puntos'] += puntos_ganados
    
    print(f"\n{personaje['nombre']} dispara con {personaje['arma']} y hace un disparo en el/la {impacto} del zombie.")
    print(f"Ganas {puntos_ganados} puntos.")

# Función para ataque del zombie
def ataque_zombie(personaje: dict[str, int | str]) -> None:
    ataque = random.choice(list(ataques.keys()))
    danio = ataques[ataque]
    personaje['vida'] -= danio

    print(f"¡El zombie ataca a {personaje['nombre']} con un {ataque} y causa {danio} de daño!")
    if personaje['vida'] <= 0:
        personaje['vida'] = 0  # Asegurarse de que la vida no sea negativa
        print(f"{personaje['nombre']} ha sido derrotado por el zombie.")

# Función para mostrar el historial de personajes
def mostrar_historial(historial_personajes: dict[str, int | str]) -> None:
    print("\nHistorial de los jugadores:")
    for personaje in historial_personajes:
        print(f"Nombre: {personaje['nombre']}, Clase: {personaje['clase']}, Vida: {personaje['vida']}, Arma: {personaje['arma']}, Puntos Finales: {personaje['puntos']}")

# Guardamos en un archivo el historial de jugadores 
def guardar_historial(historial: list[dict[str, int | str]]) -> None:
    with open("historial_juego.txt", "a") as file:
        for personaje in historial:
            file.write(f"{personaje['nombre']}, {personaje['clase']}, Vida: {personaje['vida']}, Arma: {personaje['arma']}, Puntos finales: {personaje['puntos']}, zombies eliminados: {personaje['zombies_eliminados']}\n")
    print("\nHistorial guardado en 'historial_juego.txt'.")

def jugar():
    print("¡Bienvenido al juego de combate contra zombies!")
    historial_personajes = []
    seguir_jugando = True
    
    while seguir_jugando:
        # Configurar un nuevo personaje cada vez
        personaje = configurar_personaje()
        personaje['zombies_eliminados'] = 0  # Contador de zombies eliminados
        historial_personajes.append(personaje) # para que no se transcriba eljugador 
        while True:
            print(f"\nTurno de {personaje['nombre']} - Clase: {personaje['clase']} - Vida: {personaje['vida']} - Puntos: {personaje['puntos']}")
            
            # Realizar el turno de combate
            combate(personaje)
            personaje['zombies_eliminados'] += 1  # Incrementar zombies eliminados
            
            # Zombie ataca al personaje
            ataque_zombie(personaje)
            
            # Verificar si el personaje ha sido derrotado
            if personaje['vida'] <= 0:
                print(f"\n{personaje['nombre']} ha sido derrotado. Fin del juego.")
                print("Historial del juego:")
                print(f"Nombre del personaje: {personaje['nombre']}")
                print(f"Zombies eliminados: {personaje['zombies_eliminados']}")
                print(f"Puntos finales: {personaje['puntos']}")
                
                # Preguntar si el jugador quiere continuar con un nuevo personaje
                seguir_jugando = input("¿Quieres seguir jugando? (si/no): ").strip().lower() == "si"
                if not seguir_jugando:
                    guardar_historial(historial_personajes)
                    print("¡Gracias por jugar!")
                break
            
            # Opciones de acción mientras el personaje sigue con vida
            print("\n¿Qué deseas hacer ahora?")
            print("1: Continuar jugando con el mismo personaje")
            print("2: Ver Historial")
            print("3: Comprar (arma o vendas)")
            print("4: Salir del juego")
            
            opcion = int(input("Ingresa el número de la opción: "))
            
            if opcion == 1:
                continue  # Continuar con el mismo personaje
            elif opcion == 2:
                mostrar_historial(historial_personajes)
            elif opcion == 3:
                comprar(personaje)  # Función de compra opcional
            elif opcion == 4:
                guardar_historial(historial_personajes)
                print("¡Gracias por jugar!")
                seguir_jugando = False
                break
