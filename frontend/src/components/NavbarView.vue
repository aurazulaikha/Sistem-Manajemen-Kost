<template>
  <nav class="navbar navbar-expand-lg navbar-absolute fixed-top navbar-transparent">
    <div class="container-fluid">
      <div class="navbar-wrapper">
        <div class="navbar-toggle">
          <button type="button" class="navbar-toggler">
            <span class="navbar-toggler-bar bar1"></span>
            <span class="navbar-toggler-bar bar2"></span>
            <span class="navbar-toggler-bar bar3"></span>
          </button>
        </div>
        <a class="navbar-brand" href="javascript:;">Sistem Manajemen Kost</a>
      </div>
      <button
        class="navbar-toggler"
        type="button"
        data-toggle="collapse"
        data-target="#navigation"
        aria-controls="navigation-index"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-bar navbar-kebab"></span>
        <span class="navbar-toggler-bar navbar-kebab"></span>
        <span class="navbar-toggler-bar navbar-kebab"></span>
      </button>
      <div class="collapse navbar-collapse justify-content-end" id="navigation">
        <div class="profile-icon ml-3">
          <router-link to="/profile" exact-active-class="active">
            <i class="nc-icon nc-single-02 profile-icon-style"></i>
          </router-link>
        </div>
        <div class="ml-3">
          <button class="btn btn-logout btn-sm" @click="logout">Logout</button>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import axios from 'axios';

export default {
  methods: {
    logout() {
      // Kirim permintaan POST ke API Flask untuk logout
      axios.post('http://127.0.0.1:5000/logout')  // Sesuaikan dengan URL API Anda
        .then(response => {
          console.log(response.data.message);  // Response dari server
          
          // Hapus token JWT dari localStorage atau tempat penyimpanan lainnya
          localStorage.removeItem('token');
          sessionStorage.removeItem('token');  // Jika menggunakan sessionStorage
          
          // Arahkan ke halaman login setelah logout
          this.$router.push('/');
        })
        .catch(error => {
          console.error("Logout failed:", error);
          alert('Terjadi kesalahan saat logout');
        });
    }
  }
}
</script>

<style scoped>
/* Menambahkan ukuran, ketebalan, dan warna ungu pada ikon profil */
.profile-icon-style {
  font-size: 1.50rem; /* Membuat ikon sedikit lebih besar */
  font-weight: bold; /* Membuat ikon lebih tebal */
  color: #75276d; /* Warna ungu */
}

.profile-icon-style:hover {
  color: #c20ab0; /* Warna saat ikon profil di-hover */
}

/* Styling untuk tombol logout dengan warna ungu */
.btn-logout {
  background-color: #75276d; /* Warna ungu */
  color: white;
}

.btn-logout:hover {
  background-color: #5e1d57; /* Efek hover lebih gelap */
}

.btn-sm {
  margin: 0 5px;
}
</style>
