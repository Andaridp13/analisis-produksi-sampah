import pandas as pd

def baca_file():
    return pd.read_excel('disperkim-od_16985_jumlah_produksi_sampah_berdasarkan_kabupatenkota_v3_data.xlsx')

def tampilkan_data(data):
    print("\n--- Data 5 Baris Pertama ---")
    print(data.head())

def total_sampah_tahun_tertentu(data, tahun):
    print(f"\n--- Menghitung Total Sampah untuk Tahun {tahun} ---")
    total = data[data['tahun'] == tahun]['jumlah_produksi_sampah'].sum()
    print(f"Total sampah untuk tahun {tahun}: {total:,.2f} ton")
    return total

def hitung_total_per_tahun(data):
    print("\n--- Menghitung Total Per Tahun ---")
    hasil_per_tahun = data.groupby('tahun')['jumlah_produksi_sampah'].sum()
    print("Total sampah per tahun:")
    for tahun, total in hasil_per_tahun.items():
        print(f"Tahun {tahun}: {total:,.2f} ton")
    return dict(hasil_per_tahun)

def hitung_total_per_kota(data):
    print("\n--- Menghitung Total Per Kota ---")
    # Gunakan kolom 'nama_kabupaten_kota'
    hasil_per_kota = data.groupby(['nama_kabupaten_kota', 'tahun'])['jumlah_produksi_sampah'].sum()
    print("Total sampah per kota per tahun:")
    for (kota, tahun), total in hasil_per_kota.items():
        print(f"{kota} ({tahun}): {total:,.2f} ton")
    return dict(hasil_per_kota)

def simpan_hasil(hasil_tahun, hasil_kota):
    # Ubah dictionary ke DataFrame untuk menyimpan
    df_tahun = pd.DataFrame.from_dict(hasil_tahun, orient='index', columns=['Total Sampah'])
    df_tahun.index.name = 'Tahun'
    df_tahun.reset_index(inplace=True)
    df_tahun.to_csv('hasil_pertahun.csv', index=False)
    df_tahun.to_excel('hasil_pertahun.xlsx', index=False)

    # Simpan hasil per kota
    df_kota = pd.DataFrame.from_dict(hasil_kota, orient='index', columns=['Total Sampah'])
    df_kota.index = pd.MultiIndex.from_tuples(df_kota.index, names=['Kota', 'Tahun'])
    df_kota.reset_index(inplace=True)
    df_kota.to_csv('hasil_perkota.csv', index=False)
    df_kota.to_excel('hasil_perkota.xlsx', index=False)

def main():
    print("=== Program Analisis Data Produksi Sampah ===")
    data = baca_file()
    tampilkan_data(data)
    total_sampah_tahun_tertentu(data, 2022)
    hasil_tahun = hitung_total_per_tahun(data)
    hasil_kota = hitung_total_per_kota(data)
    simpan_hasil(hasil_tahun, hasil_kota)
    print("\nProgram selesai!")

if __name__ == "__main__":
    main()