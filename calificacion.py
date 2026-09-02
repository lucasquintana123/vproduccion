def calcular_calificacion(row):

    categoria = str(row['Categoria'])  
    peso_kilos_netos = row['Peso_kilos_netos']
    var_fob_dolar = row['Valor_FOB_USD']

    rangos_calificaciones = {
        'Chocolates': {
            'peso': {(0, 894): 0,
                (895, float('inf')): 1},
            'fob': { (0, 3782): 0,
                (3783, float('inf')): 1}
        },
        'Cacao en polvo': {
            'peso': {(0, 1641): 0,
                (1642, float('inf')): 1},
            'fob': {(0, 6345): 0,
                (6346, float('inf')): 1}
        },
        'Cacao crudo': {
            'peso': {(0, 25000): 0,
                (25001, float('inf')): 1},
            'fob': {(0, 75684): 0,
                (75685, float('inf')): 1}
        },
        'Manteca de cacao': {
            'peso': {(0, 12000): 0,
                (12001, float('inf')): 1},
            'fob': {(0, 74421): 0,
                (74422, float('inf')): 1}
        },
        'pasta de cacao': {
            'peso': { (0, 9986): 0,
                (9987, float('inf')): 1},
            'fob': {(0, 40382): 0,
                (40383, float('inf')): 1}
        },
        'Cacao tostado': {
            'peso': {(0, 500): 0,
                (501, float('inf')): 1},
            'fob': {(0, 4662): 0,
                (4663, float('inf')): 1}
        },
        'otras preparaciones': {
            'peso': {(0, 5740): 0,
                (5741, float('inf')): 1},
            'fob': { (0, 27170): 0,
                (27171, float('inf')): 1}
        },
        'Cascara de cacao': {
            'peso': {(0, 12600): 0,
                (12601, float('inf')): 1},
            'fob': {(0, 6093): 0,
                (6094, float('inf')): 1}
        }
    }

    if categoria in rangos_calificaciones:

        calificacion_peso = None
        calificacion_fob = None

        for rango, calificacion in rangos_calificaciones[categoria]['peso'].items():
            if rango[0] <= peso_kilos_netos <= rango[1]:
                calificacion_peso = calificacion
                break

        for rango, calificacion in rangos_calificaciones[categoria]['fob'].items():
            if rango[0] <= var_fob_dolar <= rango[1]:
                calificacion_fob = calificacion
                break

        if calificacion_peso is None or calificacion_fob is None:
            return 0

        promedio = (calificacion_peso + calificacion_fob) / 2

        return 1 if promedio >= 0.5 else 0

    return 0
