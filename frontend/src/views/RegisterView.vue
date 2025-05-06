<template>
  <div class="register-page">
    <div class="background-image">
      <div class="register-container">
        <h1 class="register-title">Register</h1>
        <form @submit.prevent="register">
          <div class="form-group">
            <input type="text" v-model="nama" placeholder="Nama" required />
            <input type="email" v-model="email" placeholder="Email" required />
            <input type="password" v-model="password" placeholder="Password" required minlength="8" maxlength="20" />
            <input type="password" v-model="confirmPassword" placeholder="Confirm Password" required minlength="8" maxlength="20" />
            <input type="text" v-model="no_telp" placeholder="Nomor Telepon" required />
          </div>
          <button type="submit">Register</button>

          <!-- Display Error or Success Message -->
          <div v-if="error" class="error-message">{{ error }}</div>
          <div v-if="success" class="success-message">{{ success }}</div>
        </form>

        <p class="login-link">
          Sudah punya akun? <router-link to="/login">Login</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      nama: '',
      email: '',
      password: '',
      confirmPassword: '', // Added confirm password
      no_telp: '',
      error: '', // Error message
      success: '', // Success message
    };
  },
  methods: {
    async register() {
      // Clear previous messages
      this.error = '';
      this.success = '';

      // Validate email and phone number format
      const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
      if (!emailPattern.test(this.email)) {
        this.error = 'Format email tidak valid';
        return;
      }

      const phonePattern = /^[0-9]{10,15}$/;
      if (!phonePattern.test(this.no_telp)) {
        this.error = 'Nomor telepon harus terdiri dari 10 hingga 15 digit';
        return;
      }

      // Check if passwords match
      if (this.password !== this.confirmPassword) {
        this.error = 'Password dan konfirmasi password tidak cocok';
        return;
      }

      try {
        const response = await axios.post('http://127.0.0.1:5000/register', {
          nama: this.nama,
          email: this.email,
          password: this.password,
          no_telp: this.no_telp, // No roles sent since it's handled by the API
        });

        if (response.status === 201) {
          this.success = 'Registrasi berhasil! Redirecting to login...';
          setTimeout(() => {
            this.$router.push('/login');
          }, 2000); // Redirect after 2 seconds
        }
      } catch (error) {
        if (error.response && error.response.data) {
          this.error = error.response.data.error || 'Registrasi gagal. Silakan coba lagi.';
        } else {
          this.error = 'Terjadi kesalahan, silakan coba lagi.';
        }
      }
    },
  },
};
</script>

<style scoped>
/* Styling for the register page */
.register-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: url('@/assets/bed.png') no-repeat center center/cover;
  background-size: cover;
}

.background-image {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
  padding: 20px;
  border-radius: 10px;
}

.register-container {
  background: rgba(200, 200, 200, 0.8); /* Light grayish background */
  padding: 40px;
  border-radius: 10px;
  width: 100%;
  max-width: 400px;
  text-align: center;
  position: relative;
}

.register-title {
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

input,
select {
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

.error-message {
  color: red;
  font-size: 1rem;
  margin-top: 10px;
}

.success-message {
  color: green;
  font-size: 1rem;
  margin-top: 10px;
}

.login-link {
  margin-top: 20px;
  font-size: 0.9rem;
  color: #4b4a4a;
}

.login-link a {
  color: #75276d;
  font-weight: bold;
  text-decoration: none;
}

.login-link a:hover {
  text-decoration: underline;
}
</style>
