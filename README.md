# 🏛️ Smart Facade BIM System | Computational Architecture

Este proyecto es un flujo de trabajo **BIM y Diseño Paramétrico Generativo** desarrollado íntegramente en el motor de **Python 3 dentro de Rhinoceros 8 / Grasshopper**.

Demuestra la integración entre el diseño geométrico, la **Programación Orientada a Objetos (POO)** y el análisis de datos puros.

## ⚙️ Tecnologías y Conceptos Aplicados
* **Rhinoceros 8 & Grasshopper:** Modelado y visualización paramétrica en tiempo real.
* **Python 3:** Motor de cálculo y lógica central.
* **OOP (Programación Orientada a Objetos):** Implementación de **Clases Abstractas (`ABC`)**, Encapsulamiento (`@property`) y Polimorfismo.
* **Principios SOLID:** Código estructurado bajo el principio de Responsabilidad Única y Abierto/Cerrado.
* **Data Analysis (Pandas & NumPy):** Procesamiento de matrices matemáticas, estimación de presupuestos y exportación automática a `.xlsx` mediante `openpyxl`.

## 🚀 Funcionalidades del Script
1. **Control por Atractor:** La geometría de la fachada (radios de perforación y altura de extrusión) responde matemáticamente a la distancia de un punto atractor (Ej. asoleamiento o factor humano).
2. **Sistema Mixto (Polimorfismo):** El algoritmo intercala dinámicamente clases de `PanelPerforado` y `PanelLamasOpacas`, aplicando a cada uno su propia regla geométrica y económica.
3. **Cálculo de Presupuesto en Tiempo Real:** El sistema computa el área bruta, descuenta vacíos generados paramétricamente, calcula el costo total y exporta un reporte estructurado a Microsoft Excel.

---
*Desarrollado por Omar - Arquitecto Computacional / BIM Developer*
