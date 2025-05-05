import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from IPython.display import display

ehdokkaat = pd.read_csv('Ehdokas_data.csv', sep=';', encoding='utf_8')
ehdokkaat = ehdokkaat.drop(['Tiedot', 'Vuosi', 'Puolue'], axis=1)
yleinen = pd.read_csv('sukupuolijakauma.csv', sep=';', encoding='utf_8')
yleinen = yleinen.drop('Ikä', axis=1)

#lasketaan prosentit
yleinen["miesten_prosentti"] = (yleinen['Miehet'] / yleinen['Yhteensä']) * 100
yleinen["naisten_prosentti"] = (yleinen['Naiset'] / yleinen['Yhteensä']) * 100

ehdokkaat["miesten_prosentti"] = (ehdokkaat['Miehet'] / ehdokkaat['Yhteensä']) * 100
ehdokkaat["naisten_prosentti"] = (ehdokkaat['Naiset'] / ehdokkaat['Yhteensä']) * 100

print("Yleinen")
display(yleinen)
print("Ehdokkaat")
display(ehdokkaat)
