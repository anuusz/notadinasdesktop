import pandas as pd

def export_to_excel(data, filename):
    df = pd.DataFrame(data, columns=["ID", "Tanggal", "Pengirim", "Tempat", "Petugas"])
    df.drop(columns=["ID"], inplace=True)  # Sembunyikan kolom ID
    df.to_excel(filename, index=False)