<template>
  <div class="content">
    <div class="row">
      <div class="col-md-12">
        <div class="card">
          <div class="card-header d-flex justify-content-between">
            <h4 class="card-title">Financial</h4>
          </div>
          <div class="card-body">
            <!-- Search bar dan Total Pendapatan disusun sejajar -->
            <div class="d-flex justify-content-between align-items-center mb-3">
              <!-- Total Pendapatan -->
              <h6 class="total-pendapatan">Total Keuntungan: {{ formatCurrency(totalKeuntungan) }}</h6>

              <!-- Search bar -->
              <input 
                v-model="searchQuery" 
                type="text" 
                class="form-control" 
                placeholder="Cari tahun..." 
                style="width: 250px;" 
              />
            </div>

            <div class="table-responsive">
              <table class="table">
                <thead class="text-primary">
                  <tr>
                    <th>Tahun</th>
                    <th>Pendapatan</th>
                    <th>Pengeluaran</th>
                    <th>Keuntungan</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(data, index) in paginatedFinancialData" :key="index">
                    <td>{{ data.tahun }}</td>
                    <td>{{ formatCurrency(data.total_pendapatan) }}</td>
                    <td>{{ formatCurrency(data.total_pengeluaran) }}</td>
                    <td>{{ formatCurrency(data.keuntungan) }}</td>
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
      api: 'http://127.0.0.1:5000/financial', // API endpoint
      financialData: [], // Data keuangan per tahun
      searchQuery: '',  // Query pencarian
      perPage: 5,  // Jumlah data per halaman
      currentPage: 1,  // Halaman saat ini
      totalKeuntungan: 0, // Total keuntungan keseluruhan
    };
  },
  created() {
    this.getFinancialData(); // Mengambil data keuangan saat komponen dibuat
  },
  computed: {
    // Filter data berdasarkan query pencarian
    filteredFinancialData() {
      return this.financialData.filter(data => {
        const searchTerm = this.searchQuery.toLowerCase();
        // Pastikan data.tahun adalah string sebelum melakukan toLowerCase
        const tahun = data.tahun ? data.tahun.toString().toLowerCase() : '';
        return (
          tahun.includes(searchTerm) || 
          data.total_pendapatan.toString().includes(searchTerm) ||
          data.total_pengeluaran.toString().includes(searchTerm) ||
          data.keuntungan.toString().includes(searchTerm)
        );
      });
    },
    // Total halaman untuk paginasi
    totalPages() {
      return Math.ceil(this.filteredFinancialData.length / this.perPage);
    },
    // Data yang akan ditampilkan pada halaman saat ini
    paginatedFinancialData() {
      const start = (this.currentPage - 1) * this.perPage;
      const end = start + this.perPage;
      return this.filteredFinancialData.slice(start, end);
    }
  },
  methods: {
    // Fungsi untuk mengambil data dari API
    getFinancialData() {
      axios.get(this.api)
        .then(response => {
          if (Array.isArray(response.data)) {
            this.financialData = response.data.filter(item => item.tahun !== 'Total'); // Ambil semua data tahun
            const totalData = response.data.find(item => item.tahun === 'Total');
            this.totalKeuntungan = totalData ? totalData.keuntungan : 0; // Ambil total keuntungan keseluruhan
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
}
</script>

<style scoped>
.total-pendapatan {
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

.btn-warning {
  background-color: #ffc107;
}

.btn-danger {
  background-color: #dc3545;
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

.modal-backdrop {
  z-index: 1040;
}
</style>
