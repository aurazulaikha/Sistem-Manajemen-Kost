<template>
  <div class="content">
    <div class="row">
      <div class="col-md-12">
        <div class="card">
          <div class="card-header d-flex justify-content-between">
            <h4 class="card-title">Status Penyewa</h4>
            <!-- Search Input -->
            <input 
              v-model="searchQuery" 
              type="text" 
              class="form-control" 
              placeholder="Cari penyewa..." 
              style="width: 250px;" 
            />
          </div>
          <div class="card-body">
            <div class="table-responsive">
              <table class="table">
                <thead class="text-primary">
                  <tr>
                    <th>No</th>
                    <th>Nama</th>
                    <th>Email</th>
                    <th>Phone</th>
                    <th>Awal Penyewaan</th>
                    <th>Akhir Penyewaan</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(user, index) in paginatedUsers" :key="index">
                    <td>{{ (currentPage - 1) * perPage + (index + 1) }}</td>
                    <td>{{ user.nama }}</td>
                    <td>{{ user.email }}</td>
                    <td>{{ user.no_telp }}</td>
                    <td>{{ user.awal_penyewaan }}</td>
                    <td>{{ user.akhir_penyewaan }}</td>
                    <td>{{ user.status }}</td>
                  </tr>
                  <!-- Tampilkan pesan jika data tidak ditemukan -->
                  <tr v-if="filteredUsers.length === 0">
                    <td colspan="7">Tidak ada data yang sesuai.</td>
                  </tr>
                </tbody>
              </table>
            </div>
            
            <!-- Pagination Controls -->
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
export default {
  data() {
    return {
      users: [], // Data penyewa dari API
      searchQuery: '', // Input pencarian
      perPage: 5, // Jumlah data per halaman
      currentPage: 1, // Halaman aktif
    };
  },
  computed: {
    // Filter data berdasarkan input pencarian
    filteredUsers() {
      return this.users.filter(user => {
        const searchTerm = this.searchQuery.toLowerCase();
        return (
          (user.nama && user.nama.toLowerCase().includes(searchTerm)) ||
          (user.email && user.email.toLowerCase().includes(searchTerm)) ||
          (user.no_telp && user.no_telp.includes(this.searchQuery)) ||
          (user.status && user.status.toLowerCase().includes(searchTerm))
        );
      });
    },
    // Total halaman berdasarkan hasil filter
    totalPages() {
      return Math.ceil(this.filteredUsers.length / this.perPage);
    },
    // Data yang akan ditampilkan pada halaman tertentu
    paginatedUsers() {
      const start = (this.currentPage - 1) * this.perPage;
      const end = start + this.perPage;
      return this.filteredUsers.slice(start, end);
    }
  },
  methods: {
    // Mengambil data dari API
    fetchStatusPenyewa() {
      fetch('http://127.0.0.1:5000/status-penyewa')
        .then(response => {
          if (!response.ok) {
            throw new Error('Gagal mengambil data dari API');
          }
          return response.json();
        })
        .then(data => {
          this.users = data; // Isi data ke `users`
        })
        .catch(error => {
          console.error('Error:', error);
        });
    },
    // Navigasi ke halaman sebelumnya
    previousPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
      }
    },
    // Navigasi ke halaman berikutnya
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
      }
    }
  },
  mounted() {
    this.fetchStatusPenyewa(); // Ambil data saat komponen dimuat
  }
};
</script>

<style scoped>
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
</style>
