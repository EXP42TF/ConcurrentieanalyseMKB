import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
from io import StringIO

st.set_page_config(page_title="MKB-marktverkenner NL", layout="centered")

st.title("MKB-marktverkenner NL")

# ----- invoer -----
sbi_keuze = st.selectbox(
    "Kies een branche (SBI-hoofdletter):",
    ["G - Handel", "N - Zakelijke dienstverlening", "S - Overige diensten"]
)

prov_keuze = st.selectbox(
    "Kies een provincie:",
    ["Groningen", "Noord-Brabant", "Zuid-Holland"]
)

# ----- data ophalen -----
@st.cache_data
def haal_data(sbi_letter: str) -> pd.DataFrame:
    url = (
        "https://opendata.cbs.nl/ODataApi/OData/81578NED?$format=csv"
    )  # Vestigingen van bedrijven
    csv_text = requests.get(url).text
    df = pd.read_csv(StringIO(csv_text))
    return df[df["SBI2008Hoofdletter"] == sbi_letter]

sbi_letter = sbi_keuze.split()[0]  # pakt ‘G’, ‘N’ of ‘S’
data = haal_data(sbi_letter)

# ----- filter op provincie -----
subset = data[data["RegioS"] == prov_keuze]

# ----- grafiek -----
fig, ax = plt.subplots()
ax.plot(subset["Perioden"], subset["AantalVestigingen_1"])
ax.set_xlabel("Jaar")
ax.set_ylabel("Aantal vestigingen")
ax.set_title(f"{sbi_keuze} in {prov_keuze}")
st.pyplot(fig)

# ----- kerngetal -----
laatste = subset.iloc[-1]["AantalVestigingen_1"]
st.metric("Aantal vestigingen in laatste jaar", int(laatste))

# ----- bronvermelding -----
st.markdown(
    "_Bron: CBS StatLine, tabel 81578NED – CC BY 4.0._"
)
