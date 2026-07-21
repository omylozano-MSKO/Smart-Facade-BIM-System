# r: numpy, pandas, openpyxl
import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

import numpy as np
import pandas as pd
from abc import ABC, abstractmethod  # Importamos el módulo para Clases Abstractas

# ==========================================
# 1. CLASE ABSTRACTA (El Contrato Base de Obra)
# ==========================================
class ElementoEnvolvente(ABC):
    def __init__(self, id_panel, x, y):
        self.id = id_panel
        self.x = x
        self.y = y

    @abstractmethod
    def calcular_geometria_parametrica(self, distancia_atractor):
        """Obliga a cualquier clase hija a definir cómo se dibuja"""
        pass

    @abstractmethod
    def calcular_costo(self):
        """Obliga a calcular su propio presupuesto"""
        pass


# ==========================================
# 2. CLASE HIJA 1: Panel Perforado (Polimorfismo)
# ==========================================
class PanelPerforado(ElementoEnvolvente):
    def __init__(self, id_panel, x, y, ancho, alto, costo_m2):
        super().__init__(id_panel, x, y)
        self.ancho = ancho
        self.alto = alto
        self._costo_m2 = costo_m2  # Atributo protegido (Encapsulamiento básico)

    # Encapsulamiento con @property (Getter seguro para el costo)
    @property
    def costo_unitario(self):
        return self._costo_m2

    def calcular_area_bruta(self):
        return self.ancho * self.alto

    def calcular_geometria_parametrica(self, distancia_atractor):
        # Lógica de apertura por atractor (devuelve el radio del círculo)
        apertura = max(0.1, min(0.85, 1.0 / (distancia_atractor * 0.15 + 0.4)))
        return apertura * 0.9  # Radio escalado para Grasshopper

    def calcular_costo(self, area_perforacion):
        area_neta = self.calcular_area_bruta() - area_perforacion
        return area_neta * self.costo_unitario


# ==========================================
# 3. CLASE HIJA 2: Panel de Lamas / Ciega (Polimorfismo)
# ==========================================
class PanelLamasOpacas(ElementoEnvolvente):
    def __init__(self, id_panel, x, y, ancho, alto, costo_m2):
        super().__init__(id_panel, x, y)
        self.ancho = ancho
        self.alto = alto
        self._costo_m2 = costo_m2

    @property
    def costo_unitario(self):
        return self._costo_m2

    # Polimorfismo: Mismo nombre de método, pero lógica geométrica diferente (devuelve factor de escala Z)
    def calcular_geometria_parametrica(self, distancia_atractor):
        # Las lamas varían su altura de extrusión según la distancia al atractor
        altura_lama = max(0.5, min(3.5, 4.0 / (distancia_atractor * 0.1 + 0.5)))
        return altura_lama

    def calcular_costo(self):
        return (self.ancho * self.alto) * self.costo_unitario


# ==========================================
# 4. GENERACIÓN DE DATOS Y PROCESAMIENTO (NumPy & Pandas)
# ==========================================
num_x = 10
num_y = 6

x_vals = np.linspace(0, 20, num_x)
y_vals = np.linspace(0, 12, num_y)
xx, yy = np.meshgrid(x_vals, y_vals)

p_x = xx.flatten()
p_y = yy.flatten()

# Punto Atractor móvil en el espacio de la fachada
atractor_x, atractor_y = 10.0, 14.0
distancias = np.sqrt((p_x - atractor_x)**2 + (p_y - atractor_y)**2)

lista_datos = []
valores_geometricos = []
costos_totales = []
es_perforado = [] # NUEVA LISTA PARA EL FILTRO

for i in range(len(p_x)):
    if i % 2 == 0:
        panel = PanelPerforado(f"PERF-{i}", p_x[i], p_y[i], 2.0, 2.0, 140000)
        param_geo = panel.calcular_geometria_parametrica(distancias[i])
        area_perf = (2.0 * 2.0) * (param_geo / 0.9) * np.pi * 0.2
        costo = panel.calcular_costo(area_perf)
        es_perforado.append(True)  # <-- INDICAMOS QUE ES PERFORADO
    else:
        panel = PanelLamasOpacas(f"LAMA-{i}", p_x[i], p_y[i], 2.0, 2.0, 180000)
        param_geo = panel.calcular_geometria_parametrica(distancias[i])
        costo = panel.calcular_costo()
        es_perforado.append(False) # <-- INDICAMOS QUE ES LAMA

    valores_geometricos.append(param_geo)
    costos_totales.append(costo)
    
    lista_datos.append({
        "ID": panel.id,
        "Tipo": type(panel).__name__,
        "Costo": costo
    })

# Análisis con Pandas
df_obra = pd.DataFrame(lista_datos)
presupuesto_general = df_obra["Costo"].sum()

print(f"🏛️ REPORTE BIM AVANZADO (POO + SOLID):")
print(f"   Componentes totales gestionados: {len(df_obra)}")
print(f"   Presupuesto total de envolvente mixta: ${presupuesto_general:,.2f}")

# --- SALIDAS A GRASSHOPPER ---
a = p_x.tolist()
b = p_y.tolist()
c = valores_geometricos 
d = es_perforado # NUEVA SALIDA (El filtro para Grasshopper)

import os

# --- EXPORTACIÓN BIM A EXCEL ---
# Encontramos la ruta automática de tu Escritorio
ruta_escritorio = os.path.expanduser("~/Desktop/Presupuesto_Fachada_BIM.xlsx")

# Exportamos el DataFrame de Pandas a Excel (sin la columna de índice numérico)
df_obra.to_excel(ruta_escritorio, index=False)
print(f"✅ ¡Excel exportado exitosamente en el Escritorio!")
