# Elshinta Chat Internal

Elshinta Chat Internal adalah aplikasi chat internal kantor (lokal/LAN-first) untuk komunikasi tim.

## Fitur
- Register dan login (username/password)
- Room: Umum, room per divisi, room custom (admin)
- Direct Message (DM) antar user
- Upload avatar dan gambar pesan (max 5MB)
- Chat realtime via WebSocket (Django Channels)
- Admin panel untuk manage divisi, user, room, announcement
- Cleanup pesan otomatis lebih dari 3 hari

## Stack
- Frontend: React + Vite + Tailwind
- Backend: Django, Django REST Framework, Django Channels
- Database: MySQL
- Media: disimpan lokal di folder `backend/media`

## Struktur folder

elshinta-chat-internal/
├── backend/  (Django project)
├── frontend/ (React + Vite)
├── README.md
└── .gitignore

Lihat `backend/README.md` dan `frontend/README.md` untuk detail per bagian.

## Setup MySQL (singkat)
1. Install MySQL di mesin lokal.
2. Buat database dan user:

```sql
CREATE DATABASE elshinta CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'elshinta_user'@'localhost' IDENTIFIED BY 'yourpassword';
GRANT ALL PRIVILEGES ON elshinta.* TO 'elshinta_user'@'localhost';
FLUSH PRIVILEGES;
```

## Cara install backend
1. Masuk ke folder `backend`.
2. Buat virtualenv dan install dependencies:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Salin `.env.example` ke `.env` dan edit sesuai konfigurasi MySQL.

## Migrate database & create superuser

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

## Menjalankan backend lokal

```bash
python manage.py runserver 0.0.0.0:8000
```

Akses admin: http://localhost:8000/admin

## Install frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend akan tersedia di http://localhost:5173 (default Vite).

## Akses dari komputer lain di LAN
- Jalankan backend dengan `python manage.py runserver 0.0.0.0:8000`.
- Pastikan firewall mengizinkan port 8000 dan 5173.
- Gunakan IP lokal mesin, misal `http://192.168.1.10:8000`.

## WebSocket
- WebSocket endpoint: `ws://<host>:8000/ws/chat/<room_name>/`

## Cleanup pesan lama

```bash
python manage.py cleanup_old_messages
```

## Contoh `.env`

Lihat `backend/.env.example` dan `frontend/.env.example`.

## Cara push ke GitHub

```bash
git init
git add .
git commit -m "Initial commit - Elshinta Chat Internal"
git branch -M main
git remote add origin https://github.com/ahmadalvin92/elshinta-chat-internal.git
git push -u origin main
```

## Catatan v2
- Tombol/menu untuk voice/video call disiapkan di UI; implementasi WebRTC di TODO.

---

Developed by Ahmad Alvin Griffin


