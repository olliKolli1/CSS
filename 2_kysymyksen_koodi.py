#Vaikuttaako kunnan sukupuolijakauma äänestysaktiivisuuteen?

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

#Luetaan data
sukupuolijakauma = pd.read_csv('sukupuolijakauma.csv', sep=';', encoding='utf-8-sig')
aktiivisuus = pd.read_csv('äänestys_data.csv', sep=';', encoding='iso8859_10')
aanioikeutetut = pd.read_csv('väkiluku.csv', sep=';', encoding='iso8859_10')


aanestaneet = aktiivisuus[aktiivisuus['Tiedot'] == 'Äänestäneet'][['Alue', 'Äänestäneitä miehiä', 'Äänestäneitä naisia']]

# Yhdistetään äänioikeutetut ja aktkiivisuus
aktiivisuusOikeutetut = aanestaneet.merge(aanioikeutetut[['Alue', 'Äänioikeutetut']], on='Alue', how='left')

#Erotetaan kuntakoodi ja kunta omiksi sarakkeiksi.
aktiivisuusOikeutetut[["Koodi", "Kunta"]] = aktiivisuusOikeutetut["Alue"].str.extract(r'(\d+)\s+(.*)')

#Yhdistetään sukupuolijakauma ja akatiivisuus kunnittain.
sukupuoliJaAktiivisuus = aktiivisuusOikeutetut.merge(sukupuolijakauma[['Kunta', 'Yhteensä', 'Miehet', 'Naiset']], on='Kunta', how='left')

#Sukupuolijakauma = naiset% - miehet%
sukupuoliJaAktiivisuus["Sukupuolijakauma"] = ((sukupuoliJaAktiivisuus["Naiset"] / sukupuoliJaAktiivisuus["Yhteensä"] - sukupuoliJaAktiivisuus["Miehet"] / sukupuoliJaAktiivisuus["Yhteensä"])*100)
#Äänestysprosentti yhteensä
sukupuoliJaAktiivisuus["Äänestysprosentti"] = ((sukupuoliJaAktiivisuus["Äänestäneitä miehiä"] + sukupuoliJaAktiivisuus["Äänestäneitä naisia"]) / sukupuoliJaAktiivisuus["Äänioikeutetut"] * 100)
#Äänestysprosentti naiset%-miehet%
sukupuoliJaAktiivisuus["Äänestysprosentti_N-M"] = ((sukupuoliJaAktiivisuus["Äänestäneitä naisia"]) / (sukupuoliJaAktiivisuus["Äänioikeutetut"] * sukupuoliJaAktiivisuus["Naiset"] / sukupuoliJaAktiivisuus["Yhteensä"]) * 100) - ((sukupuoliJaAktiivisuus["Äänestäneitä miehiä"]) / (sukupuoliJaAktiivisuus["Äänioikeutetut"] * sukupuoliJaAktiivisuus["Miehet"] / sukupuoliJaAktiivisuus["Yhteensä"]) * 100)




#Korrelaatio
correlation = sukupuoliJaAktiivisuus["Sukupuolijakauma"].corr(sukupuoliJaAktiivisuus["Äänestysprosentti"])
print(f"Korrelaatio äänestysprosentin ja sukupuolijakauman välillä: {correlation:.3f}")

correlation2 = sukupuoliJaAktiivisuus["Sukupuolijakauma"].corr(sukupuoliJaAktiivisuus["Äänestysprosentti_N-M"])
print(f"Korrelaatio naisten ja miesten äänestysprosentin erotuksen ja sukupuolijakauman välillä: {correlation2:.3f}")

#Äänestysprosentti ja sukupuolijakauma kuvaaja
plt.figure(figsize=(10, 6))
plt.grid()
sns.regplot(x="Sukupuolijakauma", y="Äänestysprosentti", data=sukupuoliJaAktiivisuus, scatter=True, line_kws={"color":"red"})

#Lisää kunnan nimen datapisteelle
for idx, kunta in sukupuoliJaAktiivisuus.iterrows():
    plt.text(kunta["Sukupuolijakauma"], kunta["Äänestysprosentti"], kunta["Kunta"], fontsize=5, alpha=0.7)


plt.title('Gender distribution in relation to voter turnout')
plt.xlabel('Gender distribution (female% - male%)')
plt.ylabel('Voter turnout (%)')
plt.show()

#Naisten ja miesten äänestysprosenttien erotuksen ja sukupuolijakauman kuvaaja
plt.figure(figsize=(10, 6))
plt.grid()
sns.regplot(x="Sukupuolijakauma", y="Äänestysprosentti_N-M", data=sukupuoliJaAktiivisuus, scatter=True, line_kws={"color":"red"})

#Lisää kunnan nimen datapisteelle
for idx, kunta in sukupuoliJaAktiivisuus.iterrows():
    plt.text(kunta["Sukupuolijakauma"], kunta["Äänestysprosentti_N-M"], kunta["Kunta"], fontsize=5, alpha=0.7)

plt.title('Gender distribution in relation to difference in female and male voter turnout')
plt.xlabel('Gender distribution (female% - male%)')
plt.ylabel('Difference in voter turnout (female% - male%)')
plt.show()