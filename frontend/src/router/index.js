import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/list-user',
    name: 'ListUser',
    component: () => import('../views/ListUser.vue'),
    meta: { requiresAuth: true, role: ['admin', 'pemilik'] }, 
  },
  {
    path: '/user-profile',
    name: 'UserProfile',
    component: () => import('../views/UserProfile.vue')
  },
  {
    path: '/dashboard',
    name: 'DasboardView',
    component: () => import('../views/DashboardView.vue'),
    meta: { requiresAuth: true, role: ['admin', 'pemilik'] }, 
  },
  {
    path: '/dashboard-penyewa',
    name: 'DasboardPenyewa',
    component: () => import('../views/DashboardPenyewa.vue'),
    meta: { requiresAuth: true, role: ['penyewa'] }, 
  },
  {
    path: '/list-kamar-penyewa',
    name: 'ListKamarPenyewa',
    component: () => import('../views/ListKamarPenyewa.vue'),
    meta: { requiresAuth: true, role: ['penyewa'] }, 
  },
  {
    path: '/list-penyewa',
    name: 'ListPenyewa',
    component: () => import('../views/ListPenyewa.vue'),
    meta: { requiresAuth: true, role: ['admin', 'pemilik'] }, 
  },
  {
    path: '/list-pemilik',
    name: 'ListPemilik',
    component: () => import('../views/ListPemilik.vue'),
    meta: { requiresAuth: true, role: ['admin', 'pemilik'] }, 
  },
  {
    path: '/status-penyewa',
    name: 'StatusPenyewa',
    component: () => import('../views/StatusPenyewa.vue'),
    meta: { requiresAuth: true, role: ['admin', 'pemilik'] }, 
  },
  {
    path: '/informasi-penyewa',
    name: 'InformasiPenyewa',
    component: () => import('../views/InformasiPenyewa.vue'),
    meta: { requiresAuth: true, role: ['penyewa'] },
  },
  {
    path: '/tambah-user',
    name: 'TambahUser',
    component: () => import('../views/TambahUser.vue'),
    meta: { requiresAuth: true, role: ['admin', 'pemilik'] }, 
  },
  {
    path: '/tambah-penyewa',
    name: 'TambahPenyewa',
    component: () => import('../views/TambahPenyewa.vue'),
    meta: { requiresAuth: true, role: ['admin', 'pemilik'] }, 
  },
  {
    path: '/tambah-pemilik',
    name: 'TambahPemilik',
    component: () => import('../views/TambahPemilik.vue'),
    meta: { requiresAuth: true, role: ['admin', 'pemilik'] }, 
  },
  {
    path: '/edit-user/:id',
    name: 'EditUser',
    component: () => import('../views/EditUser.vue'),
    meta: { requiresAuth: true, role: ['admin', 'pemilik'] }, 
  },
  {
    path: '/edit-pemilik/:id',
    name: 'EditPemilik',
    component: () => import('../views/EditPemilik.vue'),
    meta: { requiresAuth: true, role: ['admin', 'pemilik'] }, 
  },
  {
    path: '/edit-penyewa/:id',
    name: 'EditPenyewa',
    component: () => import('../views/EditPenyewa.vue'),
    meta: { requiresAuth: true, role: ['admin', 'pemilik'] }, 
  },
  {
    path: '/list-kamar',
    name: 'ListKamar',
    component: () => import('../views/ListKamar.vue')
  },
  {
    path: '/reservasi',
    name: 'ReservasiKamar',
    component: () => import('../views/ReservasiKamar.vue'),
    meta: { requiresAuth: true, role: ['penyewa'] }, 
  },
  {
    path: '/verifikasi',
    name: 'VerifikasiView',
    component: () => import('../views/VerifikasiView.vue'),
    meta: { requiresAuth: true, role: ['admin', 'pemilik'] }, 
  },
  {
    path: '/financial',
    name: 'FinancialView',
    component: () => import('../views/FinancialView.vue'),
    meta: { requiresAuth: true, role: ['admin', 'pemilik'] }, 
  },
  {
    path: '/tambah-pengeluaran',
    name: 'TambahPengeluaran',
    component: () => import('../views/TambahPengeluaran.vue'),
    meta: { requiresAuth: true, role: ['admin', 'pemilik'] }, 
  },
  {
    path: '/pengeluaran',
    name: 'ListPengeluaran',
    component: () => import('../views/ListPengeluaran.vue'),
    meta: { requiresAuth: true, role: ['admin', 'pemilik'] }, 
  },
  {
    path: '/login',
    name: 'LoginPage',
    component: () => import('../views/LoginPage.vue')
  },
  {
    path: '/',
    name: 'LandingPage',
    component: () => import('../views/LandingPage.vue')
  },
  {
    path: '/register',
    name: 'RegisterView',
    component: () => import('../views/RegisterView.vue')
  },
  {
    path: '/profile',
    name: 'UserProfile',
    component: () => import('../views/UserProfile.vue')
  },

]
const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('token');
  const userRole = localStorage.getItem('role');

  if (to.meta.requiresAuth) {
    if (!isAuthenticated) {
      return next({ name: 'LoginPage' });
    }
    if (to.meta.role && !to.meta.role.includes(userRole)) {
      return next({ name: 'LandingPage' });
    }
  }
  next();
});

export default router;