import re

def extraer_secciones_del_texto(texto):
    # Este patrón busca números de lista seguidos por el título, y termina con el número de página después de un guion.
    patron = re.compile(r'(\d+)\.\s+(.+?)\s+-\s+(\d+)')
    matches = patron.findall(texto)
    
    secciones = []
    for match in matches:
        # match[0] es el número, match[1] es el título de la sección, y match[2] es el número de página
        secciones.append({"titulo": match[1].strip(), "pagina": f"Página {match[2].strip()}"})
    
    return secciones