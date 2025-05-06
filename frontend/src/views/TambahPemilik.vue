<template>
    <div class="content">
      <div class="col-md-8">
        <div class="card card-user">
          <div class="card-header">
            <h5 class="card-title">Tambah Pemilik</h5>
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
                      v-model="formData.nama"
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
                      v-model="formData.email"
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
                    <label>Phone</label>
                    <input 
                      type="text" 
                      class="form-control" 
                      placeholder="Phone" 
                      v-model="formData.no_telp"
                      :class="{'is-invalid': errors.no_telp}"
                      required
                    />
                    <div v-if="errors.no_telp" class="invalid-feedback">{{ errors.no_telp }}</div>
                  </div>
                </div>
              </div>
  
              <div class="row">
                <div class="update ml-auto mr-auto">
                  <button type="submit" class="btn btn-update-profile btn-round">Tambah Pemilik</button>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        formData: {
          nama: '',
          email: '',
          no_telp: ''
        },
        notification: {
          message: '',
          type: ''
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
        // Reset errors and notification
        this.errors = {};
        this.notification = {};
  
        // Validasi form
        if (!this.formData.nama) {
          this.errors.nama = 'Nama tidak boleh kosong';
        }
        if (!this.formData.email) {
          this.errors.email = 'Email tidak boleh kosong';
        } else if (!this.isValidEmail(this.formData.email)) {
          this.errors.email = 'Format email tidak valid';
        } else if (await this.isEmailExist(this.formData.email)) {
          this.errors.email = 'Email sudah terdaftar';
        }
        if (!this.formData.no_telp) {
          this.errors.no_telp = 'Nomor telepon tidak boleh kosong';
        }
  
        // Jika ada error, jangan kirim form
        if (Object.keys(this.errors).length > 0) {
          return;
        }
  
        // Kirim data ke server
        axios.post('http://127.0.0.1:5000/tambah-pemilik', this.formData)
          .then(() => {
            this.notification = { message: 'Pemilik berhasil ditambahkan!', type: 'success' };
            this.formData = { nama: '', email: '', no_telp: '' }; // Reset form
          })
          .catch(error => {
            this.notification = { message: 'Pemilik gagal ditambahkan!', type: 'error' };
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
  };
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
  