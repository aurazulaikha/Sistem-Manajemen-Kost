from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from flask import Flask, jsonify, send_from_directory
from werkzeug.security import check_password_hash
import os
import jwt

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}) 

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'db_kost'
app.config['SECRET_KEY'] = 'your_secret_key_here'
mysql = MySQL(app)

UPLOAD_FOLDER = r'D:\SEMESTER 5\Proyek\Kost\backend\uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def root():
    return 'Selamat datang di Kost Letter U'

@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400

    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id, password, roles FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user[1], password):
            # Generate JWT token
            token = jwt.encode({
                'user_id': user[0],
                'role': user[2],
                'exp': datetime.utcnow() + timedelta(hours=1)  # Correct usage of datetime
            }, app.config['SECRET_KEY'], algorithm='HS256')

            return jsonify({
                'message': 'Login successful',
                'token': token,
                'role': user[2]
            }), 200

        return jsonify({'error': 'Invalid email or password'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()

@app.route('/logout', methods=['POST'])
def logout():
    return jsonify({'message': 'Logout successful, token invalidated (remove token on client side)'}), 200

@app.route('/register', methods=['POST'])
def register():
    if request.is_json:
        data = request.get_json()

        # Get data from the request
        nama = data.get('nama')
        email = data.get('email')
        password = data.get('password')
        no_telp = data.get('no_telp')

        # Validate required fields
        if not (nama and email and password and no_telp):
            return jsonify({'error': 'Semua field harus diisi'}), 400

        # Validate password length
        if len(password) < 8 or len(password) > 20:
            return jsonify({'error': 'Password harus memiliki panjang antara 8 hingga 20 karakter'}), 400

        # Set role to 'penyewa' directly
        roles = 'penyewa'

        # Check if email or phone number already exists
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s OR no_telp = %s", (email, no_telp))
        existing_user = cursor.fetchone()
        cursor.close()

        if existing_user:
            return jsonify({'error': 'Email atau nomor telepon sudah terdaftar'}), 400

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Insert into 'users' table
        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO users (nama, email, password, roles, no_telp) VALUES (%s, %s, %s, %s, %s)",
            (nama, email, hashed_password, roles, no_telp)
        )
        mysql.connection.commit()

        # Get the user ID
        user_id = cursor.lastrowid
        cursor.close()

        # Return success message
        return jsonify({'message': 'User berhasil terdaftar!'}), 201

    return jsonify({'error': 'Request harus berupa JSON'}), 400

@app.route('/list-user', methods=['GET'])
def list_user():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, nama, email, roles, no_telp FROM users")
    rows = cursor.fetchall()

    result = []
    for row in rows:
        user_data = {
            'id' : row[0],
            'nama': row[1],
            'email': row[2],
            'roles': row[3],
            'no_telp': row[4]
        }
        result.append(user_data)

    cursor.close()
    return jsonify(result), 200

@app.route('/tambah-user', methods=['POST'])
def tambah_user():
    if request.is_json:
        data = request.get_json()

        nama = data.get('nama')
        email = data.get('email')
        password = '12345678'  # Password default
        roles = data.get('roles')
        no_telp = data.get('no_telp')

        if not (nama and email and roles and no_telp):
            return jsonify({'error': 'Semua field harus diisi'}), 400

        hashed_password = generate_password_hash(password)

        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO users (nama, email, password, roles, no_telp) VALUES (%s, %s, %s, %s, %s)",
            (nama, email, hashed_password, roles, no_telp)
        )
        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': 'Data user berhasil ditambahkan!'})

@app.route('/edit-user/<int:user_id>', methods=['GET', 'PUT'])
def edit_user(user_id):
    if request.method == 'GET':
        # Mendapatkan data pengguna berdasarkan user_id
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id, nama, email, no_telp, roles FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        
        if user:
            return jsonify({
                'id': user[0],
                'nama': user[1],
                'email': user[2],
                'no_telp': user[3],
                'roles': user[4]
            })
        else:
            return jsonify({'error': 'User tidak ditemukan'}), 404

    elif request.method == 'PUT':
        if request.is_json:
            data = request.get_json()

            nama = data.get('nama')
            email = data.get('email')
            no_telp = data.get('no_telp')

            if not (nama and email and no_telp):
                return jsonify({'error': 'Semua field harus diisi'}), 400

            # Update data user
            cursor = mysql.connection.cursor()
            cursor.execute(
                "UPDATE users SET nama = %s, email = %s, no_telp = %s WHERE id = %s",
                (nama, email, no_telp, user_id)
            )
            
            # Periksa roles pengguna, apakah 'pemilik' atau 'penyewa'
            cursor.execute("SELECT roles FROM users WHERE id = %s", (user_id,))
            roles = cursor.fetchone()[0]
            
            if roles == 'pemilik':
                # Update data di tabel pemilik
                cursor.execute(
                    "UPDATE pemilik SET nama = %s, email = %s, no_telp = %s WHERE user_id = %s",
                    (nama, email, no_telp, user_id)
                )
            elif roles == 'penyewa':
                # Update data di tabel penyewa
                cursor.execute(
                    "UPDATE penyewa SET nama = %s, email = %s, no_telp = %s WHERE user_id = %s",
                    (nama, email, no_telp, user_id)
                )
            
            # Commit perubahan
            mysql.connection.commit()
            cursor.close()

            return jsonify({'message': 'User dan data terkait berhasil diupdate!'}), 200
        else:
            return jsonify({'error': 'Permintaan harus berupa JSON'}), 400

@app.route('/delete-user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        # Cek apakah user dengan ID tersebut ada di database
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()

        if not user:
            cursor.close()
            return jsonify({'error': 'User tidak ditemukan'}), 404

        # Hapus user dari tabel users
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': 'User berhasil dihapus!'}), 200
    except Exception as e:
        return jsonify({'error': f'Gagal menghapus user: {str(e)}'}), 500

@app.route('/list-pemilik', methods=['GET'])
def list_pemilik():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, nama, email, no_telp FROM pemilik")
    rows = cursor.fetchall()

    result = []
    for row in rows:
        pemilik_data = {
            'id' : row[0],
            'nama': row[1],
            'email': row[2],
            'no_telp': row[3]
        }
        result.append(pemilik_data)

    cursor.close()
    return jsonify(result), 200

@app.route('/tambah-pemilik', methods=['POST'])
def tambah_pemilik():
    if request.is_json:
        data = request.get_json()

        nama = data.get('nama')
        email = data.get('email')
        no_telp = data.get('no_telp')

        if not (nama and email and no_telp):
            return jsonify({'error': 'Nama, email, dan no_telp harus diisi'}), 400

        # Koneksi ke database
        try:
            cursor = mysql.connection.cursor()
        except Exception as e:
            return jsonify({'error': f'Koneksi database gagal: {str(e)}'}), 500

        # Cek apakah user sudah ada di tabel 'users'
        cursor.execute("SELECT id FROM users WHERE nama = %s AND email = %s AND no_telp = %s", (nama, email, no_telp))
        user = cursor.fetchone()

        if not user:
            cursor.close()
            return jsonify({'error': 'User dengan informasi tersebut tidak ditemukan di tabel users!'}), 404

        user_id = user[0]

        # Cek apakah pemilik sudah ada untuk user ini
        cursor.execute("SELECT id FROM pemilik WHERE user_id = %s", (user_id,))
        pemilik_exists = cursor.fetchone()

        if pemilik_exists:
            cursor.close()
            return jsonify({'error': 'Pemilik sudah ada untuk user ini!'}), 400

        # Insert data pemilik ke tabel pemilik
        try:
            cursor.execute(
                "INSERT INTO pemilik (nama, email, no_telp, user_id) VALUES (%s, %s, %s, %s)",
                (nama, email, no_telp, user_id)
            )
            mysql.connection.commit()
            cursor.close()
            return jsonify({'message': 'Pemilik berhasil ditambahkan!'}), 201
        except Exception as e:
            cursor.close()
            return jsonify({'error': f'Gagal menambahkan pemilik: {str(e)}'}), 500
    else:
        return jsonify({'error': 'Permintaan harus berupa JSON'}), 400
    
@app.route('/edit-pemilik/<int:pemilik_id>', methods=['GET', 'PUT'])
def edit_pemilik(pemilik_id):
    if request.method == 'GET':
        # Mendapatkan data pemilik berdasarkan pemilik_id
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id, nama, email, no_telp, user_id FROM pemilik WHERE id = %s", (pemilik_id,))
        pemilik = cursor.fetchone()
        cursor.close()
        
        if pemilik:
            return jsonify({
                'id': pemilik[0],
                'nama': pemilik[1],
                'email': pemilik[2],
                'no_telp': pemilik[3]
            })
        else:
            return jsonify({'error': 'Pemilik tidak ditemukan'}), 404

    elif request.method == 'PUT':
        if request.is_json:
            data = request.get_json()

            nama = data.get('nama')
            email = data.get('email')
            no_telp = data.get('no_telp')

            if not (nama and email and no_telp):
                return jsonify({'error': 'Semua field harus diisi'}), 400

            cursor = mysql.connection.cursor()

            # Mengambil user_id dari pemilik untuk memperbarui data di tabel users
            cursor.execute("SELECT user_id FROM pemilik WHERE id = %s", (pemilik_id,))
            user_id = cursor.fetchone()
            
            if not user_id:
                cursor.close()
                return jsonify({'error': 'User tidak ditemukan'}), 404

            # Update data di tabel pemilik
            cursor.execute(
                "UPDATE pemilik SET nama = %s, email = %s, no_telp = %s WHERE id = %s",
                (nama, email, no_telp, pemilik_id)
            )

            # Update data di tabel users berdasarkan user_id yang didapat dari tabel pemilik
            cursor.execute(
                "UPDATE users SET nama = %s, email = %s, no_telp = %s WHERE id = %s",
                (nama, email, no_telp, user_id[0])
            )
            
            # Commit perubahan
            mysql.connection.commit()
            cursor.close()

            return jsonify({'message': 'Pemilik dan data terkait berhasil diupdate!'}), 200
        else:
            return jsonify({'error': 'Permintaan harus berupa JSON'}), 400

@app.route('/delete-pemilik/<int:pemilik_id>', methods=['DELETE'])
def delete_pemilik(pemilik_id):
    try:
        cursor = mysql.connection.cursor()

        # Cek apakah pemilik ada dalam tabel pemilik
        cursor.execute("SELECT user_id FROM pemilik WHERE id = %s", (pemilik_id,))
        pemilik = cursor.fetchone()

        if not pemilik:
            cursor.close()
            return jsonify({'error': 'Pemilik tidak ditemukan'}), 404
        
        # Ambil user_id yang terkait dengan pemilik (jika ada)
        user_id = pemilik[0]

        # Hapus pemilik dari tabel pemilik
        cursor.execute("DELETE FROM pemilik WHERE id = %s", (pemilik_id,))

        # Jika ada user_id, hapus dari tabel users
        if user_id:
            cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        
        # Commit perubahan
        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': 'Pemilik dan user terkait berhasil dihapus!'}), 200
    except Exception as e:
        return jsonify({'error': f'Gagal menghapus pemilik: {str(e)}'}), 500
 
@app.route('/list-penyewa', methods=['GET'])
def list_penyewa():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, user_id, nama, email, no_telp FROM penyewa")
    rows = cursor.fetchall()

    result = []
    for row in rows:
        penyewa_data = {
            'id': row[0],
            'user_id': row[1],
            'nama': row[2],
            'email': row[3],
            'no_telp': row[4]
        }
        result.append(penyewa_data)

    cursor.close()
    return jsonify(result), 200

@app.route('/tambah-penyewa', methods=['POST'])
def tambah_penyewa():
    if request.is_json:
        data = request.get_json()

        nama = data.get('nama')
        email = data.get('email')
        no_telp = data.get('no_telp')

        if not (nama and email and no_telp):
            return jsonify({'error': 'Nama, email, dan no_telp harus diisi'}), 400

        try:
            cursor = mysql.connection.cursor()
        except Exception as e:
            return jsonify({'error': f'Koneksi database gagal: {str(e)}'}), 500

        cursor.execute("SELECT id FROM users WHERE nama = %s AND email = %s AND no_telp = %s", (nama, email, no_telp))
        user = cursor.fetchone()

        if not user:
            cursor.close()
            return jsonify({'error': 'User dengan informasi tersebut tidak ditemukan di tabel users!'}), 404

        user_id = user[0]

        cursor.execute("SELECT id FROM penyewa WHERE user_id = %s", (user_id,))
        penyewa_exists = cursor.fetchone()

        if penyewa_exists:
            cursor.close()
            return jsonify({'error': 'Penyewa sudah ada untuk user ini!'}), 400

        try:
            cursor.execute(
                "INSERT INTO penyewa (nama, email, no_telp, user_id) VALUES (%s, %s, %s, %s)",
                (nama, email, no_telp, user_id)
            )
            mysql.connection.commit()
            cursor.close()
            return jsonify({'message': 'Penyewa berhasil ditambahkan!'}), 201
        except Exception as e:
            cursor.close()
            return jsonify({'error': f'Gagal menambahkan penyewa: {str(e)}'}), 500
    else:
        return jsonify({'error': 'Permintaan harus berupa JSON'}), 400
    
@app.route('/edit-penyewa/<int:penyewa_id>', methods=['GET', 'PUT'])
def edit_penyewa(penyewa_id):
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id, nama, email, no_telp, user_id FROM penyewa WHERE id = %s", (penyewa_id,))
        penyewa = cursor.fetchone()
        cursor.close()

        if penyewa:
            return jsonify({
                'id': penyewa[0],
                'nama': penyewa[1],
                'email': penyewa[2],
                'no_telp': penyewa[3]
            }), 200
        else:
            return jsonify({'error': 'Penyewa tidak ditemukan'}), 404

    elif request.method == 'PUT':
        if request.is_json:
            data = request.get_json()

            nama = data.get('nama')
            email = data.get('email')
            no_telp = data.get('no_telp')

            # Validate the fields
            if not (nama and email and no_telp):
                return jsonify({'error': 'Semua field harus diisi'}), 400

            cursor = mysql.connection.cursor()

            # Get user_id from penyewa to update data in users table
            cursor.execute("SELECT user_id FROM penyewa WHERE id = %s", (penyewa_id,))
            user_id = cursor.fetchone()

            if not user_id:
                cursor.close()
                return jsonify({'error': 'User terkait tidak ditemukan'}), 404

            # Update data in penyewa table
            cursor.execute(
                "UPDATE penyewa SET nama = %s, email = %s, no_telp = %s WHERE id = %s",
                (nama, email, no_telp, penyewa_id)
            )

            # Update data in users table based on user_id fetched from penyewa table
            cursor.execute(
                "UPDATE users SET nama = %s, email = %s, no_telp = %s WHERE id = %s",
                (nama, email, no_telp, user_id[0])
            )

            # Commit changes to the database
            mysql.connection.commit()
            cursor.close()

            return jsonify({'message': 'Penyewa dan data terkait berhasil diperbarui!'}), 200
        else:
            return jsonify({'error': 'Permintaan harus berupa JSON'}), 400

@app.route('/delete-penyewa/<int:penyewa_id>', methods=['DELETE'])
def delete_penyewa(penyewa_id):
    try:
        cursor = mysql.connection.cursor()

        # Cek apakah penyewa ada dalam tabel penyewa
        cursor.execute("SELECT user_id FROM penyewa WHERE id = %s", (penyewa_id,))
        penyewa = cursor.fetchone()

        if not penyewa:
            cursor.close()
            return jsonify({'error': 'Penyewa tidak ditemukan'}), 404

        # Ambil user_id yang terkait dengan penyewa (jika ada)
        user_id = penyewa[0]

        # Hapus penyewa dari tabel penyewa
        cursor.execute("DELETE FROM penyewa WHERE id = %s", (penyewa_id,))
        
        # Jika ada user_id, hapus dari tabel users
        if user_id:
            cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        
        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': 'Penyewa dan user terkait berhasil dihapus!'}), 200
    except Exception as e:
        return jsonify({'error': f'Gagal menghapus penyewa: {str(e)}'}), 500

@app.route('/list-kamar', methods=['GET'])
def list_kamar():
    cursor = mysql.connection.cursor()

    # Select rooms with their status and tenant name if applicable
    query = """
    SELECT k.id, k.nomor_kamar, k.status_kamar, s.nama
    FROM kamar k
    LEFT JOIN status_penyewa sp ON k.id = sp.kamar_id
    LEFT JOIN penyewa s ON sp.penyewa_id = s.id
    """
    
    cursor.execute(query)
    rows = cursor.fetchall()

    result = []
    for row in rows:
        kamar_data = {
            'id': row[0],
            'nomor_kamar': row[1],
            'status_kamar': row[2] if row[2] else 'Tidak diketahui',
            # Logic updated: only show tenant name if the room is not available
            'nama': row[3] if row[2] != 'tersedia' and row[2] != 'proses verifikasi' and row[3] else ('-' if row[2] == 'tersedia' else '-')
        }
        result.append(kamar_data)

    cursor.close()
    return jsonify(result), 200

@app.route('/available_rooms', methods=['GET'])
def available_rooms():
    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT id, nomor_kamar
        FROM kamar
        WHERE status_kamar = 'tersedia'
    """)
    rooms = cursor.fetchall()
    cursor.close()
    return jsonify({"rooms": [{"id": room[0], "nomor_kamar": room[1]} for room in rooms]}), 200

@app.route('/reservasi', methods=['POST'])
def reservasi():
    try:
        nama = request.form.get('nama')
        email = request.form.get('email')
        kamar_id = request.form.get('kamar_id')
        periode_penyewaan = int(request.form.get('periode_penyewaan'))
        awal_penyewaan = request.form.get('awal_penyewaan')

        try:
            awal_penyewaan = datetime.strptime(awal_penyewaan, '%Y-%m-%d')
        except ValueError:
            return jsonify({"error": "Format tanggal awal_penyewaan tidak valid. Gunakan format YYYY-MM-DD."}), 400

        akhir_penyewaan = awal_penyewaan + timedelta(days=(periode_penyewaan * 90))
        jumlah_harga = periode_penyewaan * 2000000

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id FROM penyewa WHERE nama = %s AND email = %s", (nama, email))
        penyewa = cursor.fetchone()

        if not penyewa:
            return jsonify({"error": "Penyewa tidak ditemukan. Pastikan nama dan email sudah terdaftar."}), 400

        cursor.execute("SELECT id FROM kamar WHERE id = %s AND status_kamar = 'tersedia'", (kamar_id,))
        kamar = cursor.fetchone()

        if not kamar:
            return jsonify({"error": "Kamar tidak tersedia atau tidak ditemukan."}), 400

        cursor.execute(""" 
            SELECT * FROM reservasi WHERE kamar_id = %s AND (
                (awal_penyewaan BETWEEN %s AND %s) OR 
                (akhir_penyewaan BETWEEN %s AND %s)
            )
        """, (kamar_id, awal_penyewaan.strftime('%Y-%m-%d'), akhir_penyewaan.strftime('%Y-%m-%d'),
              awal_penyewaan.strftime('%Y-%m-%d'), akhir_penyewaan.strftime('%Y-%m-%d')))
        existing_reservation = cursor.fetchone()

        if existing_reservation:
            return jsonify({"error": "Kamar sudah terpesan untuk periode ini."}), 400

        if 'bukti_pembayaran' not in request.files:
            return jsonify({"error": "File bukti pembayaran harus diunggah."}), 400

        bukti_pembayaran = request.files['bukti_pembayaran']
        if bukti_pembayaran and allowed_file(bukti_pembayaran.filename):
            filename = secure_filename(bukti_pembayaran.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            bukti_pembayaran.save(filepath)
        else:
            return jsonify({"error": "File bukti pembayaran tidak valid. Harus berupa gambar (jpg, jpeg, png)."}), 400

        cursor.execute(""" 
            INSERT INTO reservasi (penyewa_id, kamar_id, periode_penyewaan, 
            awal_penyewaan, akhir_penyewaan, jumlah_harga, bukti_pembayaran) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (penyewa[0], kamar_id, periode_penyewaan,
              awal_penyewaan.strftime('%Y-%m-%d'), akhir_penyewaan.strftime('%Y-%m-%d'),
              jumlah_harga, filename))

        reservasi_id = cursor.lastrowid

        cursor.execute(""" 
            INSERT INTO verifikasi (penyewa_id, status_verifikasi, kamar_id, reservasi_id) 
            VALUES (%s, 'belum verifikasi', %s, %s)
        """, (penyewa[0], kamar_id, reservasi_id))

        verifikasi_id = cursor.lastrowid

        cursor.execute(""" 
            INSERT INTO status_penyewa (penyewa_id, status, kamar_id, reservasi_id, verifikasi_id) 
            VALUES (%s, 'inactive', %s, %s, %s)
        """, (penyewa[0], kamar_id, reservasi_id, verifikasi_id))

        cursor.execute("UPDATE kamar SET status_kamar = 'proses verifikasi' WHERE id = %s", (kamar_id,))
        mysql.connection.commit()
        cursor.close()
        return jsonify({"message": "Reservasi berhasil dilakukan!"}), 201

    except Exception as e:
        return jsonify({"error": f"Terjadi kesalahan: {str(e)}"}), 500
  
@app.route('/verifikasi/<int:id>', methods=['GET'])
def verifikasi_status(id):
    cursor = mysql.connection.cursor()

    query = """
    SELECT v.id, v.status_verifikasi, p.nama, p.email, p.no_telp, r.bukti_pembayaran, r.awal_penyewaan, r.akhir_penyewaan, r.jumlah_harga, k.nomor_kamar
    FROM verifikasi v
    JOIN penyewa p ON v.penyewa_id = p.id
    JOIN reservasi r ON v.reservasi_id = r.id
    JOIN kamar k ON v.kamar_id = k.id
    WHERE v.id = %s
    """
    cursor.execute(query, (id,))
    result = cursor.fetchone()

    if result:
        response = {
            'id': result[0],
            'status_verifikasi': result[1],
            'penyewa': {
                'nama': result[2],
                'email': result[3],
                'no_telp': result[4]
            },
            'reservasi': {
                'bukti_pembayaran': result[5],
                'awal_penyewaan': result[6],
                'akhir_penyewaan': result[7],
                'jumlah_harga': result[8],
                'nomor_kamar': result[9]
            }
        }
        cursor.close()
        return jsonify(response), 200
    else:
        cursor.close()
        return jsonify({'message': 'Data not found'}), 404

@app.route('/verifikasi/<int:id>', methods=['PUT'])
def update_verifikasi(id):
    data = request.get_json()
    status_verifikasi = data.get('status_verifikasi')

    # Koneksi ke database
    cur = mysql.connection.cursor()

    # Ambil data verifikasi dan reservasi
    cur.execute("""
        SELECT v.penyewa_id, v.kamar_id, r.akhir_penyewaan
        FROM verifikasi v
        JOIN reservasi r ON v.reservasi_id = r.id
        WHERE v.id = %s
    """, (id,))
    verifikasi_data = cur.fetchone()

    if not verifikasi_data:
        return jsonify({"message": "Verifikasi tidak ditemukan"}), 404

    penyewa_id, kamar_id, akhir_penyewaan = verifikasi_data

    # Update status verifikasi
    cur.execute("UPDATE verifikasi SET status_verifikasi = %s WHERE id = %s", (status_verifikasi, id))
    mysql.connection.commit()  # Ensure the change is committed to the database

    # Update status penyewa dan kamar berdasarkan status verifikasi
    if status_verifikasi == 'sudah verifikasi':
        if akhir_penyewaan:
            # Pastikan akhir_penyewaan adalah objek datetime
            if isinstance(akhir_penyewaan, datetime):
                akhir_penyewaan_date = akhir_penyewaan
            else:
                akhir_penyewaan_date = datetime.combine(akhir_penyewaan, datetime.min.time())

            # Periksa jika waktu penyewaan sudah lewat
            if datetime.now() > akhir_penyewaan_date:
                # Update status kamar menjadi 'tersedia'
                cur.execute("UPDATE kamar SET status_kamar = 'tersedia' WHERE id = %s", (kamar_id,))
                mysql.connection.commit()

                # Update status penyewa menjadi 'inactive'
                cur.execute("UPDATE status_penyewa SET status = 'inactive' WHERE penyewa_id = %s AND kamar_id = %s", (penyewa_id, kamar_id))
                mysql.connection.commit()
            else:
                # Menghitung 2 minggu sebelum akhir penyewaan
                two_weeks_before_end = akhir_penyewaan_date - timedelta(weeks=2)

                if two_weeks_before_end <= datetime.now() < akhir_penyewaan_date:
                    # Update status penyewa menjadi 'masa sewa akan habis'
                    cur.execute("UPDATE status_penyewa SET status = 'masa sewa akan habis' WHERE penyewa_id = %s AND kamar_id = %s", (penyewa_id, kamar_id))
                    mysql.connection.commit()

                    # Update status kamar menjadi 'masa sewa akan habis'
                    cur.execute("UPDATE kamar SET status_kamar = 'masa sewa akan habis' WHERE id = %s", (kamar_id,))
                    mysql.connection.commit()
                else:
                    # Update status penyewa menjadi 'active'
                    cur.execute("UPDATE status_penyewa SET status = 'active' WHERE penyewa_id = %s AND kamar_id = %s", (penyewa_id, kamar_id))
                    mysql.connection.commit()

                    # Update status kamar menjadi 'terisi'
                    cur.execute("UPDATE kamar SET status_kamar = 'terisi' WHERE id = %s", (kamar_id,))
                    mysql.connection.commit()
        else:
            # Jika tidak ada akhir_penyewaan, tetap update status penyewa menjadi 'active'
            cur.execute("UPDATE status_penyewa SET status = 'active' WHERE penyewa_id = %s AND kamar_id = %s", (penyewa_id, kamar_id))
            mysql.connection.commit()

    elif status_verifikasi == 'verifikasi ditolak':
        # Update status penyewa menjadi 'inactive'
        cur.execute("UPDATE status_penyewa SET status = 'inactive' WHERE penyewa_id = %s AND kamar_id = %s", (penyewa_id, kamar_id))
        mysql.connection.commit()

        # Update status kamar menjadi 'tersedia'
        cur.execute("UPDATE kamar SET status_kamar = 'tersedia' WHERE id = %s", (kamar_id,))
        mysql.connection.commit()

    # Tutup cursor
    cur.close()

    return jsonify({"message": "Status verifikasi, kamar, dan penyewa berhasil diperbarui"}), 200

@app.route('/update-status-kamar/<int:kamar_id>', methods=['PUT'])
def update_status_kamar(kamar_id):
    data = request.get_json()
    status_kamar = data.get('status_kamar')

    # Koneksi ke database
    cur = mysql.connection.cursor()

    # Update status kamar
    cur.execute("UPDATE kamar SET status_kamar = %s WHERE id = %s", (status_kamar, kamar_id))
    mysql.connection.commit()  # Ensure the change is committed to the database

    # Tutup cursor
    cur.close()

    return jsonify({"message": "Status kamar berhasil diperbarui"}), 200

@app.route('/list-verifikasi', methods=['GET'])
def get_verifikasi_list():
    cursor = mysql.connection.cursor()

    # Query untuk mengambil data yang diperlukan dari tabel terkait
    query = """
    SELECT v.id, v.status_verifikasi, p.nama, p.email, p.no_telp, r.awal_penyewaan, r.akhir_penyewaan, r.bukti_pembayaran, k.nomor_kamar
    FROM verifikasi v
    JOIN penyewa p ON v.penyewa_id = p.id
    JOIN reservasi r ON v.reservasi_id = r.id
    JOIN kamar k ON v.kamar_id = k.id
    """
    cursor.execute(query)
    results = cursor.fetchall()

    verifikasi_list = []
    for result in results:
        verifikasi_list.append({
            'id': result[0],
            'status_verifikasi': result[1],
            'penyewa': {
                'nama': result[2],
                'email': result[3],
                'no_telp': result[4]
            },
            'reservasi': {
                'awal_penyewaan': result[5],
                'akhir_penyewaan': result[6],
                'bukti_pembayaran': result[7]
            },
            'kamar': {
                'nomor_kamar': result[8]
            }
        })

    cursor.close()
    return jsonify(verifikasi_list), 200

@app.route('/uploads/<filename>')
def get_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/status-penyewa', methods=['GET'])
def get_status_penyewa():
    try:
        # Koneksi ke database
        cursor = mysql.connection.cursor()

        # Query SQL untuk join tabel-tabel
        query = """
        SELECT 
            penyewa.nama, 
            penyewa.email, 
            penyewa.no_telp,
            reservasi.awal_penyewaan,
            reservasi.akhir_penyewaan,
            status_penyewa.status
        FROM status_penyewa
        INNER JOIN penyewa ON status_penyewa.penyewa_id = penyewa.id
        INNER JOIN reservasi ON status_penyewa.reservasi_id = reservasi.id
        INNER JOIN verifikasi ON status_penyewa.verifikasi_id = verifikasi.id
        """
        
        # Eksekusi query
        cursor.execute(query)
        rows = cursor.fetchall()

        # Ambil deskripsi kolom untuk membuat dictionary
        columns = [desc[0] for desc in cursor.description]

        # Transformasi hasil query ke dalam list of dict
        results = [dict(zip(columns, row)) for row in rows]

        # Tutup koneksi database
        cursor.close()

        # Return hasil dalam bentuk JSON
        return jsonify(results), 200
    except Exception as e:
        # Jika terjadi error, tampilkan error dalam JSON
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/financial', methods=['GET'])
def get_financial_data():
    # Koneksi ke database
    cursor = mysql.connection.cursor()

    # Query untuk menghitung jumlah pendapatan per tahun dan total pendapatan keseluruhan
    query_pendapatan = """
    SELECT YEAR(r.awal_penyewaan) AS tahun, SUM(r.jumlah_harga) AS total_pendapatan
    FROM verifikasi v
    JOIN reservasi r ON v.reservasi_id = r.id
    WHERE v.status_verifikasi = 'sudah verifikasi'
    GROUP BY YEAR(r.awal_penyewaan)
    ORDER BY tahun DESC
    """
    
    # Query untuk menghitung jumlah pengeluaran per tahun
    query_pengeluaran = """
    SELECT YEAR(p.tanggal) AS tahun, SUM(p.jumlah_pengeluaran) AS total_pengeluaran
    FROM pengeluaran p
    GROUP BY YEAR(p.tanggal)
    ORDER BY tahun DESC
    """
    
    # Eksekusi query untuk menghitung pendapatan per tahun
    cursor.execute(query_pendapatan)
    pendapatan_rows = cursor.fetchall()

    # Eksekusi query untuk menghitung pengeluaran per tahun
    cursor.execute(query_pengeluaran)
    pengeluaran_rows = cursor.fetchall()

    # Menyusun data untuk pengeluaran dan pendapatan
    result = []
    total_pendapatan = 0
    total_pengeluaran = 0
    total_keuntungan = 0

    # Membuat dictionary untuk pengeluaran berdasarkan tahun
    pengeluaran_dict = {row[0]: row[1] for row in pengeluaran_rows}

    # Menggabungkan data pendapatan dan pengeluaran
    for row in pendapatan_rows:
        tahun = row[0]
        total_per_tahun = row[1]
        total_pendapatan += total_per_tahun  # Tambahkan total pendapatan

        # Ambil total pengeluaran untuk tahun yang sama
        total_per_tahun_pengeluaran = pengeluaran_dict.get(tahun, 0)

        # Hitung keuntungan per tahun (pendapatan - pengeluaran)
        keuntungan_per_tahun = total_per_tahun - total_per_tahun_pengeluaran
        total_keuntungan += keuntungan_per_tahun

        # Menyusun data untuk setiap tahun
        result.append({
            'tahun': tahun,
            'total_pendapatan': total_per_tahun,
            'total_pengeluaran': total_per_tahun_pengeluaran,
            'keuntungan': keuntungan_per_tahun
        })

    # Menambahkan total keseluruhan (pendapatan, pengeluaran, keuntungan)
    result.append({
        'tahun': 'Total',
        'total_pendapatan': total_pendapatan,
        'total_pengeluaran': total_pengeluaran,
        'keuntungan': total_keuntungan
    })

    # Menutup cursor
    cursor.close()

    # Mengembalikan response dengan data pendapatan, pengeluaran, dan keuntungan per tahun
    return jsonify(result), 200

@app.route('/kamar-aktif', methods=['GET'])
def kamar_aktif():
    try:
        cursor = mysql.connection.cursor()

        # Query to count rooms where:
        # - status_kamar is 'terisi' OR 'masa sewa akan habis'
        query = """
        SELECT 
            COUNT(*) 
        FROM kamar
        WHERE status_kamar IN ('terisi', 'masa sewa akan habis')
        """

        # Execute the query
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()

        # Check if result is available
        if result and result[0] > 0:
            return jsonify({'message': 'Success', 'data': {'jumlah_kamar': result[0]}}), 200
        else:
            return jsonify({'error': 'No rooms found with status "terisi" or "masa sewa akan habis"'}), 404

    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'}), 500

@app.route('/jumlah-users', methods=['GET'])
def jumlah_users():
    try:
        cursor = mysql.connection.cursor()

        # Query untuk menghitung jumlah pengguna
        query = """
        SELECT COUNT(*) FROM users
        """

        # Eksekusi query
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()

        # Periksa apakah hasil tersedia
        if result:
            return jsonify({'message': 'Success', 'data': {'jumlah_users': result[0]}}), 200
        else:
            return jsonify({'error': 'No users found'}), 404

    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'}), 500

@app.route('/total-pendapatan', methods=['GET'])
def get_total_pendapatan():
    try:
        # Koneksi ke database
        cursor = mysql.connection.cursor()

        # Query untuk menghitung total pendapatan keseluruhan
        query = """
        SELECT SUM(r.jumlah_harga) AS total_pendapatan
        FROM verifikasi v
        JOIN reservasi r ON v.reservasi_id = r.id
        WHERE v.status_verifikasi = 'sudah verifikasi'
        """

        # Eksekusi query
        cursor.execute(query)
        row = cursor.fetchone()

        # Menutup cursor
        cursor.close()

        # Memeriksa hasil query
        if row and row[0]:
            total_pendapatan = row[0]
            return jsonify({
                'message': 'Success',
                'total_pendapatan': total_pendapatan
            }), 200
        else:
            return jsonify({
                'error': 'No financial data found'
            }), 404

    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'}), 500

@app.route('/total-keuntungan', methods=['GET'])
def get_total_keuntungan():
    # Koneksi ke database
    cursor = mysql.connection.cursor()

    # Query untuk menghitung jumlah pendapatan per tahun dan total pendapatan keseluruhan
    query_pendapatan = """
    SELECT YEAR(r.awal_penyewaan) AS tahun, SUM(r.jumlah_harga) AS total_pendapatan
    FROM verifikasi v
    JOIN reservasi r ON v.reservasi_id = r.id
    WHERE v.status_verifikasi = 'sudah verifikasi'
    GROUP BY YEAR(r.awal_penyewaan)
    ORDER BY tahun DESC
    """
    
    # Query untuk menghitung jumlah pengeluaran per tahun
    query_pengeluaran = """
    SELECT YEAR(p.tanggal) AS tahun, SUM(p.jumlah_pengeluaran) AS total_pengeluaran
    FROM pengeluaran p
    GROUP BY YEAR(p.tanggal)
    ORDER BY tahun DESC
    """
    
    # Eksekusi query untuk menghitung pendapatan per tahun
    cursor.execute(query_pendapatan)
    pendapatan_rows = cursor.fetchall()

    # Eksekusi query untuk menghitung pengeluaran per tahun
    cursor.execute(query_pengeluaran)
    pengeluaran_rows = cursor.fetchall()

    # Menyusun data untuk pengeluaran dan pendapatan
    total_pendapatan = 0
    total_pengeluaran = 0
    total_keuntungan = 0

    # Membuat dictionary untuk pengeluaran berdasarkan tahun
    pengeluaran_dict = {row[0]: row[1] for row in pengeluaran_rows}

    # Menggabungkan data pendapatan dan pengeluaran untuk menghitung keuntungan
    for row in pendapatan_rows:
        tahun = row[0]
        total_per_tahun = row[1]
        total_pendapatan += total_per_tahun  # Tambahkan total pendapatan

        # Ambil total pengeluaran untuk tahun yang sama
        total_per_tahun_pengeluaran = pengeluaran_dict.get(tahun, 0)

        # Hitung keuntungan per tahun (pendapatan - pengeluaran)
        keuntungan_per_tahun = total_per_tahun - total_per_tahun_pengeluaran
        total_keuntungan += keuntungan_per_tahun

    # Menutup cursor
    cursor.close()

    # Mengembalikan response dengan total keuntungan keseluruhan
    return jsonify({'total_keuntungan': total_keuntungan}), 200

@app.route('/tambah-pengeluaran', methods=['POST'])
def tambah_pengeluaran():
    if request.is_json:
        data = request.get_json()

        # Ambil data dari request
        keterangan = data.get('keterangan')
        jumlah_pengeluaran = data.get('jumlah_pengeluaran')
        tanggal = data.get('tanggal')  # Format tanggal diharapkan 'YYYY-MM-DD'

        # Validasi input
        if not keterangan:
            return jsonify({'error': 'Keterangan harus diisi'}), 400
        if not isinstance(jumlah_pengeluaran, (int, float)) or jumlah_pengeluaran <= 0:
            return jsonify({'error': 'Jumlah pengeluaran harus berupa angka positif'}), 400
        if not tanggal:
            return jsonify({'error': 'Tanggal harus diisi'}), 400
        try:
            # Validasi format tanggal
            datetime.strptime(tanggal, '%Y-%m-%d')
        except ValueError:
            return jsonify({'error': 'Format tanggal tidak valid. Gunakan format YYYY-MM-DD'}), 400

        try:
            cursor = mysql.connection.cursor()
        except Exception as e:
            return jsonify({'error': f'Koneksi database gagal: {str(e)}'}), 500

        try:
            # Masukkan data ke tabel pengeluaran
            cursor.execute(
                "INSERT INTO pengeluaran (keterangan, jumlah_pengeluaran, tanggal) VALUES (%s, %s, %s)",
                (keterangan, jumlah_pengeluaran, tanggal)
            )
            mysql.connection.commit()
            cursor.close()
            return jsonify({'message': 'Pengeluaran berhasil ditambahkan!'}), 201
        except Exception as e:
            cursor.close()
            return jsonify({'error': f'Gagal menambahkan pengeluaran: {str(e)}'}), 500
    else:
        return jsonify({'error': 'Permintaan harus berupa JSON'}), 400

@app.route('/pengeluaran', methods=['GET'])
def get_pengeluaran():
    try:
        # Koneksi ke database
        cursor = mysql.connection.cursor()

        # Query untuk mendapatkan daftar pengeluaran
        query_pengeluaran = """
        SELECT id, keterangan, jumlah_pengeluaran, tanggal
        FROM pengeluaran
        ORDER BY tanggal DESC
        """

        # Eksekusi query
        cursor.execute(query_pengeluaran)
        pengeluaran = cursor.fetchall()

        # Format hasil sebagai list of dict
        pengeluaran_list = []
        for row in pengeluaran:
            pengeluaran_list.append({
                'id': row[0],
                'keterangan': row[1],
                'jumlah_pengeluaran': row[2],
                'tanggal': row[3].strftime('%Y-%m-%d')  # Format tanggal menjadi string
            })

        # Menutup cursor
        cursor.close()

        return jsonify({
            'message': 'Success',
            'data': pengeluaran_list
        }), 200

    except Exception as e:
        return jsonify({'error': f'Terjadi kesalahan: {str(e)}'}), 500

@app.route('/informasi-penyewa', methods=['GET'])
def informasi_penyewa():
    # Mendapatkan token dari header Authorization
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': 'Token is required'}), 401

    try:
        # Decode token
        decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        user_id = decoded_token['user_id']

        # Query informasi penyewa
        cursor = mysql.connection.cursor()
        query = """
            SELECT 
                penyewa.nama, 
                penyewa.email, 
                penyewa.no_telp, 
                kamar.nomor_kamar, 
                status_penyewa.status AS status_penyewa, 
                verifikasi.status_verifikasi, 
                reservasi.awal_penyewaan, 
                reservasi.akhir_penyewaan
            FROM penyewa
            LEFT JOIN status_penyewa ON penyewa.id = status_penyewa.penyewa_id
            LEFT JOIN verifikasi ON penyewa.id = verifikasi.penyewa_id
            LEFT JOIN reservasi ON penyewa.id = reservasi.penyewa_id
            LEFT JOIN kamar ON status_penyewa.kamar_id = kamar.id
            WHERE penyewa.user_id = %s
              AND (verifikasi.status_verifikasi = 'sudah verifikasi' OR verifikasi.status_verifikasi IS NULL)
        """
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()

        if not result:
            return jsonify({'error': 'Data penyewa tidak ditemukan atau belum diverifikasi'}), 404

        # Mapping hasil query ke dalam JSON
        data = {
            'nama': result[0],
            'email': result[1],
            'no_telp': result[2],
            'nomor_kamar': result[3],
            'status_penyewa': result[4],
            'status_verifikasi': result[5],
            'awal_penyewaan': result[6],
            'akhir_penyewaan': result[7],
        }
        return jsonify(data), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()

@app.route('/profile', methods=['GET'])
def profile():
    # Mendapatkan token dari header Authorization
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': 'Token is required'}), 401

    try:
        # Decode token
        decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        user_id = decoded_token['user_id']

        # Query informasi profil pengguna
        cursor = mysql.connection.cursor()
        query = """
            SELECT 
                id, 
                nama, 
                email, 
                roles, 
                no_telp 
            FROM users
            WHERE id = %s
        """
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()

        if not result:
            return jsonify({'error': 'Data pengguna tidak ditemukan'}), 404

        # Mapping hasil query ke dalam JSON
        data = {
            'id': result[0],
            'nama': result[1],
            'email': result[2],
            'roles': result[3],
            'no_telp': result[4],
        }
        return jsonify(data), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()

@app.route('/list-kamar-penyewa', methods=['GET'])
def list_kamar_penyewa():
    cursor = mysql.connection.cursor()

    # Select rooms with their status and tenant name if applicable
    query = """
    SELECT k.id, k.nomor_kamar, k.status_kamar
    FROM kamar k
    LEFT JOIN status_penyewa sp ON k.id = sp.kamar_id
    """
    
    cursor.execute(query)
    rows = cursor.fetchall()

    result = []
    for row in rows:
        kamar_data = {
            'id': row[0],
            'nomor_kamar': row[1],
            'status_kamar': row[2] if row[2] else 'Tidak diketahui'
        }
        result.append(kamar_data)

    cursor.close()
    return jsonify(result), 200


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
