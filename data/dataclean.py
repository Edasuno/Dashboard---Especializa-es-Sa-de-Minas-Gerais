import pandas as pd 

df = pd.read_csv("./data/doctoralia.csv")

df2 = df.drop(["newest_review_date", "url", "fetch_time"], axis=1)

df2["price"] = pd.to_numeric(df["price"], errors="coerce")


# Filtrar apenas as linhas onde "region" é "minas-gerais"
df2 = df2.loc[df2["region"] == "minas-gerais-mg"]


#Resolvendo preços absurds  na coluna price
df2 = df2[df2["price"] <= 1500]


#Tirando a media da coluna price para resolver os valores nulos e deixando 2 casas apos a ,
media_price = round(df2["price"].mean(), 2)

#Aplicando a todos os NaN
df2["price"].fillna(media_price, inplace=True)


#Resetando o Index para começar do 1
df2.reset_index(drop=True, inplace=True)
df2.index += 1

df2.index.name = "doctor_id"



#Resolvendo o NaN da coluna "reviews"

df2["reviews"].fillna(0, inplace=True)



df2.to_csv("./data/newdata.csv", index=True)


