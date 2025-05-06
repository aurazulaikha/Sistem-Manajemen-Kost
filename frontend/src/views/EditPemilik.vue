<template>
    <div class="content">
      <div class="col-md-8">
        <div class="card card-user">
          <div class="card-header">
            <h5 class="card-title">Edit Pemilik</h5>
          </div>
          <div class="card-body">
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
                      v-model="pemilik.nama"
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
                      v-model="pemilik.email"
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
                      v-model="pemilik.no_telp"
                      :class="{'is-invalid': errors.no_telp}"
                      required
                    />
                    <div v-if="errors.no_telp" class="invalid-feedback">{{ errors.no_telp }}</div>
                  </div>
                </div>
              </div>
              <div class="row">
                <div class="update ml-auto mr-auto">
                  <button type="submit" class="btn btn-update-profile btn-round">Edit Pemilik</button>
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
        pemilik: {
          id: '', 
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
    created() {
      const pemilikId = this.$route.params.id; 
      if (pemilikId) {
        this.getPemilikData(pemilikId); 
      } else {
        console.error('Pemilik ID tidak ditemukan');
      }
    },
    methods: {
      async getPemilikData(pemilikId) {
        try {
          const response = await axios.get(`http://127.0.0.1:5000/edit-pemilik/${pemilikId}`);
          if (response.data) {
            this.pemilik = response.data; 
          } else {
            this.notification.message = 'Pemilik tidak ditemukan';
            this.notification.type = 'alert-danger';
          }
        } catch (error) {
          this.notification.message = 'Gagal mengambil data pemilik';
          this.notification.type = 'alert-danger';
        }
      },
  
      async submitForm() {
        this.errors = {};

        if (!this.pemilik.nama) {
          this.errors.nama = 'Nama tidak boleh kosong';
        }
        if (!this.pemilik.email) {
          this.errors.email = 'Email tidak boleh kosong';
        } else if (!this.isValidEmail(this.pemilik.email)) {
          this.errors.email = 'Format email tidak valid';
        }
        if (!this.pemilik.no_telp) {
          this.errors.no_telp = 'Nomor telepon tidak boleh kosong';
        }
  
        if (Object.keys(this.errors).length > 0) {
          return;
        }

        try {
          await axios.put(`http://127.0.0.1:5000/edit-pemilik/${this.pemilik.id}`, this.pemilik);
  
      
          this.notification.message = 'Data Pemilik berhasil diperbarui!';
          this.notification.type = 'alert-success';
  
          setTimeout(() => {
            this.$router.push('/list-pemilik');
          }, 2000);
        } catch (error) {
          this.notification.message = 'Data gagal diperbarui!';
          this.notification.type = 'alert-danger';
          console.error(error);
        }
      },
  
      isValidEmail(email) {
        const regex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
        return regex.test(email);
      }
    }
  };
  </script>
  
  <style scoped>
  .notification {
    padding: 10px;
    margin-bottom: 15px;
    border-radius: 5px;
  }
  .alert-success {
    color: #155724;
    background-color: #d4edda;
    border-color: #c3e6cb;
  }
  .alert-danger {
    color: #721c24;
    background-color: #f8d7da;
    border-color: #f5c6cb;
  }
  .is-invalid {
    border-color: #e3342f;
  }
  .invalid-feedback {
    color: #e3342f;
    font-size: 0.875em;
  }
  </style>
  