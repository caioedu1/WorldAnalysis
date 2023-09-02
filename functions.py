import win32com.client as win32
import os
import pandas as pd

"""Automatically send emails with the plot figures"""


def send_email(emails):
    # Check if emails is a list of strings
    if (
        isinstance(emails, list)
        and all(isinstance(i, str) for i in emails)
        or (isinstance(emails, str))
    ):
        if not isinstance(emails, list):
            emails = [emails]
        try:
            outlook = win32.Dispatch("outlook.application")
            mail = outlook.CreateItem(0)
            mail.To = ";".join(emails)
            mail.Subject = "Requested Files"
            mail.HTMLBody = (
                '<h2> Files based on the analysis of "world-data-2023.csv" </h2>'
            )

            folder = r"C:\Users\Caioe\OneDrive\Área de Trabalho\Caio\GitHub\HarvardCS50\plot_figs"

            attachment_list = []
            for root, dirs, files in os.walk(folder):
                for arquivo in files:
                    full_path = os.path.join(root, arquivo)
                    attachment = mail.Attachments.Add(full_path)
                    attachment_list.append(attachment)

            mail.Send()
            print("Email sent.")
        except Exception as e:
            print(f"An error has occurred: {str(e)}")
    else:
        raise TypeError("Emails must be a string or a list of strings")


"""Data Clean"""


def data_clean(df):
    """Set float to 2 decimal places"""
    pd.options.display.float_format = "{:.2f}".format

    """Some countries has this weird symbol � in its name, so I decided 
    to pass the full row of all these countries to Null (None)"""
    df.loc[df["Country"].str.contains("�", na=False), :] = None


    """Renaming columns"""
    df = df.rename(
        columns={
            "Agricultural Land( %)": "Agricultural Land (%)",
            "Population: Labor force participation (%)": "Labor force participation (%)"
        }
    )

    
    """Passing columns to numeric and cleaning values"""
    df["Out of pocket health expenditure"] = pd.to_numeric(
        df["Out of pocket health expenditure"].str.replace("%", "")
    )
    df["Labor force participation (%)"] = pd.to_numeric(
        df["Labor force participation (%)"].str.replace("%", "")
    )
    df["Density (P/Km2)"] = pd.to_numeric(
        df.iloc[:, 1].str.replace('"', "").str.replace(" ", "").str.replace(",", ".")
    )
    df["GDP"] = pd.to_numeric(
        df["GDP"].str.replace("[\$,]", "", regex=True).astype(float)
    )
    df["Armed Forces size"] = pd.to_numeric(
        df["Armed Forces size"].str.replace('"', "").str.replace(",", "")
    )
    df["Forested Area (%)"] = pd.to_numeric(
        df["Forested Area (%)"].str.replace("%", "")
    )
    df["Gross primary education enrollment (%)"] = pd.to_numeric(
        df["Gross primary education enrollment (%)"].str.replace("%", "")
    )
    df["Gross tertiary education enrollment (%)"] = pd.to_numeric(
        df["Gross tertiary education enrollment (%)"].str.replace("%", "")
    )
    df["CPI"] = pd.to_numeric(df["CPI"].str.replace(",", ""))
    df["Urban_population"] = pd.to_numeric(df["Urban_population"].str.replace(",", ""))
    df["Agricultural Land (%)"] = pd.to_numeric(
        df["Agricultural Land (%)"].str.replace("%", ""), errors="coerce"
    )
    df["Population"] = pd.to_numeric(df["Population"].str.replace(",", ""))
    df["Country"] = df["Country"].str.replace("S�����������", "Sao Tome and Principe")
    df["Unemployment rate"] = pd.to_numeric(
        df["Unemployment rate"].str.replace("%", "")
    )
    df["Tax revenue (%)"] = pd.to_numeric(df["Tax revenue (%)"].str.replace("%", ""))
    df["Total tax rate"] = pd.to_numeric(df["Total tax rate"].str.replace("%", ""))
    df["CPI Change (%)"] = (
        pd.to_numeric(
            df["CPI Change (%)"].str.replace("%", "").str.replace(".", ""),
            errors="coerce",
        )
        / 100
    )
    df["Co2-Emissions"] = pd.to_numeric(df["Co2-Emissions"].str.replace(",", ""))
    
    """Add some important columns"""
    df["CO2-Emissions/person"] = df["Population"] / df["Co2-Emissions"]
    df["GDP per capita"] = df["GDP"] / df["Population"]

    return df
