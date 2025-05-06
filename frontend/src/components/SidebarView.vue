<template>
  <div class="sidebar-wrapper">
    <ul class="nav" id="nav">
      <li v-if="roles === 'admin' || roles === 'pemilik'">
        <router-link to="/dashboard" exact-active-class="active">
          <i class="nc-icon nc-bank"></i>
          <p>Dashboard</p>
        </router-link>
      </li>
      <li  v-if="roles === 'penyewa'">
        <router-link to="/dashboard-penyewa" exact-active-class="active">
          <i class="nc-icon nc-bank"></i>
          <p>Dashboard</p>
        </router-link>
      </li>
      <li v-if="roles === 'admin' || roles === 'pemilik'">
        <router-link to="/financial" exact-active-class="active">
          <i class="nc-icon nc-money-coins"></i>
          <p>Financial</p>
        </router-link>
      </li>
      <li v-if="roles === 'admin' || roles === 'pemilik'">
        <router-link to="/pengeluaran" exact-active-class="active">
          <i class="nc-icon nc-tap-01"></i>
          <p>Pengeluaran</p>
        </router-link>
      </li>
      <li v-if="roles === 'admin' || roles === 'pemilik'">
        <router-link to="/list-kamar" exact-active-class="active">
          <i class="nc-icon nc-app"></i>
          <p>List Kamar</p>
        </router-link>
      </li>
      <li  v-if="roles === 'penyewa'">
        <router-link to="/list-kamar-penyewa" exact-active-class="active">
          <i class="nc-icon nc-app"></i>
          <p>List Kamar</p>
        </router-link>
      </li>
      <li v-if="roles === 'penyewa'">
        <router-link to="/reservasi" exact-active-class="active">
          <i class="nc-icon nc-cart-simple"></i>
          <p>Reservasi</p>
        </router-link>
      </li>
      <li v-if="roles === 'admin' || roles === 'pemilik'">
        <router-link to="/verifikasi" exact-active-class="active">
          <i class="nc-icon nc-check-2"></i>
          <p>Verifikasi</p>
        </router-link>
      </li>
      <li v-if="roles === 'admin' || roles === 'pemilik'">
        <router-link to="/status-penyewa" exact-active-class="active">
          <i class="nc-icon nc-layout-11"></i>
          <p>Status Penyewa</p>
        </router-link>
      </li>
      <li v-if="roles === 'penyewa'">
        <router-link to="/informasi-penyewa" exact-active-class="active">
          <i class="nc-icon nc-alert-circle-i"></i>
          <p>Informasi Penyewa</p>
        </router-link>
      </li>
      <hr v-if="roles === 'admin' || roles === 'pemilik'" class="divider">
      <li v-if="roles === 'admin' || roles === 'pemilik'">
        <router-link to="/list-user" exact-active-class="active">
          <i class="nc-icon nc-badge"></i>
          <p>User List</p>
        </router-link>
      </li>
      <ul>
        <li v-if="roles === 'admin' || roles === 'pemilik'">
          <router-link to="/list-penyewa" exact-active-class="active">
            <i class="nc-icon nc-single-02"></i>
            <p>Penyewa</p>
          </router-link>
        </li>
        <li v-if="roles === 'admin' || roles === 'pemilik'">
          <router-link to="/list-pemilik" exact-active-class="active">
            <i class="nc-icon nc-single-02"></i>
            <p>Pemilik</p>
          </router-link>
        </li>
      </ul>
      <hr v-if="roles === 'admin' || roles === 'pemilik'" class="divider">
    </ul>
  </div>
</template>

<script>
export default {
  props: {
    roles: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      isSidebarVisible: true, // Menampilkan sidebar
    };
  },
};
</script>

<style scoped>
/* Style for active link with purple background, white text, and rounded corners */
#nav a.active {
  background-color: #75276d !important; /* Purple background */
  color: white !important; /* White text */
  border-radius: 8px; /* Rounded corners */
  padding: 8px 15px; /* Padding inside the active link */
}

#nav a.active i {
  color: white !important; /* White icon */
}

/* Style for non-active link */
#nav a {
  color: #555; /* Default text color */
}

#nav a i {
  color: #555; /* Default icon color */
}

#nav a.router-link-exact-active,
#nav a.router-link-exact-active i {
  background-color: transparent !important;
  color: #75276d !important; /* Retain purple text color for active link */
}

/* Divider styles */
.divider {
  border: none;
  border-top: 1px solid #ddd;
  margin: 10px 0;
}

/* Padding for nav items */
.nav li {
  padding: 10px 0;
}

/* Adding padding to inner <ul> to properly align nested items */
.nav ul {
  padding-left: 20px;
}

/* To make the sidebar responsive */
@media (max-width: 768px) {
  #nav {
    padding: 0;
  }
}
</style>
