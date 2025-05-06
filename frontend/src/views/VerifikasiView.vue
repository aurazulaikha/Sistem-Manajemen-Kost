<template>
  <div class="content">
    <div class="row">
      <div class="col-md-12">
        <div class="card">
          <div class="card-header d-flex justify-content-between">
            <h4 class="card-title">Verifikasi</h4>
            <!-- Search Input -->
            <input 
              v-model="searchQuery" 
              type="text" 
              class="form-control" 
              placeholder="Cari verifikasi..." 
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
                    <th>No.Telp</th>
                    <th>Bukti Pembayaran</th>
                    <th>Awal Penyewaan</th>
                    <th>Akhir Penyewaan</th>
                    <th>No. Kamar</th>
                    <th>Status</th>
                    <th>Verifikasi</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(verifikasi, index) in paginatedVerifikasi" :key="verifikasi.id">
                    <td>{{ (currentPage - 1) * perPage + (index + 1) }}</td>
                    <td>{{ verifikasi.penyewa.nama }}</td>
                    <td>{{ verifikasi.penyewa.email }}</td>
                    <td>{{ verifikasi.penyewa.no_telp }}</td>
                    <td>
                      <template v-if="verifikasi.reservasi.bukti_pembayaran">
                        <img 
                          :src="`http://127.0.0.1:5000/uploads/${verifikasi.reservasi.bukti_pembayaran}`" 
                          alt="Bukti Pembayaran" 
                          width="100" 
                          height="auto" 
                        />
                        <br />
                        <a 
                          :href="`http://127.0.0.1:5000/uploads/${verifikasi.reservasi.bukti_pembayaran}`" 
                          download
                          class="btn btn-info btn-sm mt-2"
                        >
                          Download
                        </a>
                      </template>
                      <span v-else>N/A</span>
                    </td>
                    <td>{{ verifikasi.reservasi.awal_penyewaan }}</td>
                    <td>{{ verifikasi.reservasi.akhir_penyewaan }}</td>
                    <td>{{ verifikasi.kamar.nomor_kamar }}</td>
                    <td>{{ verifikasi.status_verifikasi }}</td>
                    <td class="text-right">
                      <button @click="updateVerifikasi(verifikasi.id, 'sudah verifikasi')" class="btn btn-success btn-sm">Terima</button>
                      <p></p>
                      <button @click="updateVerifikasi(verifikasi.id, 'verifikasi ditolak')" class="btn btn-danger btn-sm">Tolak</button>
                    </td>
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
import axios from 'axios';

export default {
data() {
  return {
    api: 'http://127.0.0.1:5000/list-verifikasi', // Endpoint API untuk mengambil data verifikasi
    verifikasiList: [],
    searchQuery: '',
    perPage: 5,
    currentPage: 1,
  };
},
created() {
  this.fetchVerifikasiList(); // Panggil fungsi untuk mengambil data saat komponen dibuat
},
computed: {
  filteredVerifikasi() {
    return this.verifikasiList.filter(verifikasi => {
      const searchTerm = this.searchQuery.toLowerCase();
      return (
        (verifikasi.penyewa.nama && verifikasi.penyewa.nama.toLowerCase().includes(searchTerm)) ||
        (verifikasi.penyewa.email && verifikasi.penyewa.email.toLowerCase().includes(searchTerm)) ||
        (verifikasi.penyewa.no_telp && verifikasi.penyewa.no_telp.toLowerCase().includes(searchTerm)) ||
        (verifikasi.kamar.nomor_kamar && verifikasi.kamar.nomor_kamar.toLowerCase().includes(searchTerm)) ||
        (verifikasi.status_verifikasi  && verifikasi.status_verifikasi.toLowerCase().includes(searchTerm))
      );
    });
  },
  totalPages() {
    return Math.ceil(this.filteredVerifikasi.length / this.perPage);
  },
  paginatedVerifikasi() {
    const start = (this.currentPage - 1) * this.perPage;
    const end = start + this.perPage;
    return this.filteredVerifikasi.slice(start, end);
  }
},  
methods: {
  fetchVerifikasiList() {
    axios.get(this.api)
      .then(response => {
        this.verifikasiList = response.data;
      })
      .catch(error => {
        console.error('Error fetching verifikasi data:', error);
      });
  },
  updateVerifikasi(id, status) {
    axios.put(`http://127.0.0.1:5000/verifikasi/${id}`, { status_verifikasi: status })
      .then(() => {
        this.fetchVerifikasiList(); // Refresh data setelah update status
        alert('Status verifikasi berhasil diperbarui');
      })
      .catch(error => {
        console.error('Error updating verifikasi status:', error);
        alert('Gagal memperbarui status verifikasi');
      });
  },
  previousPage() {
    if (this.currentPage > 1) {
      this.currentPage--;
    }
  },
  nextPage() {
    if (this.currentPage < this.totalPages) {
      this.currentPage++;
    }
  }
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

.btn-success {
background-color: #28a745;
}

.btn-warning {
background-color: #ffc107;
}

.btn-danger {
background-color: #dc3545;
}

.pagination-container {
font-size: 14px;
}
</style>
