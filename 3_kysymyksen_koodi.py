import pandas as pd
from IPython.display import display
import string

ehdokkaat = pd.read_csv('Ehdokas_data.csv', sep=';', encoding='utf_8')
ehdokkaat = ehdokkaat.drop(['Tiedot', 'Vuosi', 'Puolue'], axis=1)
yleinen = pd.read_csv('sukupuolijakauma.csv', sep=';', encoding='utf_8')
yleinen = yleinen.drop('Ikä', axis=1)
yleinen = yleinen.rename(columns={'Kunta': 'Alue'})

#lasketaan prosentit
yleinen["y_miesten_prosentti"] = (yleinen['Miehet'] / yleinen['Yhteensä']) * 100
yleinen["y_naisten_prosentti"] = (yleinen['Naiset'] / yleinen['Yhteensä']) * 100


ehdokkaat["e_miesten_prosentti"] = (ehdokkaat['Miehet'] / ehdokkaat['Yhteensä']) * 100
ehdokkaat["e_naisten_prosentti"] = (ehdokkaat['Naiset'] / ehdokkaat['Yhteensä']) * 100

#Muokataan taulukot yhteen sopiviksi ja poistetaan numeeriset määrät
ehdokkaat['Alue'] = ehdokkaat['Alue'].str.lstrip(string.digits)
ehdokkaat['Alue'] = ehdokkaat['Alue'].str.strip()
ehdokkaat = ehdokkaat.drop(['Miehet', 'Naiset', 'Yhteensä'], axis=1)
yleinen = yleinen.drop(['Miehet', 'Naiset', 'Yhteensä'], axis=1)

#Yhdistetään taulukot
yhdistetyt = yleinen.merge(ehdokkaat, on='Alue', how='left')

#Uusi taulukko prosenttien erotuksille
erotus = yhdistetyt.copy()
erotus['Miesten_prosentuaalinen_muutos'] = erotus['e_miesten_prosentti'] - erotus['y_miesten_prosentti']
erotus['Naisten_prosentuaalinen_muutos'] = erotus['e_naisten_prosentti'] - erotus['y_naisten_prosentti']
erotus = erotus.drop(['e_miesten_prosentti', 'e_naisten_prosentti', 'y_miesten_prosentti', 'y_naisten_prosentti'], axis=1)

#Filtteröidään
miehiä_enemmän = erotus[erotus['Miesten_prosentuaalinen_muutos'] > 20]
naisia_enemmän = erotus[erotus['Naisten_prosentuaalinen_muutos'] > 0]
alle_yhden = erotus[abs(erotus['Miesten_prosentuaalinen_muutos']) < 1]


print("Yleineny")
display(yleinen)

print("Ehdokkaat")
display(ehdokkaat)

print("yhdistetyt")
display(yhdistetyt)

print("Erotus:")
display(erotus)

print("Miesten muutos yli 30:")
display(miehiä_enemmän)

print("Enemmän naisehdokkaita")
display(naisia_enemmän)

print("Alle prosentin muutos:")
display(alle_yhden)

print("Dataa erotuksesta:")
display(erotus.agg({'Miesten_prosentuaalinen_muutos': ["min", "max", "median", "mean"], 'Naisten_prosentuaalinen_muutos': ["min", "max", "median", "mean"]}))

print("Dataa prosenteista:")
display(yhdistetyt.agg({'e_miesten_prosentti': ["min", "max", "median", "mean"], 'e_naisten_prosentti': ["min", "max", "median", "mean"], 'y_miesten_prosentti': ["min", "max", "median", "mean"], 'y_naisten_prosentti': ["min", "max", "median", "mean"]}))

