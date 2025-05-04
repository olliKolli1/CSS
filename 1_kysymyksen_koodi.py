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
#print(täydellinen_data.head())

# plottaus ja korrelaatio
plt.figure(figsize=(10, 6))
sns.regplot(x='suhteutettu_ehdokkaiden_lukumäärä', y='Äänestysprosentti_keskiarvo', data=täydellinen_data, scatter=True, line_kws={"color":"red"})
plt.title('Number of candidates per resident and voter turnout')
plt.xlabel('Number of candidates per resident')
plt.ylabel('Voter turnout percentage (%)')
plt.show()

correlation = täydellinen_data['suhteutettu_ehdokkaiden_lukumäärä'].corr(täydellinen_data['Äänestysprosentti_keskiarvo'])
print(f"Korrelaatio suhteutetun ehdokkaiden määrän ja äänestysprosentin välillä: {correlation:.3f}")

# paras äänestysprosentti
best_voter_turnout_value = täydellinen_data['Äänestysprosentti_keskiarvo'].max()

# Missä paras äänestys prosentti on
best_turnout_alueet_data = täydellinen_data[täydellinen_data['Äänestysprosentti_keskiarvo'] == best_voter_turnout_value]

# Pelkkä paikka (voi olla monta samaa)
best_alueet = best_turnout_alueet_data['Alue'].tolist()

print(f"\nKorkein äänestysprosentti: {best_voter_turnout_value:.3f}%") # Lisätty %-merkki selkeydeksi

col_description = "per äänioikeutettu" # Description reflecting the calculation

if len(best_alueet) == 1:

    alue_name = best_alueet[0]
    relative_candidates_value = best_turnout_alueet_data.iloc[0]['suhteutettu_ehdokkaiden_lukumäärä']

    print(f"Alue, jolla korkein äänestysprosentti: {alue_name}")
    print(f" -> Suhteutettu ehdokkaiden määrä ({"per äänioikeutettu"}) tällä alueella: {relative_candidates_value:.4f}")
else:
    print(f"Alueet, joilla korkein äänestysprosentti (tasapeli): {', '.join(best_alueet)}")
    print(" -> Vastaavat suhteutetut ehdokkaiden määrät per äänioikeutettu")
    for index, row in best_turnout_alueet_data.iterrows():
        print(f"    - {row['Alue']}: {row['suhteutettu_ehdokkaiden_lukumäärä']:.4f}")