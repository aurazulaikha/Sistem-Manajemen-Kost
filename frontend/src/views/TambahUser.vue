<template>
    <div class="content">
      <div class="col-md-8">
        <div class="card card-user">
          <div class="card-header">
            <h5 class="card-title">Tambah User</h5>
          </div>
          <div class="card-body">
            <!-- Notifikasi -->
            <div v-if="notification.message" :class="['notification', notification.type]">
              {{ notification.message }}
            </div>
  
            <form @submit.prevent="submitForm">
              <div class="row">
                <div class="col-md-12">
                  <div class="form-group">
                    <label>Nama</label>
                    <input 
                      type="text" 
                      class="form-control" 
                      placeholder="Nama" 
                      v-model="user.nama"
                      :class="{'is-invalid': errors.nama}"
                      required
                    />
                    <div v-if="errors.nama" class="invalid-feedback">{{ errors.nama }}</div>
                  </div>
                </div>
              </div>
              <div class="row">
                <div class="col-md-12">
                  <div class="form-group">
                    <label>Email</label>
                    <input 
                      type="email" 
                      class="form-control" 
                      placeholder="Email" 
                      v-model="user.email"
                      :class="{'is-invalid': errors.email}"
                      required
                    />
                    <div v-if="errors.email" class="invalid-feedback">{{ errors.email }}</div>
                  </div>
                </div>
              </div>
              <div class="row">
                <div class="col-md-12">
                  <div class="form-group">
                    <label>Roles</label>
                    <select class="form-control" v-model="user.roles" required>
                      <option value="admin">Admin</option>
                      <option value="penyewa">Penyewa</option>
                      <option value="pemilik">Pemilik</option>
                    </select>
                  </div>
                </div>
              </div>
              <div class="row">
                <div class="col-md-12">
                  <div class="form-group">
                    <label>Phone</label>
                    <input 
                      type="text" 
                      class="form-control" 
                      placeholder="Phone" 
                      v-model="user.no_telp"
                      :class="{'is-invalid': errors.no_telp}"
                      required
                    />
                    <div v-if="errors.no_telp" class="invalid-feedback">{{ errors.no_telp }}</div>
                  </div>
                </div>
              </div>
              <div class="row">
                <div class="update ml-auto mr-auto">
                  <button type="submit" class="btn btn-update-profile btn-round">Tambah User</button>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios'; // Import axios
  
  export default {
    data() {
      return {
        user: {
          nama: '',
          email: '',
          roles: '',
          no_telp: ''
        },
        notification: {
          message: '',
          type: '' // 'success' or 'error'
        },
        errors: {
          nama: '',
          email: '',
          no_telp: ''
        }
      };
    },
    methods: {
      async submitForm() {
        // Reset errors
        this.errors = {};
  
        // Validasi form
        if (!this.user.nama) {
          this.errors.nama = 'Nama tidak boleh kosong';
        }
        if (!this.user.email) {
          this.errors.email = 'Email tidak boleh kosong';
        } else if (!this.isValidEmail(this.user.email)) {
          this.errors.email = 'Format email tidak valid';
        } else if (await this.isEmailExist(this.user.email)) {
          this.errors.email = 'Email sudah terdaftar';
        }
        if (!this.user.no_telp) {
          this.errors.no_telp = 'Nomor telepon tidak boleh kosong';
        }
  
        // Jika ada error, jangan kirim form
        if (Object.keys(this.errors).length > 0) {
          return;
        }
  
        // Kirim data ke server atau API
        axios.post('http://127.0.0.1:5000/tambah-user', this.user)
          .then(response => {
            // Tampilkan notifikasi sukses
            this.notification.message = 'Data User berhasil ditambahkan!';
            this.notification.type = 'success'; // Green notification
            console.log(response.data);
  
            // Reset form setelah berhasil
            this.user = {
              nama: '',
              email: '',
              roles: '',
              no_telp: ''
            };
          })
          .catch(error => {
            // Tampilkan notifikasi error
            this.notification.message = 'Data gagal ditambahkan!';
            this.notification.type = 'error'; // Red notification
            console.error(error);
          });
      },
  
      // Cek format email valid
      isValidEmail(email) {
        const regex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
        return regex.test(email);
      },
  
      // Cek apakah email sudah ada
      async isEmailExist(email) {
        try {
          const response = await axios.get(`http://127.0.0.1:5000/check-email?email=${email}`);
          return response.data.exists;
        } catch (error) {
          console.error('Terjadi kesalahan saat memeriksa email:', error);
          return false;
        }
      }
    }
  }
  </script>
  
  <style scoped>
  .btn-update-profile {
    background-color: #75276d; 
    color: white; 
    border-color: #75276d;
  }
  
  .btn-update-profile:hover {
    background-color: #5e1d57;
    border-color: #5e1d57;
  }
  
  /* CSS untuk notifikasi */
  .notification {
    padding: 10px;
    margin-bottom: 20px;
    border-radius: 5px;
    font-weight: bold;
    text-align: center;
  }
  
  .notification.success {
    background-color: #28a745; /* Green */
    color: white;
  }
  
  .notification.error {
    background-color: #dc3545; /* Red */
    color: white;
  }
  
  /* Styling untuk input yang error */
  .is-invalid {
    border-color: #dc3545;
  }
  
  .invalid-feedback {
    color: #dc3545;
    font-size: 0.875em;
  }
  </style>
  