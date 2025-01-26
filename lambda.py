import pandas as pd
import matplotlib.pyplot as plt

# Baca file
data = pd.read_excel('disperkim-od_16985_jumlah_produksi_sampah_berdasarkan_kabupatenkota_v3_data.xlsx')

# Jumlahkan total sampah per kab/kota per tahun
total_sampah_kota = data.groupby(['nama_kabupaten_kota', 'tahun'])['jumlah_produksi_sampah'].sum().reset_index()

# Tambahkan kolom Kategori
def kategorikan_sampah(jumlah):
    return 'Harus Segera Ditanggulangi' if jumlah > 400 else 'Aman'
total_sampah_kota['Kategori'] = total_sampah_kota['jumlah_produksi_sampah'].apply(kategorikan_sampah)

# Hitung bayaran sampah
total_sampah_kota['Bayaran_Sampah'] = total_sampah_kota['jumlah_produksi_sampah'] * 123000

# Tambahkan kolom pajak
total_sampah_kota['Pajak'] = total_sampah_kota.apply(
    lambda row: row['Bayaran_Sampah'] * 0.05 if row['Kategori'] == 'Harus Segera Ditanggulangi' else 0, 
    axis=1
)

# 1. Grafik Total Sampah per Kota per Tahun
plt.figure(figsize=(15, 10))
pivot_data = total_sampah_kota.pivot(index='nama_kabupaten_kota', columns='tahun', values='jumlah_produksi_sampah')
pivot_data.plot(kind='bar', stacked=False)
plt.title('Total Produksi Sampah per Kabupaten/Kota di Jawa Barat')
plt.xlabel('Kabupaten/Kota')
plt.ylabel('Jumlah Sampah (ton)')
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig('total_sampah_per_kota.png')
plt.close()

# 2. Grafik Perbandingan Kategori Sampah
kategori_counts = total_sampah_kota['Kategori'].value_counts()
plt.figure(figsize=(8, 8))
kategori_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=['#66b3ff', '#ff9999'])
plt.title('Perbandingan Kategori Sampah')
plt.ylabel('')
plt.savefig('perbandingan_kategori_sampah.png')
plt.close()

# 3. Grafik Pajak Berdasarkan Kota
pajak_per_kota = total_sampah_kota.groupby('nama_kabupaten_kota')['Pajak'].sum()
plt.figure(figsize=(15, 8))
pajak_per_kota.sort_values(ascending=False).plot(kind='bar', color='orange')
plt.title('Total Pajak Sampah per Kabupaten/Kota')
plt.xlabel('Kabupaten/Kota')
plt.ylabel('Total Pajak (Rp)')
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig('total_pajak_per_kota.png')
plt.close()

# 4. Grafik Tren Total Sampah per Tahun
total_sampah_tahunan = total_sampah_kota.groupby('tahun')['jumlah_produksi_sampah'].sum()
plt.figure(figsize=(10, 6))
total_sampah_tahunan.plot(kind='line', marker='o', color='green')
plt.title('Tren Total Produksi Sampah per Tahun')
plt.xlabel('Tahun')
plt.ylabel('Jumlah Sampah (ton)')
plt.grid(True)
plt.tight_layout()
plt.savefig('tren_total_sampah_per_tahun.png')
plt.close()

# Simpan hasil analisis ke Excel
total_sampah_kota.to_excel('analisis_sampah_lengkap.xlsx', index=False)

print("Proses selesai. Grafik tambahan dibuat, cek file berikut:")
print("- total_sampah_per_kota.png")
print("- perbandingan_kategori_sampah.png")
print("- total_pajak_per_kota.png")
print("- tren_total_sampah_per_tahun.png")
print("Data lengkap disimpan di 'analisis_sampah_lengkap.xlsx'.")
