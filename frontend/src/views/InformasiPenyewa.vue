<template>
    <div class="content">
      <div class="room-details">
        <div class="row mb-3">
          <div class="col-md-12">
            <div class="card alamat-card">
              <!-- Header -->
              <div class="card-header alamat-header">
                <h4 class="text-white">Informasi Penyewa</h4>
              </div>
            </div>
          </div>
        </div>
        <div class="row mb-3">
          <div class="col-md-12">
            <div class="card informasi-card">
              <div class="card-body">
                <div class="row">
                  <!-- Detail Penyewa -->
                  <div class="col-md-6">
                    <h5 class="section-title">Detail Penyewa</h5>
                    <ul class="details-list">
                      <li><b>Nama : </b> {{ penyewa.nama }}</li>
                      <li><b>Email : </b> {{ penyewa.email }}</li>
                      <li><b>Telp : </b> {{ penyewa.no_telp }}</li>
                      <li><b>Nomor Kamar : </b> {{ penyewa.nomor_kamar }}</li>
                    </ul>
                  </div>
                  <!-- Status -->
                  <div class="col-md-6">
                    <h5 class="section-title">Status</h5>
                    <ul class="details-list">
                      <li><b>Status Penyewa : </b> {{ penyewa.status_penyewa }}</li>
                      <li><b>Status Verifikasi : </b> {{ penyewa.status_verifikasi }}</li>
                    </ul>
                  </div>
                </div>
  
                <!-- Periode Penyewaan -->
                <div v-if="penyewa.awal_penyewaan && penyewa.akhir_penyewaan" class="row mt-4">
                  <div class="col-md-12">
                    <h5 class="section-title text-purple">Periode Penyewaan</h5>
                    <ul class="details-list">
                      <li><b>Awal Sewa : </b> {{ penyewa.awal_penyewaan }}</li>
                      <li><b>Akhir Sewa : </b> {{ penyewa.akhir_penyewaan }}</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    data() {
      return {
        penyewa: {},
        loading: true,
      };
    },
    created() {
      this.fetchPenyewaInfo();
    },
    methods: {
      async fetchPenyewaInfo() {
        const token = localStorage.getItem("token"); // Assuming token is stored in localStorage
        if (!token) {
          alert("Anda belum login.");
          this.$router.push("/login"); // Redirect to login page
          return;
        }
  
        try {
          const response = await axios.get("http://127.0.0.1:5000/informasi-penyewa", {
            headers: {
              Authorization: token,
            },
          });
  
          this.penyewa = response.data;
        } catch (error) {
          console.error(error);
          alert("Gagal memuat informasi penyewa.");
        } finally {
          this.loading = false;
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .room-details {
    margin-top: 30px;
  }
  
  /* Informasi Penyewa Card Styling */
  .informasi-card {
    background-color: #ffffff; /* Purple background for the card body */
    color: white; /* White text color */
    border-radius: 15px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  }
  
  .informasi-header {
    background-color: #ffffff; /* Purple background for the header */
    padding: 15px;
    border-top-left-radius: 15px;
    border-top-right-radius: 15px;
  }
  
  .informasi-header h4 {
    margin: 0;
    font-size: 20px;
    font-weight: bold;
  }
  
  /* Section Titles */
  .section-title {
    color: #75276d; /* White color for the section titles */
    font-size: 18px;
    margin-bottom: 10px;
    font-weight: bold;
  }
  
  /* Periode Section Title */
  .text-purple {
    color: #75276d;;
  }
  
  /* List Styling */
  .details-list {
    list-style-type: none;
    padding-left: 0;
  }
  
  .details-list li {
    font-size: 16px;
    color: #919191; /* Light grey color for list items */
    margin-bottom: 8px;
  }
  
  /* Alamat Card Styling */
  .alamat-card {
    background-color:  #75276d;
    border-radius: 15px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }
  
  .alamat-header {
    background-color: #75276d; /* Purple background for the alamat header */
    padding: 15px;
    border-top-left-radius: 15px;
    border-top-right-radius: 15px;
  }
  
  .alamat-header h4 {
    margin: 0;
    font-size: 20px;
    font-weight: bold;
  }
  
  .alamat-link {
    color: #75276d;
    text-decoration: none;
  }
  
  .alamat-link:hover {
    text-decoration: underline;
  }
  
  .border-line {
    border-bottom: 2px solid #75276d;
    margin-bottom: 20px;
  }
  </style>
  