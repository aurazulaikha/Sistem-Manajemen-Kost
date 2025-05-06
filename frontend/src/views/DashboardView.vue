<template>
  <div class="content">
    <div class="row">
      <div class="col-lg-3 col-md-6 col-sm-6"> 
        <div class="card card-stats">
          <div class="card-body">
            <div class="row">
              <div class="col-5 col-md-4">
                <div class="icon-big text-center icon-warning">
                  <i class="nc-icon nc-app text-warning"></i>
                </div>
              </div>
              <div class="col-7 col-md-8">
                <div class="numbers">
                  <p class="card-category">Capacity</p>
                  <p class="card-title">23</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-lg-3 col-md-6 col-sm-6">
        <div class="card card-stats">
          <div class="card-body">
            <div class="row">
              <div class="col-5 col-md-4">
                <div class="icon-big text-center icon-warning">
                  <i class="nc-icon nc-badge text-success"></i>
                </div>
              </div>
              <div class="col-7 col-md-8">
                <div class="numbers">
                  <p class="card-category">Penyewa</p>
                  <p class="card-title">{{ penyewaCount }}</p> <!-- Bind API data here -->
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-lg-3 col-md-6 col-sm-6">
        <div class="card card-stats">
          <div class="card-body">
            <div class="row">
              <div class="col-5 col-md-4">
                <div class="icon-big text-center icon-warning">
                  <i class="nc-icon nc-single-02 text-danger"></i>
                </div>
              </div>
              <div class="col-7 col-md-8">
                <div class="numbers">
                  <p class="card-category">Users</p>
                  <p class="card-title">{{ usersCount }}</p> 
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-lg-3 col-md-6 col-sm-6">
        <div class="card card-stats">
          <div class="card-body">
            <div class="row">
              <div class="col-5 col-md-4">
                <div class="icon-big text-center icon-warning">
                  <i class="nc-icon nc-money-coins text-primary"></i>
                </div>
              </div>
              <div class="col-7 col-md-8">
                <div class="numbers">
                  <p class="card-category">Keuntungan</p>
                  <p class="card-title">{{ totalKeuntungan }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="room-details">
      <div class="row mb-3">
        <div class="col-md-12">
          <img src="assets/img/kos.jpg" alt="Room Image" class="img-fluid rounded shadow">
        </div>
      </div>
      <div class="row mb-3">
        <div class="col-md-12">
          <div class="card" style="background-color: #ffffff;">
            <div class="card-body">
              <h4 class="informasi-kos-title">Informasi Kos</h4>
              <div class="border-line"></div>

              <!-- Room Information -->
              <div class="room-info">
                <!-- Harga Section -->
                <div class="section">
                  <h5>Harga</h5>
                  <ul>
                    <li><b>-</b> Satu unit kamar: <b>Rp. 2.000.000/3 bulan</b></li>
                    <li><b>-</b> Maksimal 1 unit kamar: 1 orang</li>
                    <li><b>-</b> Harga sudah termasuk biaya air dan listrik</li>
                    <li><b>-</b> Kost terdapat 2 lantai, lantai pertama terdapat 10 kamar dan lantai kedua terdapat 13 kamar</li>
                    <li><b>-</b> Diskon: - </li>
                  </ul>
                </div>

                <!-- Fasilitas Section -->
                <div class="section">
                  <h5>Fasilitas</h5>
                  <ul>
                    <li><b>-</b> Kerusakan lampu dan air ditanggung pemilik kos</li>
                    <li><b>-</b> Kamar mandi di dalam</li>
                    <li><b>-</b> Parkiran aman</li>
                    <li><b>-</b> Tidak menyediakan WIFI</li>
                  </ul>
                </div>

                <!-- Ketentuan Section -->
                <div class="section">
                  <h5>Ketentuan</h5>
                  <ul>
                    <li><b>-</b> Diharapkan dapat mengkonfirmasi pemilik kos maksimal 2 minggu sebelum pindah dari kos</li>
                    <li><b>-</b> Pulang maksimal penghuni kos adalah sampai jam 00.00 WIB</li>
                    <li><b>-</b> Tidak diperbolehkan memasang AC</li>
                    <li><b>-</b> Tidak diperbolehkan membawa teman lawan jenis yang tidak memiliki hubungan keluarga ke dalam lingkungan kos</li>
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
import axios from 'axios'; // Import axios for API calls

export default {
  name: 'RoomDetails',
  data() {
    return {
      penyewaCount: 0, // Store tenant count
      usersCount: 0, // Store user count
      totalKeuntungan: 0, // Store total profit
    };
  },
  mounted() {
    this.getPenyewaCount(); // Fetch tenant count on component mount
    this.getUsersCount(); // Fetch user count on component mount
    this.getTotalKeuntungan(); // Fetch total profit
  },
  methods: {
    async getPenyewaCount() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/kamar-aktif');
        if (response.data && response.data.data) {
          this.penyewaCount = response.data.data.jumlah_kamar;
        }
      } catch (error) {
        console.error('Error fetching penyewa count:', error);
      }
    },
    async getUsersCount() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/jumlah-users');
        if (response.data && response.data.data) {
          this.usersCount = response.data.data.jumlah_users;
        }
      } catch (error) {
        console.error('Error fetching users count:', error);
      }
    },
    async getTotalKeuntungan() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/total-keuntungan');
        if (response.data && response.data.total_keuntungan !== undefined) {
          this.totalKeuntungan = this.formatKeuntungan(response.data.total_keuntungan);
        }
      } catch (error) {
        console.error('Error fetching total keuntungan:', error);
      }
    },
    formatKeuntungan(amount) {
  const juta = amount / 1000000;
  return `Rp. ${juta.toFixed(2)} jt`; 
}

  },
};
</script>

<style scoped>
.room-details {
  margin-top: 30px;
}

.room-details img {
  max-width: 100%;
  border-radius: 15px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.room-details h4, .room-details h5 {
  color: #75276d;
  font-weight: bold;
}

.room-details p, .room-details ul {
  color: #75276d;
}

.room-info ul {
  list-style-type: none;
  padding-left: 0;
}

.room-info ul li {
  margin-bottom: 10px;
}

.room-info h5 {
  margin-top: 20px;
  font-size: 18px;
}

.card {
  border-radius: 15px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.card-body {
  padding: 20px;
}

.informasi-kos-title,
.alamat-title {
  color: #75276d;
  margin-bottom: 15px;
}

.border-line {
  border-bottom: 2px solid #75276d;
  margin-bottom: 20px;
}

.section {
  margin-bottom: 20px;
}

.section h5 {
  color: #75276d;
  font-size: 18px;
  margin-bottom: 10px;
}

.section ul {
  padding-left: 20px;
}

.section ul li {
  font-size: 16px;
  color: #75276d;
}

.alamat-link {
  color: #75276d;
  text-decoration: none;
}

.alamat-link:hover {
  text-decoration: underline;
}
</style>