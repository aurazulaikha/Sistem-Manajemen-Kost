<template>
  <div class="landing-page">
    <div class="background-image">
      <div class="header">
        <div class="logo-title">
          <img src="/assets/img/logokost.png" alt="Logo" class="logo" />
          <h1 class="title">Kost Letter U</h1>
        </div>
        <h2 class="slogan"><i>"Comfortable, just like home!"</i></h2> <!-- Slogan di bawah judul -->
      </div>
      
      <div class="description-container">
        <p class="cta-text">
          Kos Letter U adalah pilihan terbaik untuk Anda! Kami menawarkan berbagai fasilitas unggulan dan harga yang sangat bersaing. Dengan lokasi yang strategis dan lingkungan yang aman, Kos Letter U memberikan kenyamanan untuk Anda yang membutuhkan tempat tinggal yang praktis dan nyaman.
        </p>
        <p class="cta-text">
          Ayo bergabung dengan kami dan nikmati pengalaman kost yang berbeda!
        </p>
      </div>

      <!-- Call-to-Action Buttons -->
      <div class="buttons">
        <router-link to="/login">
          <button class="btn login">Login Sekarang!</button>
        </router-link>
        <router-link to="/register">
          <button class="btn register">Register</button>
        </router-link>
      </div>
    </div>

    <!-- Footer -->
    <footer class="footer">
      <div class="footer-content">
        <div class="footer-section">
          <h3>Kost Letter U</h3>
          <ul>
            <li><a href="#">Tentang Kami</a></li>
          </ul>
          <ul>
            <li><a href="#">Blog Kost Letter U</a></li>
          </ul>
        </div>
        <div class="footer-section">
          <h3>Kebijakan</h3>
          <ul>
            <li><a href="#">Kebijakan Privasi</a></li>
          </ul>
          <ul>
            <li><a href="#">Syarat dan Ketentuan</a></li>
          </ul>
        </div>
        <div class="footer-section">
          <h3>Hubungi Kami</h3>
          <p>+628-1209-2928-9012</p>
          <div class="social-icons">
            <a href="#"><img src="/assets/img/facebook.png" alt="Facebook" class="icon" /></a>
            <a href="#"><img src="/assets/img/instagram.png" alt="Instagram" class="icon" /></a>
            <a href="#"><img src="/assets/img/twitter.png" alt="Twitter" class="icon" /></a>
            <a href="#"><img src="/assets/img/mail.png" alt="Email" class="icon" /></a>
          </div>
        </div>
      </div>
      <hr class="footer-divider" />
      <div class="footer-copyright">
        <p>© {{ new Date().getFullYear() }} letteru.com. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<style scoped>
.landing-page {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  text-align: center;
  color: white;
  background: url('@/assets/bed.png') no-repeat center center/cover;
  height: 125vh;
  overflow-y: auto;
  animation: backgroundAnimation 5s infinite alternate;
}

@keyframes backgroundAnimation {
  0% {
    background-position: center center;
  }
  50% {
    background-position: center top;
  }
  100% {
    background-position: center bottom;
  }
}

.background-image {
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 40px;
  background: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), url('@/assets/bed.png') no-repeat center center/cover;
  background-size: cover;
  border-radius: 10px;
  animation: backgroundZoom 15s infinite alternate;
}

@keyframes backgroundZoom {
  0% {
    background-size: 100%;
  }
  50% {
    background-size: 110%;
  }
  100% {
    background-size: 100%;
  }
}

.header {
  margin-bottom: 30px;
  display: flex;
  flex-direction: column; /* Mengubah layout ke arah kolom */
  align-items: center;
}

.logo-title {
  display: flex;
  align-items: center;
  gap: 20px; /* Memberikan jarak antara logo dan teks */
}

.logo {
  width: 80px; /* Ukuran logo bisa disesuaikan */
  height: auto;
}

.title {
  font-size: 3.0rem;
  font-weight: bold;
  margin-bottom: 0;
}

.slogan {
  font-size: 2.0rem;
  margin-top: 25px;
}

.description-container {
  max-width: 800px;
  margin-bottom: 30px;
}

.cta-text {
  font-size: 1rem;
  margin-bottom: 20px;
}

.buttons {
  display: flex;
  flex-direction: row;
  gap: 20px;
}

.btn {
  padding: 15px 30px;
  font-size: 1rem;
  color: white;
  border: 2px solid white;
  border-radius: 5px;
  background: transparent;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn:hover {
  background: white;
  color: #581a52;
}

.footer {
  background-color: #581a52;
  padding: 20px;
  width: 100%;
}

.footer-content {
  display: flex;
  justify-content: space-around;
  align-items: flex-start;
  margin-bottom: 10px;
}

.footer-section {
  text-align: left;
}

.footer-section h3 {
  margin-bottom: 10px;
  font-size: 1.2rem;
  font-weight: bold;
}

.footer-section ul {
  list-style: none;
  padding: 0;
}

.footer-section ul li {
  margin-bottom: 5px;
}

.footer-section ul li a {
  color: white;
  text-decoration: none;
}

.social-icons a {
  color: white;
  margin-right: 10px;
}

.icon {
  width: 20px;
  height: 20px;
  margin-right: 10px;
  cursor: pointer;
  transition: transform 0.3s ease, filter 0.3s ease;
  filter: brightness(0) invert(1);
}

.icon:hover {
  transform: scale(1.2);
}

.footer-divider {
  width: 100%;
  height: 1px;
  background-color: white;
  opacity: 0.5;
  margin: 20px 0;
}

.footer-copyright {
  text-align: right;
  font-size: 0.8rem;
  padding-right: 10px;
  color: #ffffff;
  opacity: 0.8;
}
</style>
