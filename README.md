# TOMECTOR  

Script ini adalah alat sederhana untuk pengujian keamanan website, seperti:  
✅ **Port Scanning** – Mengecek port terbuka pada target.  
✅ **Directory Enumeration** – Mencari direktori tersembunyi seperti `/admin` atau `/login`.  
✅ **SQL Injection Testing** – Menguji kemungkinan celah SQL Injection.  
✅ **Subdomain Enumeration** – Menemukan subdomain yang tersembunyi.  

---

## **Instalasi & Penggunaan**  

Jalankan perintah berikut di **Termux** atau **Linux** untuk menginstal dan menjalankan script:  

```sh
pkg update && pkg upgrade  
pkg install python -y  
pip install -r requirements.txt  
chmod +x install
./install
