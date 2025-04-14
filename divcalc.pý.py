def calcular_divisor_tension(Vin, Vout_deseado, tolerancia=0.05):
    resistencias = [
        100, 220, 330, 470, 560, 680, 820,
        1000, 2200, 3300, 4700, 5600, 6800, 8200,
        10000, 22000, 33000, 47000, 56000, 68000, 82000,
        100000, 220000, 330000, 470000, 560000, 680000, 820000,
        1000000
    ]
    
    soluciones = []

    for R1 in resistencias:
        for R2 in resistencias:
            Vout = Vin * R2 / (R1 + R2)
            error = abs(Vout - Vout_deseado) / Vout_deseado
            if error <= tolerancia:
                soluciones.append((R1, R2, Vout, error))

    if not soluciones:
        print("No se encontraron combinaciones dentro de la tolerancia.")
    else:
        print("Posibles combinaciones (R1, R2, Vout calculado, error):")
        for R1, R2, Vout, error in sorted(soluciones, key=lambda x: x[3]):
            print(f"R1: {R1} Ω, R2: {R2} Ω → Vout: {Vout:.2f} V (error: {error*100:.2f}%)")

# Ejemplo de uso
Vin = float(input("Ingrese la tensión de entrada (Vin) en voltios: "))
Vout_deseado = float(input("Ingrese la tensión de salida deseada (Vout) en voltios: "))
calcular_divisor_tension(Vin, Vout_deseado)
