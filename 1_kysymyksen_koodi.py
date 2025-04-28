import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

aktiivisuus = pd.read_csv('äänestys_data.csv', sep=';', encoding='iso8859_10')
ehdokkaat = pd.read_csv('Ehdokas_data.csv', sep=';', encoding='utf-8')
vakiluku = pd.read_csv('väkiluku.csv', sep=';', encoding='iso8859_10')
#print(aktiivisuus.head())
#print(ehdokkaat.head())
#print(vakiluku.head())

# Yhdistetään väkiluku aktiviisuusdataan Alue-kentän perusteella
aktiivisuus_väkiluku = aktiivisuus.merge(vakiluku[['Alue', 'Äänioikeutetut']], on='Alue', how='left')

# Yhdistetään ehdokkaat ja aktiivisuus-väkiluku-data
täydellinen_data = aktiivisuus_väkiluku.merge(ehdokkaat[['Alue', 'Yhteensä']], on='Alue', how='left')

# Lasketaan suhteutettu ehdokkaiden lukumäärä per asukas
täydellinen_data['suhteutettu_ehdokkaiden_lukumäärä'] = täydellinen_data['Yhteensä'] / täydellinen_data['Äänioikeutetut']

# Yhdistetään äänestysprosentti
äänestysprosentti = aktiivisuus[aktiivisuus['Tiedot'] == 'Äänestysprosentti'][['Alue', 'Äänestäneitä miehiä', 'Äänestäneitä naisia']]

# miesten ja naisten äänestysprosenttien keskiarvo
äänestysprosentti['Äänestysprosentti_keskiarvo'] = (äänestysprosentti['Äänestäneitä miehiä'] + äänestysprosentti['Äänestäneitä naisia']) / 2
täydellinen_data = täydellinen_data.merge(äänestysprosentti[['Alue', 'Äänestysprosentti_keskiarvo']], on='Alue', how='left')
print(täydellinen_data.head())

# plottaus ja korrelaatio
plt.figure(figsize=(10, 6))
sns.regplot(x='suhteutettu_ehdokkaiden_lukumäärä', y='Äänestysprosentti_keskiarvo', data=täydellinen_data, scatter=True, line_kws={"color":"red"})
plt.title('Suhteutettu ehdokkaiden määrä ja äänestysaktiivisuus')
plt.xlabel('Suhteutettu ehdokkaiden määrä per asukas')
plt.ylabel('Äänestysprosentti')
plt.show()

correlation = täydellinen_data['suhteutettu_ehdokkaiden_lukumäärä'].corr(täydellinen_data['Äänestysprosentti_keskiarvo'])
print(f"Korrelaatio suhteutetun ehdokkaiden määrän ja äänestysprosentin välillä: {correlation:.3f}")