from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from io import StringIO
import re  # Import regex library

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def ssRNA(data_s):
    GSize = data_s['BaseCount'].str.len()

    def str_count(data, pattern):
        return data.apply(lambda x: len(re.findall(pattern, x)))

    # Counting specific patterns
    Count_TT = str_count(data_s['BaseCount'], "TT")
    
    # Counting possible dimers
    dimer_patterns = ["TT", "TC", "CT", "CC"]
    Count_Dimers = pd.DataFrame({pattern: str_count(data_s['BaseCount'], pattern) for pattern in dimer_patterns})
    
    # Step-by-step replacement and counting
    data_TT = data_s['BaseCount'].replace("TT", "BB", regex=True)
    Count_TC = str_count(data_TT, "TC")

    data_TC = data_TT.replace("TC", "DD", regex=True)
    Count_CT = str_count(data_TC, "CT")

    data_CT = data_TC.replace("CT", "EE", regex=True)
    Count_CC = str_count(data_CT, "CC")

    data_CC = data_CT.replace("CC", "FF", regex=True)

    Dimer_Count = pd.DataFrame({'TT': Count_TT, 'TC': Count_TC, 'CT': Count_CT, 'CC': Count_CC})

    # Counting Purines with replacement sequences
    purine_patterns = [
        ("ABB", "HHH"), ("BBA", "III"), ("GBB", "JJJ"), ("BBG", "KKK"),
        ("ADD", "LLL"), ("DDA", "MMM"), ("GDD", "NNN"), ("DDG", "OOO"),
        ("AEE", "PPP"), ("EEA", "QQQ"), ("GEE", "RRR"), ("EEG", "SSS"),
        ("AFF", "UUU"), ("FFA", "VVV"), ("GFF", "WWW"), ("FFG", "XXX")
    ]

    data = data_CC.copy()
    purine_counts = {}

    for original, replacement in purine_patterns:
        purine_counts[original] = str_count(data, original)
        data = data.replace(original, replacement, regex=True)

    Purines_Count = pd.DataFrame(purine_counts)
    Purines_Count.columns = ["ATT", "TTA", "GTT", "TTG", "ATC", "TCA", "GTC", "TCG",
                             "ACT", "CTA", "GCT", "CTG", "ACC", "CCA", "GCC", "CCG"]

    Comb_Count = pd.concat([Dimer_Count, Purines_Count], axis=1)

    MixedTT = Comb_Count['ATT'] + Comb_Count['TTA'] + Comb_Count['GTT'] + Comb_Count['TTG']
    MixedCC = Comb_Count['ACC'] + Comb_Count['CCA'] + Comb_Count['GCC'] + Comb_Count['CCG']
    MixedTC = Comb_Count['ATC'] + Comb_Count['TCA'] + Comb_Count['GTC'] + Comb_Count['TCG']
    MixedCT = Comb_Count['ACT'] + Comb_Count['CTA'] + Comb_Count['GCT'] + Comb_Count['CTG']

    PureTT = Comb_Count['TT'] - MixedTT
    PureCC = Comb_Count['CC'] - MixedCC
    PureTC = Comb_Count['TC'] - MixedTC
    PureCT = Comb_Count['CT'] - MixedCT

    TotalTTs = MixedTT * 0.5 + PureTT
    TotalCCs = MixedCC * 0.5 + PureCC
    TotalTCs = MixedTC * 0.5 + PureTC
    TotalCTs = MixedCT * 0.5 + PureCT

    FracTTs = TotalTTs / GSize * 100
    FracCCs = TotalCCs / GSize * 100
    FracTCs = TotalTCs / GSize * 100
    FracCTs = TotalCTs / GSize * 100

    TFracts = FracTTs * FracCCs * FracTCs * FracCTs
    PNNsFV = TFracts / GSize

    D90 = 10.41 + (19983.83 * PNNsFV)

    return D90  # Assuming D90 is calculated at the end of your function


# @app.get("/")
# def home():
#     return {"message": "FastAPI is up!"}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    print("Received file:", file.filename)

    try:
        contents = await file.read()
        decoded = contents.decode("utf-8")
        print("File content loaded")

        # Assuming one sequence in the file
        df = pd.read_csv(StringIO(decoded), names=["BaseCount"])
        d90 = ssRNA(df).values[0]  # Convert Series to float
  # Assuming ssRNA returns a single value like float

        return {"filename": file.filename, "D90": d90}
    
    except Exception as e:
        print("ERROR:", str(e))
        raise HTTPException(status_code=500, detail="Internal server error")


