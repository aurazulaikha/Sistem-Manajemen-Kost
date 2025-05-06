<template>
<div class="content">
    <div class="col-md-6 mx-auto">
    <div class="card card-user">
        <div class="card-header">
        <h5 class="card-title">Tambah Pengeluaran</h5>
        </div>
        <div class="card-body">
        <form @submit.prevent="submitPengeluaran">
            <div class="form-group">
            <label>Keterangan</label>
            <input 
                type="text" 
                class="form-control" 
                v-model="formData.keterangan" 
                placeholder="Masukkan keterangan pengeluaran"
                required 
            />
            </div>
            <div class="form-group">
            <label>Jumlah Pengeluaran</label>
            <input 
                type="number" 
                class="form-control" 
                v-model="formData.jumlah_pengeluaran" 
                placeholder="Masukkan jumlah pengeluaran" 
                required 
                min="1"
            />
            </div>
            <div class="form-group">
            <label>Tanggal</label>
            <input 
                type="date" 
                class="form-control" 
                v-model="formData.tanggal" 
                required 
            />
            </div>
            <button type="submit" class="btn btn-purple btn-block">Tambah</button>
        </form>
        <div v-if="notification.message" :class="['notification', notification.type]">
            {{ notification.message }}
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
        formData: {
        keterangan: "",
        jumlah_pengeluaran: null,
        tanggal: "",
        },
        notification: { message: "", type: "" },
    };
    },
    methods: {
    async submitPengeluaran() {
        try {
        const response = await axios.post("http://127.0.0.1:5000/tambah-pengeluaran", this.formData);
        if (response.status === 201) {
            this.notification = { message: response.data.message, type: "success" };
            this.resetForm();
        }
        } catch (error) {
        this.notification = { message: error.response?.data?.error || "Terjadi kesalahan.", type: "error" };
        }
    },
    resetForm() {
        this.formData = { keterangan: "", jumlah_pengeluaran: null, tanggal: "" };
    },
    },
};
</script>

<style scoped>
.notification {
    margin-top: 15px;
    padding: 10px;
    border-radius: 5px;
    text-align: center;
}

.notification.success {
    background-color: #d4edda;
    color: #155724;
}

.notification.error {
    background-color: #f8d7da;
    color: #721c24;
}

.card {
    margin-top: 50px;
}

button {
    width: 100%;
}

/* Tambahkan gaya untuk tombol ungu */
.btn-purple {
    background-color: #75276d;
    color: white;
    border: none;
}

.btn-purple:hover {
    background-color: #5e1d57;
    color: white;
}
</style>
