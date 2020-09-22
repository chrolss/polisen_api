from src.postgresql import postgresql
import os
import pandas as pd

#filepath_credentials = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'credentials/sql_credentials')
filepath_credentials = 'credentials/sql_credentials'
psql = postgresql('polisen', filepath_credentials)
engine = psql.create_connection()

# Get the analytics dataframe
res = engine.execute('SELECT * FROM fact_polisen')
df = pd.DataFrame(data=res.fetchall(), columns=res.keys())

unique_types = df.type.unique().tolist()

category_dict = {
    'Alkohollagen': 'Förargelse',
    'Anträffad död': 'Person i nöd',
    'Anträffat gods': 'Övrigt',
    'Arbetsplatsolycka': 'Olycka',
    'Bedrägeri': 'Stöld',
    'Bombhot': 'Bomb',
    'Brand': 'Brand',
    'Bråk': 'Personvåld',
    'Detonation': 'Bomb',
    'Djur': 'Övrigt',
    'Efterlyst person': 'Person i nöd',
    'Farligt föremål, misstänkt': 'Bomb',
    'Fjällräddning': 'Person i nöd',
    'Fylleri/LOB': 'Förargelse',
    'Försvunnen person': 'Person i nöd',
    'Hemfridsbrott': 'Personvåld',
    'Hets mot folkgrupp': 'Förargelse',
    'Häleri': 'Stöld',
    'Inbrott': 'Inbrott',
    'Inbrott, försök': 'Inbrott',
    'Knivlagen': 'Personvåld',
    'Kontroll person/fordon': 'Trafik',
    'Lagen om hundar och katter ': 'Övrigt',
    'Larm Inbrott': 'Inbrott',
    'Larm Överfall': 'Personvåld',
    'Luftfartslagen': 'Trafik',
    'Miljöbrott': 'Övrigt',
    'Missbruk av urkund': 'Övrigt',
    'Misshandel': 'Personvåld',
    'Misshandel, grov': 'Personvåld',
    'Mord/dråp': 'Mord',
    'Mord/dråp, försök': 'Mord',
    'Motorfordon, anträffat stulet': 'Stöld',
    'Motorfordon, stöld': 'Stöld',
    'Narkotikabrott': 'Övrigt',
    'Ofredande/förargelse': 'Förargelse',
    'Olaga frihetsberövande/människorov': 'Person i nöd',
    'Olaga hot': 'Personvåld',
    'Olaga intrång': 'Inbrott',
    'Olovlig körning': 'Trafik',
    'Ordningslagen': 'Förargelse',
    'Polisinsats/kommendering': 'Övrigt',
    'Rattfylleri': 'Trafik',
    'Räddningsinsats': 'Person i nöd',
    'Rån': 'Rån',
    'Rån väpnat': 'Rån',
    'Rån övrigt': 'Rån',
    'Rån, försök': 'Rån',
    'Sabotage mot blåljusverksamhet': 'Blåljussabotage',
    'Sammanfattning dag': 'Sammanfattning',
    'Sammanfattning eftermiddag': 'Sammanfattning',
    'Sammanfattning förmiddag': 'Sammanfattning',
    'Sammanfattning kväll': 'Sammanfattning',
    'Sammanfattning kväll och natt': 'Sammanfattning',
    'Sammanfattning natt': 'Sammanfattning',
    'Sammanfattning vecka':'Sammanfattning',
    'Sedlighetsbrott': 'Förargelse',
    'Sjukdom/olycksfall': 'Olycka',
    'Sjölagen': 'Trafik',
    'Skadegörelse': 'Skadegörelse',
    'Skottlossning': 'Skjutning',
    'Skottlossning, misstänkt': 'Skjutning',
    'Skyddslagen': 'Övrigt',
    'Spridning smittsamma kemikalier': 'Övrigt',
    'Stöld': 'Stöld',
    'Stöld, försök': 'Stöld',
    'Stöld/inbrott': 'Inbrott',
    'Trafikbrott': 'Trafik',
    'Trafikhinder': 'Trafik',
    'Trafikkontroll': 'Trafik',
    'Trafikolycka': 'Trafik',
    'Trafikolycka, personskada': 'Trafik',
    'Trafikolycka, singel': 'Trafik',
    'Trafikolycka, smitning från': 'Trafik',
    'Trafikolycka, vilt': 'Trafik',
    'Uppdatering': 'Sammanfattning',
    'Utlänningslagen': 'Utlänningslagen',
    'Vapenlagen': 'Övrigt',
    'Varningslarm/haveri': 'Olycka',
    'Våld/hot mot tjänsteman': 'Blåljussabotage',
    'Våldtäkt': 'Våldtäkt',
    'Våldtäkt, försök': 'Våldtäkt',
    'Vållande till kroppsskada': 'Personvåld',
    'Åldringsbrott': 'Stöld',
    'Övrigt': 'Övrigt'
}

df['category'] = df.type.apply(lambda x: category_dict[x])
df.sort_values('category', inplace=True)

mini_df = df[['category', 'type']]
mini_df = mini_df.drop_duplicates()

_ = mini_df.to_sql('dim_crime', engine, if_exists='replace', index=False)
