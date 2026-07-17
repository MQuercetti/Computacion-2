"""analizadores — un proceso por cada dimensión del snapshot.

Cada módulo exporta una función `analizar(pids, snapshot, intervalos, verbose)`
que es el entry point del Process. El loop interno duerme según el intervalo
configurado para su slot y reescribe el slot correspondiente del snapshot.

Ver README del TP y consigna.md para el detalle de cada dimensión.
"""
