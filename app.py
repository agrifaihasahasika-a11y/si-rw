import	json
import	os
import	streamlit	as	st
FILE_DATA	=	"data_warga.json"
#	==========================================
#	1.	MODULARISASI	(FUNGSI	I/O	&	PERSISTENSI)
#	==========================================
def	muat_data():
				"""Membaca	data	dari	file	JSON.	Jika	file	belum	ada,	kembalikan	list	kosong."""
				if	not	os.path.exists(FILE_DATA):
								return	[]
				try:
								with	open(FILE_DATA,	"r")	as	f:
											return	json.load(f)
				except	(json.JSONDecodeError,	FileNotFoundError):
								return	[]

def	simpan_data(data):
				"""Menyimpan	(menulis	ulang)	seluruh	data	ke	file	JSON."""
				with	open(FILE_DATA,	"w")	as	f:
								json.dump(data,	f,	indent=4)
#	==========================================
#	2.	LOGIKA	PERCABANGAN	(RULES	ENGINE)
#	==========================================
def	proses_kategori_warga(usia):
				if	usia	<	5:
								kategori	=	"Balita"
				elif	usia	<=	17:
								kategori	=	"Anak/Remaja"
				elif	usia	<=	59:
								kategori	=	"Dewasa/Produktif"
				else:
								kategori	=	"Lansia"
				return	kategori
#	==========================================
#	3.	INTERFACE	(STREAMLIT)	&	DATA	ARRAY
#	==========================================
st.set_page_config(page_title="Pendataan	Warga	RW	03",	layout="wide")
st.title("		Sistem	Pengelolaan	Data	Kependudukan	RW	03")
daftar_warga	=	muat_data()
#	---	FORM	INPUT	DI	SIDEBAR	--
st.sidebar.header("	Form	Input	Warga	Baru")
nik	=	st.sidebar.text_input("NIK	(16	Digit)")
nama	=	st.sidebar.text_input("Nama	Lengkap")
usia	=	st.sidebar.number_input("Usia",	min_value=0,	max_value=120,	value=25)
status_domisili	=	st.sidebar.selectbox("Status	Domisili",	["Tetap",	"Pendatang"])
if	st.sidebar.button("Simpan	Data"):
				if	len(nik)	!=	16:
								st.sidebar.error("NIK	harus	persis	16	digit!")
				elif	any(warga["nik"]	==	nik	for	warga	in	daftar_warga):
								st.sidebar.error("NIK	ini	sudah	terdaftar!")
				elif	not	nama.strip():
								st.sidebar.error("Nama	wajib	disi!")
				else:
								nama	=	nama.strip()
								kategori	=	proses_kategori_warga(usia)
								warga_baru	=	{
												"nik":	nik,
												"nama":	nama,
												"usia":	usia,
												"kategori":	kategori,
												"domisili":	status_domisili
								}
								daftar_warga.append(warga_baru)
								simpan_data(daftar_warga)
								st.sidebar.success(f"Data	{nama}	berhasil	ditambahkan!")
#	==========================================
#	4.	LOGIKA	PERULANGAN	(STATISTIK)
#	==========================================
total_lansia	=	0
total_pendatang	=	0
for	warga	in	daftar_warga:
		if	warga["kategori"]	==	"Lansia":
				total_lansia	+=	1
		if	warga["domisili"]	==	"Pendatang":
				total_pendatang	+=	1
col1,	col2,	col3	=	st.columns(3)
col1.metric("Total	Warga	Terdaftar",	len(daftar_warga))
col2.metric("Jumlah	Lansia",	total_lansia)
col3.metric("Warga	Pendatang",	total_pendatang)
st.divider()
st.subheader("	Tabel	Data	Warga	RW	03")
if	daftar_warga:
		st.dataframe(daftar_warga,	use_container_width=True)
else:
		st.info("Belum	ada	data	warga.	Gunakan	form	di	sebelah	kiri	untuk	menambah	data.")