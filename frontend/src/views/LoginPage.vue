<template>
  <div class="login-page">
    <div class="background-image">
      <div class="login-container">
        <h1 class="login-title">Login</h1>
        <form @submit.prevent="login">
          <div class="form-group">
            <input type="email" v-model="email" placeholder="Email" required />
            <input type="password" v-model="password" placeholder="Password" required />
            <div class="password-note">Password must be at least 8 characters long</div>
          </div>
          <button type="submit">Login</button>
        </form>

        <div class="register-link">
          <p class="center-text">
            Tidak punya akun? <router-link to="/register">Register</router-link>
          </p>
          <router-link to="/" class="back-button">Kembali ke halaman sebelumnya</router-link>
        </div>
      </div>
    </div>

    <!-- Modal Notification -->
    <div v-if="showErrorModal" class="modal-overlay">
      <div class="modal-content">
        <span class="close-icon" @click="showErrorModal = false">&times;</span>
        <p>{{ errorMessage }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      email: '',
      password: '',
      showErrorModal: false,  // Menandakan apakah modal error ditampilkan
      errorMessage: '',       // Menyimpan pesan error
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post('http://127.0.0.1:5000/login', {
          email: this.email,
          password: this.password,
        });

        if (response.status === 200) {
          localStorage.setItem('token', response.data.token);
          localStorage.setItem('role', response.data.role);

          const role = response.data.role;
          if (role === 'admin' || role === 'pemilik') {
            this.$router.push('/dashboard');
          } else if (role === 'penyewa') {
            this.$router.push('/dashboard-penyewa');
          }
        }
      } catch (error) {
        this.errorMessage = error.response?.data?.error || 'Login failed';
        this.showErrorModal = true;  // Menampilkan modal jika login gagal
      }
    },
  },
};
</script>

<style scoped>
/* Styling for the login page */
.login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: url('@/assets/bed.png') no-repeat center center/cover;
  background-size: cover;
  position: relative;
}

.background-image {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
  background: url('@/assets/bed.png') no-repeat center center/cover;
  background-size: cover;
  padding: 20px;
  border-radius: 10px;
}

.login-container {
  background: rgba(200, 200, 200, 0.8); /* Light grayish background */
  padding: 40px;
  border-radius: 10px;
  width: 100%;
  max-width: 400px;
  text-align: center;
  position: relative;
}

.login-title {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 20px;
  color: #75276d;
}

.form-group {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}

input {
  margin: 10px 0;
  padding: 10px;
  width: 100%;
  border: 1px solid #ccc;
  border-radius: 5px;
}

button {
  margin: 10px 0;
  padding: 10px;
  width: 100%;
  background-color: #75276d;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #5a1c54;
}

.password-note {
  font-size: 0.8rem;
  color: #373737;
  margin-top: 5px;
  text-align: left;
}

.register-link {
  margin-top: 20px;
  font-size: 0.9rem;
  color: #4b4a4a;
}

.center-text {
  text-align: center; /* Center the text */
}

.register-link a {
  color: #75276d; /* Same color as "Tidak punya akun?" */
  font-weight: bold;
  text-decoration: none;
}

.register-link a:hover {
  text-decoration: underline;
}

.back-button {
  margin-top: 10px;
  font-size: 12px; /* Add space between "Register" and "Back" */
  color: #4b4a4a;
  text-decoration: underline; /* Underline the "Back" link */
}

.back-button:hover {
  text-decoration: none; /* Remove underline when hovered */
}

/* Modal Styling */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.3); /* Black background with transparency */
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background: white; /* Bright red background */
  color: #c40e0e; /* White text color */
  padding: 20px;
  border-radius: 10px;
  text-align: center;
  max-width: 300px;
  font-weight: bold;
  position: relative;
}

.close-icon {
  position: absolute;
  top: 5px;
  right: 5px;
  font-size: 20px;
  font-weight: bold;
  cursor: pointer;
  color: #c40e0e; /* White color for close icon */
}

button {
  background-color: #75276d;
  border-radius: 5px;
  padding: 10px 20px;
  border: none;
  color: white;
  cursor: pointer;
}

button:hover {
  background-color: #5a1c54;
}
</style>
