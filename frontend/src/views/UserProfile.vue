<template>
  <div class="content">
    <div class="row justify-content-center align-items-start" style="height: 74vh;">
      <div class="col-md-4 col-sm-6 col-10"> 
        <div class="card card-user square-card">
          <div class="card-header text-center">
            <h5 class="card-title title-style">User Profile</h5>
          </div>
          <div class="card-body text-center">
            <div class="profile-info">
              <!-- Image above the name -->
              <div class="info-item">
                <img class="info-icon" :src="profile.imageUrl || 'assets/img/profile.png'" alt="User Avatar" />
              </div>
              <div class="info-item">
                <h3 class="info-name">{{ profile.nama || 'Loading...' }}</h3>
              </div>
              <hr class="divider" />
              <div class="info-item d-flex justify-content-between">
                <div class="info-box">
                  <label class="info-label">Email:</label>
                  <p class="info-value">{{ profile.email || 'Loading...' }}</p>
                </div>
                <div class="info-box text-right">
                  <label class="info-label">Nomor Telepon:</label>
                  <p class="info-value">{{ profile.no_telp || 'Loading...' }}</p>
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
import axios from "axios";

export default {
  data() {
    return {
      profile: {
        nama: '',
        email: '',
        no_telp: '',
        imageUrl: ''
      },
      loading: true,
    };
  },
  created() {
    this.fetchProfile();
  },
  methods: {
    async fetchProfile() {
      const token = localStorage.getItem("token");
      if (!token) {
        alert("Anda belum login.");
        this.$router.push("/login"); // Redirect to login page
        return;
      }

      try {
        const response = await axios.get("http://127.0.0.1:5000/profile", {
          headers: {
            Authorization: token,
          },
        });

        this.profile = response.data;
      } catch (error) {
        console.error(error);
        alert("Gagal memuat informasi profil.");
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.card-user {
  border-radius: 12px; 
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); 
}

.square-card {
  width: 100%;
  max-width: 550px; 
  display: flex;
  flex-direction: column;
  justify-content: flex-start; 
}

.card-header {
  background-color: #75276d;
  color: white;
  padding: 10px; 
  border-radius: 12px 12px 0 0; 
}

.card-body {
  flex: 1;
  padding: 10px 20px; 
}

.profile-info {
  margin-top: 5px; 
}

.info-item {
  margin-bottom: 5px; 
}

.info-name {
  font-size: 28px; 
  font-weight: bold;
  color: #75276d;
  margin: 0;
}

.divider {
  border-top: 2px solid #75276d; 
  margin: 10px 0; 
}

.info-label {
  font-weight: bold;
  color: #555;
}

.info-value {
  margin: 5px 0;
  color: #333;
}

.title-style {
  font-weight: bold;
}

.d-flex {
  display: flex;
  justify-content: space-between; 
  width: 100%;
}

.info-box {
  width: 45%; 
  text-align: left;
}

.text-right {
  text-align: right; 
}

.info-icon {
  width: 80px;
  height: 80px;
  border-radius: 50%; 
  object-fit: cover; 
  margin-bottom: 10px;
}

.row {
  display: flex;
  justify-content: center; 
  align-items: flex-start; 
  height: 100vh; 
  padding-top: 15vh;
  padding-bottom: 5vh;
}

.col-md-4 {
  width: 100%; 
}

@media (max-width: 768px) {
  .square-card {
    max-width: 90%; 
  }
  .info-name {
    font-size: 24px; 
  }
}
</style>
