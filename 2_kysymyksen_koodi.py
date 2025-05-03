#Vaikuttaako kunnan sukupuolijakauma äänestysaktiivisuuteen?

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

#Luetaan data
sukupuolijakauma = pd.read_csv('sukupuolijakauma.csv', sep=';', encoding='utf-8-sig')
aktiivisuus = pd.read_csv('äänestys_data.csv', sep=';', encoding='iso8859_10')

print(sukupuolijakauma.head())
print(aktiivisuus.head())

# Yhdistetään äänestysprosentti
aanestysprosentti = aktiivisuus[aktiivisuus['Tiedot'] == 'Äänestysprosentti'][['Alue', 'Äänestäneitä miehiä', 'Äänestäneitä naisia']]

#Erotetaan kuntakoodi ja kunta omiksi sarakkeiksi.
aanestysprosentti[["Koodi", "Kunta"]] = aanestysprosentti["Alue"].str.extract(r'(\d+)\s+(.*)')

#Yhdistetään sukupuolijakauma ja ääniakatiivisuus kunnittain.
sukupuoliJaAktiivisuus = aanestysprosentti.merge(sukupuolijakauma[['Kunta', 'Yhteensä', 'Miehet', 'Naiset']], on='Kunta', how='left')

#Sukupuolijakauma = naiset% - miehet%
sukupuoliJaAktiivisuus["Sukupuolijakauma"] = ((sukupuoliJaAktiivisuus["Naiset"] / sukupuoliJaAktiivisuus["Yhteensä"] - sukupuoliJaAktiivisuus["Miehet"] / sukupuoliJaAktiivisuus["Yhteensä"])*100)

#Äänestysprosentti = (äänestäneet miehet + äänestäneet naiset) / äänioikeutetut * 100
sukupuoliJaAktiivisuus["Äänestysprosentti"] = ((sukupuoliJaAktiivisuus["Äänestäneitä miehiä"] + sukupuoliJaAktiivisuus["Äänestäneitä naisia"]) / 2)

#Korrelaatio
correlation = sukupuoliJaAktiivisuus["Sukupuolijakauma"].corr(sukupuoliJaAktiivisuus["Äänestysprosentti"])
print(f"Korrelaatio äänestysprosentin ja sukupuolijakauman välillä: {correlation:.3f}")

#Kuvaaja
plt.figure(figsize=(10, 6))
sns.regplot(x="Sukupuolijakauma", y="Äänestysprosentti", data=sukupuoliJaAktiivisuus, scatter=True, line_kws={"color":"red"})
plt.title('Sukupuolijakauma suhteessa äänestysaktiivisuuteen')
plt.xlabel('Sukupuolijakauma (naiset% - miehet%)')
plt.ylabel('Äänestysprosentti (%)')
plt.show()