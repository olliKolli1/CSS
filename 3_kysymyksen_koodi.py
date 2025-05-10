import pandas as pd
from IPython.display import display
import string
import matplotlib.pyplot as plt
import seaborn as sns

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
erotus['Change in percentages of males'] = erotus['e_miesten_prosentti'] - erotus['y_miesten_prosentti']
erotus['Change in percentages of females'] = erotus['e_naisten_prosentti'] - erotus['y_naisten_prosentti']
erotus = erotus.drop(['e_miesten_prosentti', 'e_naisten_prosentti', 'y_miesten_prosentti', 'y_naisten_prosentti'], axis=1)
erotus = erotus.rename(columns={'Alue': 'Municipality'})

#korrelaatio
korrelaatio = yleinen["y_miesten_prosentti"].corr(ehdokkaat["e_miesten_prosentti"])
print("Correlation between the male voters and candidates:", korrelaatio)

#Filtteröidään
miehiä_enemmän = erotus[erotus['Change in percentages of males'] > 20]
naisia_enemmän = erotus[erotus['Change in percentages of females'] > 0]
alle_yhden = erotus[abs(erotus['Change in percentages of males']) < 1]


print("Yleinen")
display(yleinen)

print("Ehdokkaat")
display(ehdokkaat)

print("yhdistetyt")
display(yhdistetyt)

print("Erotus:")
display(erotus)

print("Change in the share of males over 20 percentage units:\n")
display(miehiä_enemmän)

print("The bigger share of female candidates than female voters:\n")
display(naisia_enemmän)

print("Change of under a percent:\n")
display(alle_yhden)

print("Common figures from the changes of shares in both males and females:\n")
display(erotus.agg({'Change in percentages of males': ["min", "max", "median", "mean"], 'Change in percentages of females': ["min", "max", "median", "mean"]}))

print("Dataa prosenteista:")
display(yhdistetyt.agg({'e_miesten_prosentti': ["min", "max", "median", "mean"], 'e_naisten_prosentti': ["min", "max", "median", "mean"], 'y_miesten_prosentti': ["min", "max", "median", "mean"], 'y_naisten_prosentti': ["min", "max", "median", "mean"]}))

#plottausta
#pelkkä_miesten_muutos=erotus.drop('Naisten_prosentuaalinen_muutos', axis=1)
#plt.figure(figsize=(20, 16))
#sns.displot(data=pelkkä_miesten_muutos, x="Area", y="Percentual change")
#plt.title('Change in percentage from the overall population to the candidates')
#plt.xlabel('City')
#plt.ylabel('Change in percentage')
#plt.show()
