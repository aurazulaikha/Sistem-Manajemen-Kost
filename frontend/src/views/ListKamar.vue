<template>
  <div class="kamar-container">
    <div class="keterangan-warna">
      <h5><b>Keterangan</b></h5>
      <p><span class="warna-hijau"></span> Kamar yang tersedia</p>
      <p><span class="warna-kuning"></span> Dalam proses verifikasi</p>
      <p><span class="warna-merah"></span> Masa sewa akan habis</p>
      <p><span class="warna-abu"></span> Kamar yang terisi</p>
    </div>
    
    <!-- Lantai 1 -->
    <div v-if="kamarList.length > 0">
      <h2>Lantai 1</h2>
      <div class="kamar-row">
        <div v-for="kamar in kamarList.filter(k => k.nomor_kamar <= 10).sort((a, b) => a.nomor_kamar - b.nomor_kamar)" :key="kamar.id" 
             class="kamar-card"
             :style="getKamarStyle(kamar.status_kamar)"
             @click="showDetail(kamar)">
          <div class="kamar-item">
            <div class="nomor-kamar" :style="getNomorKamarStyle(kamar.status_kamar)">{{ kamar.nomor_kamar }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Lantai 2 -->
    <div v-if="kamarList.length > 0">
      <h2>Lantai 2</h2>
      <div class="kamar-row">
        <div v-for="kamar in kamarList.filter(k => k.nomor_kamar > 10).sort((a, b) => a.nomor_kamar - b.nomor_kamar)" :key="kamar.id" 
             class="kamar-card"
             :style="getKamarStyle(kamar.status_kamar)"
             @click="showDetail(kamar)">
          <div class="kamar-item">
            <div class="nomor-kamar" :style="getNomorKamarStyle(kamar.status_kamar)">{{ kamar.nomor_kamar }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Detail Kamar -->
    <div v-if="showModal" class="modal" @click.self="closeModal">
      <div class="modal-content">
        <h3>Detail Kamar</h3>
        <p><strong>Nomor Kamar : </strong> {{ selectedKamar.nomor_kamar }}</p>
        <p><strong>Status Kamar : </strong> {{ selectedKamar.status_kamar }}</p>
        <p><strong>Nama Penyewa : </strong> {{ selectedKamar.nama }}</p>
        <button @click="closeModal">Tutup</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      kamarList: [],         // Array to store list of rooms
      selectedKamar: null,   // To store selected room details
      showModal: false       // To control the visibility of the modal
    };
  },
  created() {
    this.fetchKamarList();  // Fetch list of rooms when the component is created
  },
  methods: {
    async fetchKamarList() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/list-kamar');
        this.kamarList = response.data;  // Store fetched rooms into kamarList
        console.log(this.kamarList);  // Debugging: Ensure the data is correct
      } catch (error) {
        console.error('Error fetching kamar list:', error);
      }
    },
    getKamarStyle(status) {
      const statusLower = status.toLowerCase();  // Convert to lowercase to ensure matching

      // Define styles based on status_kamar
      if (statusLower === 'tersedia') {
        return { backgroundColor: '#8BC34A' };  // Soft Green for available rooms
      } else if (statusLower === 'terisi') {
        return { backgroundColor: '#B0BEC5' };  // Soft Gray for occupied rooms
      } else if (statusLower === 'masa sewa akan habis') {
        return { backgroundColor: '#D30000' };  // Red for rooms with expiring lease
      } else if (statusLower === 'proses verifikasi') {
        return { backgroundColor: '#FFEB3B' };  // Yellow for rooms under verification
      }
      return { backgroundColor: '#E0E0E0' };  // Default case (soft gray)
    },
    getNomorKamarStyle(status) {
      const statusLower = status.toLowerCase();  // Convert to lowercase to ensure matching

      // Define text color for the room number based on status_kamar
      if (statusLower === 'masa sewa akan habis') {
        return { color: 'white' };  // If red, text becomes white
      } else if (statusLower === 'proses verifikasi') {
        return { color: '#333' };  // Yellow status stays with dark text
      }
      return { color: '#333' };  // Default case (black text)
    },
    showDetail(kamar) {
      this.selectedKamar = kamar;  // Store the selected room details
      this.showModal = true;       // Show the modal
    },
    closeModal() {
      this.showModal = false;     // Close the modal
      this.selectedKamar = null;  // Clear selected room
    }
  }
};
</script>

<style scoped>
.kamar-container {
  display: flex;
  flex-direction: column;
  gap: 40px;
  padding: 20px;
  margin-top: 50px;  /* Add top margin */
}

h2 {
  margin-bottom: 20px;
  color: #75276d;  /* Purple color */
  font-size: 22px;
  font-weight: bold;
}

h5 {
  color: #75276d;
}

.kamar-row {
  display: flex;
  gap: 20px;  /* Add space between rooms */
  flex-wrap: wrap;  /* Keep rooms wrapped if too many */
}

.kamar-card {
  width: 140px;
  height: 140px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: transform 0.3s;
}

.kamar-card:hover {
  transform: scale(1.05);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
}

.kamar-item {
  text-align: center;
}

.nomor-kamar {
  color: #333;
  font-size: 18px;
  font-weight: bold;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  width: 300px;
  text-align: left;
}

button {
  padding: 10px 20px;
  background-color: #c20ab0;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #9b0a7f;
}

.keterangan-warna {
  margin-bottom: 20px;
  font-size: 14px;
}

.keterangan-warna p {
  display: flex;
  align-items: center;
  margin: 5px 0;
}

.keterangan-warna .warna-hijau,
.keterangan-warna .warna-kuning,
.keterangan-warna .warna-merah,
.keterangan-warna .warna-abu {
  display: inline-block;
  width: 20px;
  height: 20px;
  margin-right: 10px;
  border-radius: 4px;
}

.keterangan-warna .warna-hijau {
  background-color: #8BC34A;
}

.keterangan-warna .warna-kuning {
  background-color: #FFEB3B;
}

.keterangan-warna .warna-merah {
  background-color: #D30000;
}

.keterangan-warna .warna-abu {
  background-color: #B0BEC5;
}
</style>
