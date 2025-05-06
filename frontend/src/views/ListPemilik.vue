<template>
  <div class="content">
    <div class="row">
      <div class="col-md-12">
        <div class="card">
          <div class="card-header d-flex justify-content-between">
            <h4 class="card-title">Daftar Pemilik</h4>
          </div>
          <div class="card-body">
            <div class="d-flex justify-content-between mb-3">
              <router-link to="/tambah-pemilik">
                <button class="btn btn-purple btn-sm">Tambah Data</button>
              </router-link>
              <input 
                v-model="searchQuery" 
                type="text" 
                class="form-control" 
                placeholder="Cari pemilik..." 
                style="width: 250px;" 
              />
            </div>
            <div class="table-responsive">
              <table class="table">
                <thead class="text-primary">
                  <tr>
                    <th>No</th>
                    <th>Nama</th>
                    <th>Email</th>
                    <th>Phone</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(pemilik, index) in paginatedPemilik" :key="pemilik.id">
                    <td>{{ (currentPage - 1) * perPage + (index + 1) }}</td>
                    <td>{{ pemilik.nama }}</td>
                    <td>{{ pemilik.email }}</td>
                    <td>{{ pemilik.no_telp }}</td>
                    <td class="text-right">
                      <router-link :to="'/edit-pemilik/' + pemilik.id">
                        <button class="btn btn-warning btn-sm">Edit</button>
                      </router-link>
                      <button class="btn btn-danger btn-sm" @click="confirmDelete(pemilik)">Hapus</button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            
            <!-- Paginasi -->
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

    <div v-if="showDeleteModal" class="modal fade show" tabindex="-1" style="display: block;" aria-modal="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Konfirmasi Penghapusan</h5>
            <button type="button" class="close" @click="closeDeleteModal">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <p>Apakah Anda yakin ingin menghapus pemilik <strong>{{ pemilikToDelete.nama }}</strong>?</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeDeleteModal">Batal</button>
            <button type="button" class="btn btn-danger" @click="deletePemilik">Hapus</button>
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
      api: 'http://127.0.0.1:5000/list-pemilik', 
      pemilik: [], 
      searchQuery: '',  
      perPage: 5, 
      currentPage: 1,  
      showDeleteModal: false,  
      pemilikToDelete: null, 
    };
  },
  created() {
    this.getPemilik();  
  },
  computed: {
    filteredPemilik() {
      return this.pemilik.filter(pemilik => {
        const searchTerm = this.searchQuery.toLowerCase();
        return (
          (pemilik.nama && pemilik.nama.toLowerCase().includes(searchTerm)) ||
          (pemilik.email && pemilik.email.toLowerCase().includes(searchTerm)) ||
          (pemilik.no_telp && pemilik.no_telp.toLowerCase().includes(searchTerm))
        );
      });
    },
    totalPages() {
      return Math.ceil(this.filteredPemilik.length / this.perPage);  
    },
    paginatedPemilik() {
      const start = (this.currentPage - 1) * this.perPage;
      const end = start + this.perPage;
      return this.filteredPemilik.slice(start, end);  
    }
  },
  methods: {
    getPemilik() {
      axios.get(this.api)
        .then(response => {
          if (Array.isArray(response.data)) {
            this.pemilik = response.data; 
          } else {
            console.error('Data yang diterima tidak sesuai:', response.data);
          }
        })
        .catch(error => {
          console.error('Terjadi kesalahan:', error); 
        });
    },
    confirmDelete(pemilik) {
      this.pemilikToDelete = pemilik;  
      this.showDeleteModal = true;  
    },
    closeDeleteModal() {
      this.showDeleteModal = false; 
      this.pemilikToDelete = null;  
    },
    deletePemilik() {
      if (this.pemilikToDelete && this.pemilikToDelete.id) {
        axios.delete(`http://127.0.0.1:5000/delete-pemilik/${this.pemilikToDelete.id}`)
          .then(response => {
            console.log('Pemilik berhasil dihapus:', response);
            this.getPemilik();  
            this.closeDeleteModal();  
          })
          .catch(error => {
            console.error('Terjadi kesalahan saat menghapus pemilik:', error);
          });
      } else {
        console.error('ID pemilik tidak ditemukan');
      }
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
}
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
