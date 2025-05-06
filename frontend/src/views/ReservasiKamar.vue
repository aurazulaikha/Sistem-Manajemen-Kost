<template>
  <div class="content">
    <div class="col-md-8">
      <div class="card card-user">
        <div class="card-header">
          <h5 class="card-title">Form Reservasi Kamar</h5>
        </div>
        <div class="card-body">
          <!-- Form Reservasi -->
          <form @submit.prevent="submitReservasi">
            <div class="form-group">
              <label>Nama</label>
              <input type="text" class="form-control" v-model="formData.nama" required />
            </div>

            <div class="form-group">
              <label>Email</label>
              <input type="email" class="form-control" v-model="formData.email" required />
            </div>

            <div class="form-group">
              <label>Nomor Kamar</label>
              <select class="form-control" v-model="formData.kamar_id" required>
                <option value="" disabled>Pilih Nomor Kamar</option>
                <option v-for="kamar in kamarTersedia" :key="kamar.id" :value="kamar.id">
                  {{ kamar.nomor_kamar }}
                </option>
              </select>
            </div>

            <div class="form-group">
              <label>Periode Penyewaan (per 3 Bulan)</label>
              <input type="number" class="form-control" v-model="formData.periode_penyewaan" @input="updateJumlahHarga" required min="1" />
            </div>

            <div class="form-group">
              <label>Awal Penyewaan</label>
              <input type="date" class="form-control" v-model="formData.awal_penyewaan" @input="updateAkhirPenyewaan" required />
            </div>

            <!-- Hapus field akhir_penyewaan -->
            <!-- <div class="form-group">
              <label>Akhir Penyewaan</label>
              <input type="date" class="form-control" v-model="formData.akhir_penyewaan" disabled />
            </div> -->

            <div class="form-group">
              <label>Bukti Pembayaran</label>
              <input type="file" class="form-control" @change="handleFileUpload" required />
              <!-- Tampilkan keterangan file yang diupload atau pesan jika belum diupload -->
              <p v-if="formData.bukti_pembayaran">
                File yang diupload: {{ formData.bukti_pembayaran.name }}
              </p>
              <p v-else>Belum ada file yang diupload.</p>
            </div>

            <div class="form-group">
              <label>Jumlah Harga</label>
              <input type="number" class="form-control" v-model="formData.jumlah_harga" disabled />
            </div>

            <!-- Button Kirim Reservasi -->
            <button type="submit" class="btn" :style="{ backgroundColor: '#75276d', color: '#fff' }">Kirim Reservasi</button>
          </form>
          
          <!-- Notifikasi -->
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
        nama: "",
        email: "",
        kamar_id: "",
        periode_penyewaan: 1,
        awal_penyewaan: "",
        akhir_penyewaan: "",
        jumlah_harga: 2000000,
        bukti_pembayaran: null,
      },
      kamarTersedia: [],
      notification: { message: "", type: "" },
    };
  },
  methods: {
    // Mengambil data kamar yang tersedia dari backend
    async fetchKamarTersedia() {
      try {
        const response = await axios.get("http://127.0.0.1:5000/available_rooms");
        this.kamarTersedia = response.data.rooms;  // Pastikan API mengembalikan data yang tepat
      } catch (error) {
        this.notification = { message: "Gagal memuat data kamar.", type: "error" };
      }
    },

    // Mengupdate harga berdasarkan periode penyewaan
    updateJumlahHarga() {
      this.formData.jumlah_harga = this.formData.periode_penyewaan * 2000000;
    },

    // Menghitung akhir penyewaan berdasarkan awal penyewaan
    updateAkhirPenyewaan() {
      const awal = new Date(this.formData.awal_penyewaan);
      const akhir = new Date(awal);
      akhir.setMonth(awal.getMonth() + parseInt(this.formData.periode_penyewaan, 10));
      this.formData.akhir_penyewaan = akhir.toISOString().split("T")[0];
    },

    // Menangani file upload bukti pembayaran
    handleFileUpload(event) {
      this.formData.bukti_pembayaran = event.target.files[0];
    },

    // Mengirim data reservasi ke backend
    async submitReservasi() {
      // Membuat FormData untuk mengirim file
      const formDataToSend = new FormData();
      formDataToSend.append('nama', this.formData.nama);
      formDataToSend.append('email', this.formData.email);
      formDataToSend.append('kamar_id', this.formData.kamar_id);
      formDataToSend.append('periode_penyewaan', this.formData.periode_penyewaan);
      formDataToSend.append('awal_penyewaan', this.formData.awal_penyewaan);
      formDataToSend.append('bukti_pembayaran', this.formData.bukti_pembayaran);

      try {
  const response = await axios.post("http://127.0.0.1:5000/reservasi", formDataToSend, { headers: { "Content-Type": "multipart/form-data" } });
  if (response.data && response.data.message) {
    this.notification = { message: response.data.message, type: "success" };
  } else {
    this.notification = { message: "Response tidak sesuai.", type: "error" };
  }
} catch (error) {
  console.error("Error:", error);
  this.notification = { message: error.response?.data?.error || "Terjadi kesalahan.", type: "error" };
}

    },
  },
  mounted() {
    // Mengambil data kamar yang tersedia saat komponen dimuat
    this.fetchKamarTersedia();
  },
};
</script>

<style scoped>
/* Styling untuk notifikasi sukses dan error */
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

/* Styling untuk form input */
.form-group {
  margin-bottom: 15px;
}

input[type="file"] {
  padding: 10px;
}

/* Button styling */
button {
  margin-top: 15px;
  width: 100%;
}
</style>
