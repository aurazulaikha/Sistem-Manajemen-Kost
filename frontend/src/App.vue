<template>
  <div>
    <!-- Layout utama untuk halaman selain login, register, dan landing -->
    <div v-if="$route.path !== '/login' && $route.path !== '/register' && $route.path !== '/'">
      <div class="wrapper">
        <div class="sidebar" data-color="white" data-active-color="danger">
          <div class="logo">
            <div class="logo-container">
              <div class="logo-image-small">
                <img src="assets/img/kostLogo.png" alt="Logo Kost" />
              </div>
              <div class="logo-text">Kos Letter U</div>
            </div>
          </div>
          <!-- Sidebar dengan role yang benar -->
          <SidebarView :roles="userRole" />
        </div>
        <div class="main-panel">
          <NavbarView />
          <router-view />
          <FooterView />
        </div>
      </div>
    </div>

    <!-- Layout sederhana untuk login, register, dan landing -->
    <div v-else>
      <router-view />
    </div>
  </div>
</template>

<script>
import FooterView from './components/FooterView.vue';
import NavbarView from './components/NavbarView.vue'
import SidebarView from './components/SidebarView.vue';

export default {
  name: 'App',
  components: {
    FooterView,
    NavbarView,
    SidebarView
  },
  data() {
    return {
      userRole: '', // Variabel untuk menyimpan role user
    };
  },
  created() {
    this.setUserRole(); // Tentukan userRole saat komponen dibuat
    console.log('User Role Set on Created Hook:', this.userRole);
  },
  methods: {
    logout() {
      localStorage.removeItem('role');
      localStorage.removeItem('token');
      this.updateRoleAfterLogout(); // Mengupdate role setelah logout
      this.$router.push({ name: 'LoginPage' }); // Redirect ke halaman login
    },
    setUserRole() {
      const rolesFromRoute = this.$route.params.roles || '';
      const validRoles = ['admin', 'pemilik', 'penyewa'];

      if (validRoles.includes(rolesFromRoute)) {
        this.userRole = rolesFromRoute;
        localStorage.setItem('role', rolesFromRoute);
      } else {
        const storedRole = localStorage.getItem('role');
        if (validRoles.includes(storedRole)) {
          this.userRole = storedRole;
        } else {
          this.userRole = 'penyewa'; // Default role
        }
      }
      console.log('Current User Role:', this.userRole);
    },
    updateRoleAfterLogout() {
      this.userRole = 'penyewa'; // Setelah logout, set role default sebagai penyewa
      localStorage.setItem('role', 'penyewa'); // Simpan role default ke localStorage
    }
  },
  watch: {
    '$route.path'() {
      this.setUserRole();
    },
  },
};
</script>


<style scoped>
.logo-container {
  display: flex;
  align-items: center;
}

.logo-image-small img {
  width: 30px;
  height: auto;
  margin-right: 8px;
}

.logo-text {
  font-size: 18px;
  font-weight: bold;
  color: #75276d;
}
</style>
