import pandas as pd
import streamlit as st
import pickle


# Load the CSV file
df = pd.read_csv('carssales.csv', delimiter=',', encoding='utf-8')

result = df

st.title("Car Sales Data Explorer")

st.sidebar.header("Filter Options")

modify = st.sidebar.checkbox("Add filters and choose order")

#CONVERTI LES DATES AU BON FORMAT, DE OBJET A DATETIME
#.dt.tz_localize(None) RENDS LES TIMEZONES NAIVES
df["date de vente"] = pd.to_datetime(df["date de vente"]).dt.tz_localize(None)

#CONVERTI LA COLONNE MAKE AU FORMAT CATEGORY
df["constructeur"] = df["constructeur"].astype("category")

#FUNCTION POUR AJOUTER UN FILTRE FABRIQUANT ET MODELE
def make_model(df,option,int_filtered_value,asc):

                min_value = int(min(df["prix conseillé"]))
                max_value = int(max(df["prix conseillé"]))
                price = st.sidebar.slider("select price range",min_value = min_value, max_value=max_value, value=(min_value,max_value))
                price_filtered_value = (df["prix conseillé"] >= price[0]) & (df["prix conseillé"] <= price[1])

    #PRENDS UN TEXTE EN ENTREE
                maker = st.sidebar.text_input("choose maker")
    #UTILISE ISIN() POUR TROUVER LE FABRIQUANT DANS SA COLONNE    RETOURNE LISTE DE BOOLEEN
                filter_make = df["constructeur"].isin([maker.lower()])
    #ESPERLUETTE (&) COMBINE LES LISTES DE BOOLEEN
                all = filter_make & int_filtered_value & price_filtered_value
    #UTILISE (loc[]) POUR CREER UNE NOUVELLE DATAFRAME SELON LE FILTRE     RETOURNE LISTE D'OBJET
                make_finder = df.loc[all,:]
    #UTILISE (sort_values) AFIN DE TRIER SELON LA COLONNE ET L'ORDRE CHOISI
                result = make_finder.sort_values(option, ascending=asc)
        #CHECKBOX POUR DECIDER D'APPLIQUER FILTRE POUR LE MODELE   RETOURNE TRUE OU FALSE
                modèle=st.sidebar.checkbox("modèle filter")
        #CONDITIONELLE (IF) QUI PERMET OU NON LE FILTRAGE PAR MODELE
                if modèle :
            #(unique()) APPLIQUER AU FILTRE DES FABRIQUANTS AFIN D'ISOLER LES MODELES PROPRES AU FABRIQUANT
            #RETOURNE LISTE DE MODELES
                    model_uni = make_finder["modèle"].unique()
            #(MULTISELECT) OFFRE LE CHOIX DE FILTRER PLUSIEURS MODELE EN MEME TEMPS
                    modèle = st.sidebar.multiselect("choose modèle",model_uni)
                    model_filter = df["modèle"].isin(modèle)
            #RAJOUTE LE FILTRE MODELE
                    all = all & model_filter & price_filtered_value
                    make_finder = df.loc[all,:]
                    result = make_finder.sort_values(option, ascending=asc)
            #ELSE QUI RESTAURE LE BON FILTRE
                else :
                    all = (filter_make & int_filtered_value) & price_filtered_value
                    make_finder = df.loc[all,:]
                    result = make_finder.sort_values(option, ascending=asc)
                return(result)

#APPLIQUE CONDITION SI CHECKBOX EST (TRUE)
if modify :

    asc = st.sidebar.checkbox("Ascending order")
    option = st.sidebar.selectbox("chose a category",(df.columns)) 
    modify2 = st.sidebar.checkbox("Chose two columns to compare")
#APPLIQUE CONDITION SI CHECKBOX EST (TRUE) POUR AGGREGATION    
    if modify2 :
    #CREATION DES DATFRAMES QUANTITATIVE ET QUALITATIVE    
        newdf = df.select_dtypes(include=['int64', 'float64']).columns
        newdf2 = df.select_dtypes(include=['category', 'object']).columns
    
        group_columns = st.sidebar.multiselect("Choose categorical columns to group by", newdf2)
        agg_columns = st.sidebar.multiselect('Choose numeric columns for aggregation', newdf)
    #SI LES DEUX COLONNES RESEIGNER..    
        if agg_columns and group_columns:
    #..AGGREGATION
            grouped_df = df.groupby(group_columns)[agg_columns].agg(['mean', 'sum', 'min', 'max'])
            grouped_df = grouped_df.sort_values(by=group_columns, ascending=asc)
            st.write(grouped_df)  
       
    constructeur=st.sidebar.checkbox("more filters")
#SI COLONNE NUMERIQUE    
    if pd.api.types.is_numeric_dtype(df[option]) | pd.api.types.is_float_dtype(df[option]):
        min_value = int(min(df[option]))
        max_value = int(max(df[option]))
        step1 = max(1, (max_value - min_value) // 100)
        value1 = st.slider("select value",min_value,max_value,step=step1,value=(min_value, max_value))
    #FILTRE EN RAPPORT AVEC LA RANGEE CHOISI   
        int_filtered_value = (df[option] >= value1[0]) & (df[option] <= value1[1])
    #APPLIQUE CONDITION SI CHECKBOX EST (TRUE)
        if constructeur :
    #APPLIQUE FUNCTION        
            result = make_model(df,option,int_filtered_value,asc)  
    #SINON NE PREND QUE VALEURS DE FILTRE RESEIGNER PLUS HAUT (int_filtered_value)                  
        else :
            make_finder = df.loc[int_filtered_value,:]
            result = make_finder.sort_values(option, ascending=asc)
    #MEME CHOSE POUR LES DATES        
    elif pd.api.types.is_datetime64_any_dtype(df[option]):
        min_value = df[option].min()
        max_value = df[option].max()
        date_value = st.date_input("date",value=(min_value.date(), max_value.date()), min_value=min_value.date(), max_value=max_value.date())
       #VERIFICATION QU'IL Y A BIEN DEUX DATES
        if isinstance(date_value, tuple) and len(date_value) == 2:
            start_date, end_date = date_value
            start_date = pd.to_datetime(start_date)
            end_date = pd.to_datetime(end_date)
            date_filter = (df[option] >= start_date) & (df[option] <= end_date)
            date_finder = df.loc[date_filter,:]
            result = date_finder.sort_values(option, ascending=asc)
        else :
            pass
        if constructeur :
           result = make_model(df,option,date_filter,asc)
    #MEME CHOSE POUR LES OBJET,CATEGORIE
    else :
        uni = df[option].unique()
        sel = st.sidebar.multiselect("chose",uni)
        filt = df[option].isin(sel)
        res = df.loc[filt,:]
        result = res.sort_values(option, ascending=asc)
    
        if constructeur :
           result = make_model(df,option,filt,asc)         

else:
    pass
    
st.write(result)

#BOUTON TELECHARGEMENT
st.download_button(
   label = "Download csv",
   data = result.to_csv().encode("utf-8"),
   file_name = "cardataframe.csv",
   mime = "text/csv"
)

#ML

with open('model_pkl' , 'rb') as f:
    lr = pickle.load(f)

with open('model_pipeline' , 'rb') as g:
    pl = pickle.load(g)


# Interface utilisateur pour entrer de nouvelles données
st.title("Ajout de nouvelles données")

makes = ['kia', 'bmw', 'volvo', 'nissan', 'chevrolet', 'audi', 'ford',
       'hyundai', 'buick', 'cadillac', 'acura', 'lexus', 'infiniti',
       'jeep', 'mercedesenz', 'mitsubishi', 'mazda', 'mini', 'land rover',
       'lincoln', 'jaguar', 'volkswagen', 'toyota', 'subaru', 'scion',
       'porsche', 'chrysler', 'dodge', 'fiat', 'honda', 'gmc', 'ram',
       'bentley', 'maserati', 'smart', 'suzuki', 'tesla', 'Others']

models = ['sorento', '3 series', 's60', '6 series gran coupe', 'altima',
       'm5', 'cruze', 'a4', 'camaro', 'a6', 'optima', 'fusion', 'q5',
       '6 series', 'impala', '5 series', 'a3', 'xc70', 'sq5', 's5',
       'verano', 'suburban', 'elr', 'v60', 'x6', 'ilx', 'k900', 'malibu',
       'rx 350', 'versa', 'elantra', 'versa note', 'a8', 'x1', 'enclave',
       'tts', '4 series', 'silverado 2500hd', 'mdx', 'silverado 1500',
       'srx', 'x5', 'g coupe', 'g sedan', 'fx', 'santa fe', 'genesis',
       'equus', 'sonata', 'sonata hybrid', 'accent', 'veloster',
       'elantra coupe', 'azera', 'tucson', 'genesis coupe', 'wrangler',
       's-class', 'gs 350', 'outlander', 'mazda2', 'rio', 'c-class',
       '370z', 'soul', 'outlander sport', 'slk-class', 'es 350',
       'e-class', 'mazda3', 'cooper clubman', 'cooper', 'cx-9', 'forte',
       'compass', 'jx', 'lr4', 'mazda5', 'm', 'range rover evoque',
       'ls 460', 'glk-class', 'sportage', 'grand cherokee', 'mkx', 'mkt',
       'xf', 'gl-class', 'm-class', 'cooper countryman', 'lancer',
       'range rover sport', 'passat', 'corolla', 'xc60', 'sienna', 'juke',
       'yaris', 'sentra', 'nv', 'cc', 'camry', 'tacoma', 'jetta',
       'impreza wrx', 'fj cruiser', 'beetle', 'avalon', 'fr-s', 'nv200',
       'rogue', 'quest', 'maxima', 'cayenne', '911', 'xterra', 'prius',
       's80', 'frontier', 'boxster', 'camry hybrid', 'xb', 'cube',
       'jetta sportwagen', '4runner', 'sequoia', 'legacy', 'leaf',
       'armada', 'venza', 'murano', 'pathfinder', 'panamera',
       'highlander', '200', 'grand caravan', 'town and country', 'tahoe',
       'impala limited', 'charger', 'dart', '300', 'challenger',
       'journey', 'express cargo', 'sonic', 'equinox', 'express',
       'traverse', 'f-150', 'mustang', 'focus', 'explorer', 'escape',
       'fiesta', '500l', 'e-series wagon', 'expedition', 'e-series van',
       'f-250 super duty', 'f-350 super duty', 'santa fe sport',
       'cherokee', 'cr-v', 'cadenza', 'patriot', 'elantra gt', 'civic',
       'f-type', 'shelby gt500', 'q50', 'qx70', 'pilot', 'odyssey', 'xj',
       'accord', 'taurus', 'yukon xl', 'q60 convertible', 'qx60',
       'cooper roadster', 'cx-5', 'is 250', 'mazda6', 'cooper paceman',
       'range rover', 'sedona', '1500', 'mx-5 miata', 'rogue select',
       'cayman', 'cla-class', 'g-class', 'captiva sport', 'allroad',
       'ats', '2500', 'corvette', '7 series', 'x3', 'prius v',
       'continental gtc', 's6', 'xv crosstrek', 'a5', 'forester',
       'touareg', 'lacrosse', '3500', 'q7', 'tundra', 'avenger',
       'c-max energi', 'edge', 'c-max hybrid', 'spark', 'insight', 'flex',
       'transit connect', 'terrain', 'fit', 'sierra 1500',
       'fusion hybrid', 'rs 7', 'outback', 'navigator', 'lx 570',
       'lancer evolution', 'gx 460', 'qx80', 'rs 5', 'jetta gli', 'gt-r',
       'a7', 'es 300h', 'capt', 'm4', 'durango', 'grand', '500',
       'focus st', 'fusion energi', 'yukon', 'acadia', 'savana',
       'sierra 2500hd', 'q60 coupe', 'q70', 'qx50', 'ct 200h', 'mks',
       'cooper coupe', 'quattroporte', 'cls-class', 'mirage', 'sl-class',
       'sprinter', 'murano crosscabriolet', 'nv cargo', 'impreza', 'iq',
       'tc', 'xd', 'rav4', 'golf', 'jetta hybrid', 'tiguan', 'tl', 's7',
       'rdx', 'tsx', 'cts', 'regal', 'encore', 'xts', 'volt',
       'black diamond avalanche', 'escalade', 'escalade esv',
       'silverado 3500hd', 's8', 'rlx', '2 series', 'm6', 'm6 gran coupe',
       'sierra 3500hd', 'crosstour', 'qx', 'xk', 'mkz', 'rx 450h',
       'mazdaspeed3', 'lancer sportback', 'titan', 'fortwo',
       'c/v tradesman', 'brz', 'grand vitara', 'sx4', 'model s',
       'land cruiser', 'prius plug-in', 'prius c', 'gti',
       'beetle convertible', 'golf r', 'routan', 'corvette stingray',
       'ss', 'is 350', 'ghibli', 'xc90', 'ridgeline', 'highlander hybrid',
       'gr', 'promaster cargo van', '1 series', 'z4', 'cr-z',
       'g convertible', 'cts-v coupe', 'tribeca', 'savana cargo',
       'accord hybrid', 'm3', '3 series gran turismo', 'is 250 c',
       '5 series gran turismo', 'avalon hybrid', '6', 'matrix', 'Other',
       's4', 'cts coupe', 'lr2', 'eos', 'golf gti', 'macan',
       'cv tradesman', 'gs 450h', 'i8', 'nv passenger', 'wrx', 'x6 m',
       '500e', 'mkc', 'continental gt', 'tt rs', 'granturismo',
       'cl-class', 'transit van', '3', 'b-class electric drive', 'x5 m',
       'x4', 'transit wagon', 'rc f', 'colorado', '4 series gran coupe',
       'rc 350']

# Saisie des caractéristiques
ye = st.number_input('année', min_value=1980, max_value=2025)
co = st.number_input('condition', min_value=1, max_value=49)
km = st.number_input('kilométrage', min_value=1, max_value=600000)
maker = st.selectbox("choisir fabriquant",makes) 
model = st.selectbox("choisir model",models) 


# Lorsque l'utilisateur entre les données et clique sur le bouton, faire une prédiction
if st.button('Faire une prédiction'):
    new_data = pd.DataFrame({
        'model': [model],
        'make': [maker],   
        'year': [ye],
        'condition': [co],
        'odometer': [km]
    })


    transformed_data = pl.transform(new_data)

    prediction = lr.predict(transformed_data)

    st.write(f"Le prix pour la voiture est : {prediction[0]}")

 