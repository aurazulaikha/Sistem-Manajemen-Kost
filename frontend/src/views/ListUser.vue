<template>
  <div class="content">
    <div class="row">
      <div class="col-md-12">
        <div class="card">
          <div class="card-header d-flex justify-content-between">
            <h4 class="card-title">Daftar User</h4>
          </div>
          <div class="card-body">
            <div class="d-flex justify-content-between mb-3">
              <router-link to="/tambah-user">
                <button class="btn btn-purple btn-sm">Tambah Data</button>
              </router-link>
              <input 
                v-model="searchQuery" 
                type="text" 
                class="form-control" 
                placeholder="Cari user..." 
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
                    <th>Role</th>
                    <th>Phone</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(user, index) in paginatedUsers" :key="user.id">
                    <td>{{ (currentPage - 1) * perPage + (index + 1) }}</td>
                    <td>{{ user.nama }}</td>
                    <td>{{ user.email }}</td>
                    <td>{{ user.roles }}</td>
                    <td>{{ user.no_telp }}</td>
                    <td class="text-right">
                      <router-link :to="'/edit-user/' + user.id">
                        <button class="btn btn-warning btn-sm">Edit</button>
                      </router-link>
                      <button class="btn btn-danger btn-sm" @click="confirmDelete(user)">Hapus</button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            
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
            <p>Apakah Anda yakin ingin menghapus user <strong>{{ userToDelete.nama }}</strong>?</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeDeleteModal">Batal</button>
            <button type="button" class="btn btn-danger" @click="deleteUser">Hapus</button>
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
      api: 'http://127.0.0.1:5000/list-user',
      users: [],
      searchQuery: '',
      perPage: 5,
      currentPage: 1,
      showDeleteModal: false, 
      userToDelete: null,      
    };
  },
  created() {
    this.getUsers();
  },
  computed: {
    filteredUsers() {
      return this.users.filter(user => {
        const searchTerm = this.searchQuery.toLowerCase();
        return (
          (user.nama && user.nama.toLowerCase().includes(searchTerm)) ||
          (user.email && user.email.toLowerCase().includes(searchTerm)) ||
          (user.no_telp && user.no_telp.toLowerCase().includes(searchTerm)) ||
          (user.roles && user.roles.toLowerCase().includes(searchTerm))
        );
      });
    },
    totalPages() {
      return Math.ceil(this.filteredUsers.length / this.perPage);
    },
    paginatedUsers() {
      const start = (this.currentPage - 1) * this.perPage;
      const end = start + this.perPage;
      return this.filteredUsers.slice(start, end);
    }
  },
  methods: {
    getUsers() {
      axios.get(this.api)
        .then(response => {
          if (Array.isArray(response.data)) {
            this.users = response.data;
          } else {
            console.error('Data yang diterima tidak sesuai:', response.data);
          }
        })
        .catch(error => {
          console.error('Terjadi kesalahan:', error);
        });
    },
    confirmDelete(user) {
      console.log("User ID untuk dihapus:", user.id);  
      this.userToDelete = user;
      this.showDeleteModal = true;
    },
    closeDeleteModal() {
      console.log("Modal ditutup"); 
      this.showDeleteModal = false;
      this.userToDelete = null;
    },
    deleteUser() {
      if (this.userToDelete && this.userToDelete.id) {
        console.log("Menghapus user dengan ID:", this.userToDelete.id);  
        axios.delete(`http://127.0.0.1:5000/delete-user/${this.userToDelete.id}`)
          .then(response => {
            console.log('User berhasil dihapus:', response);
            this.getUsers();  
            this.closeDeleteModal();  
          })
          .catch(error => {
            console.error('Terjadi kesalahan saat menghapus user:', error);
          });
      } else {
        console.error('ID user tidak ditemukan');
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
