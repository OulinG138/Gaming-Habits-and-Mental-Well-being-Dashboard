import pandas as pd


def convert_to_categorical(df):
    columns_to_convert = [
        "Game",
        "Platform",
        "earnings",
        "whyplay",
        "Gender",
        "Work",
        "Residence_ISO3",
        "Birthplace_ISO3",
    ]

    df[columns_to_convert] = df[columns_to_convert].apply(
        lambda x: x.astype("category")
    )

    df["GADE"] = pd.Categorical(
        df["GADE"],
        categories=[
            "Not difficult at all",
            "Somewhat difficult",
            "Very difficult",
            "Extremely difficult",
        ],
        ordered=True,
    )

    df["Degree"] = pd.Categorical(
        df["Degree"],
        categories=[
            "High school diploma (or equivalent)",
            "Bachelor\xa0(or equivalent)",
            "Master\xa0(or equivalent)",
            "Ph.D., Psy. D., MD (or equivalent)",
        ],
        ordered=True,
    )

    return df
