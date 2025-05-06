<template>
  <div class="content">
    <div class="row">
      <div class="col-md-12">
        <div class="card">
          <div class="card-header d-flex justify-content-between">
            <h4 class="card-title">Daftar Pengeluaran</h4>
          </div>
          <div class="card-body">
            <!-- Button Tambah Pengeluaran dan Search bar -->
            <div class="d-flex justify-content-between align-items-center mb-3">
              <!-- Tombol Tambah Pengeluaran -->
              <router-link 
                to="/tambah-pengeluaran" 
                class="btn btn-purple"
              >
                Tambah Pengeluaran
              </router-link>
  
              <!-- Search bar -->
              <input 
                v-model="searchQuery" 
                type="text" 
                class="form-control" 
                placeholder="Cari keterangan atau tanggal..." 
                style="width: 250px;" 
              />
            </div>
            
            <!-- Total Pengeluaran -->
            <h6 class="total-pengeluaran mb-3">Total Pengeluaran: {{ formatCurrency(totalPengeluaran) }}</h6>
            
            <div class="table-responsive">
              <table class="table">
                <thead class="text-primary">
                  <tr>
                    <th>Item</th>
                    <th>Tanggal</th>
                    <th>Jumlah Pengeluaran</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(data, index) in paginatedPengeluaran" :key="index">
                    <td>{{ data.keterangan }}</td>
                    <td>{{ data.tanggal }}</td>
                    <td>{{ formatCurrency(data.jumlah_pengeluaran) }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
            
            <!-- Pagination -->
            <div class="pagination-container d-flex justify-content-between mt-3">
              <span>Halaman {{ currentPage }} dari {{ totalPages }}</span>
              <div class="pagination-buttons d-flex justify-content-end">
                <button 
                  class="btn btn-purple btn-sm" 
                  :disabled="currentPage === 1" 
                  @click="previousPage"
                >
                  Previous
                </button>
                <button 
                  class="btn btn-purple btn-sm" 
                  :disabled="currentPage === totalPages" 
                  @click="nextPage"
                >
                  Next
                </button>
              </div>
            </div>
          </div>
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
      api: 'http://127.0.0.1:5000/pengeluaran', // API endpoint
      pengeluaranData: [], // Data pengeluaran
      searchQuery: '',  // Query pencarian
      perPage: 5,  // Jumlah data per halaman
      currentPage: 1,  // Halaman saat ini
      totalPengeluaran: 0, // Total pengeluaran keseluruhan
    };
  },
  created() {
    this.getPengeluaranData(); // Mengambil data pengeluaran saat komponen dibuat
  },
  computed: {
    // Filter data berdasarkan query pencarian
    filteredPengeluaran() {
      return this.pengeluaranData.filter(data => {
        const searchTerm = this.searchQuery.toLowerCase();
        const keterangan = data.keterangan ? data.keterangan.toLowerCase() : '';
        const tanggal = data.tanggal ? data.tanggal.toLowerCase() : '';
        return (
          keterangan.includes(searchTerm) || 
          tanggal.includes(searchTerm)
        );
      });
    },
    // Total halaman untuk paginasi
    totalPages() {
      return Math.ceil(this.filteredPengeluaran.length / this.perPage);
    },
    // Data yang akan ditampilkan pada halaman saat ini
    paginatedPengeluaran() {
      const start = (this.currentPage - 1) * this.perPage;
      const end = start + this.perPage;
      return this.filteredPengeluaran.slice(start, end);
    }
  },
  methods: {
    // Fungsi untuk mengambil data dari API
    getPengeluaranData() {
      axios.get(this.api)
        .then(response => {
          if (response.data && response.data.data) {
            this.pengeluaranData = response.data.data; // Ambil data pengeluaran
            this.totalPengeluaran = this.pengeluaranData.reduce((total, item) => total + item.jumlah_pengeluaran, 0); // Hitung total pengeluaran
          } else {
            console.error('Data tidak sesuai:', response.data);
          }
        })
        .catch(error => {
          console.error('Terjadi kesalahan:', error);
        });
    },
    // Fungsi untuk format uang (contoh: 1000000 -> Rp 1.000.000)
    formatCurrency(amount) {
      return 'Rp ' + amount.toLocaleString();
    },
    // Fungsi untuk ke halaman sebelumnya
    previousPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
      }
    },
    // Fungsi untuk ke halaman selanjutnya
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
      }
    }
  }
};
</script>

<style scoped>
.total-pengeluaran {
  color: #75276d; /* Warna ungu */
}

.table th, .table td {
  text-align: center;
}

.table th {
  background-color: #f8f9fa;
}

.btn-sm {
  margin: 0 5px;
}

.btn-purple {
  background-color: #75276d;
  color: white;
}

.btn-purple:hover {
  background-color: #5e1d57;
}

.pagination-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.pagination-buttons {
  display: flex;
  gap: 10px;
}

.btn-purple {
  background-color: #75276d;
  color: white;
}

.btn-purple:hover {
  background-color: #5e1d57;
}
</style>
