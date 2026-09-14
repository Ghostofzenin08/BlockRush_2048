// Firebase Configuration for BlockRush
const firebaseConfig = {
  apiKey: "AIzaSyDk0t5kyDfHWttNuTZfeLJY7ztQzgPn0mM",
  authDomain: "blockrush-5b539.firebaseapp.com",
  projectId: "blockrush-5b539",
  storageBucket: "blockrush-5b539.firebasestorage.app",
  messagingSenderId: "908410956719",
  appId: "1:908410956719:web:07c4f607fe74f8c25c1d5a",
  measurementId: "G-T6388VB4HM"
};

// Initialize Firebase App
let firebaseApp = null;
let firebaseAuth = null;

try {
  if (typeof firebase !== 'undefined') {
    firebaseApp = firebase.initializeApp(firebaseConfig);
    firebaseAuth = firebase.auth();
    console.log("Firebase initialized successfully for BlockRush.");
  }
} catch (e) {
  console.warn("Firebase initialization warning:", e);
}

window.BLOCKRUSH_API_BASE = (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' || window.location.origin.includes('onrender.com'))
  ? ''
  : 'https://blockrush-2048.onrender.com';

// Global Auth State Manager
window.BlockRushAuth = {
  currentUser: null,
  jwtToken: localStorage.getItem('blockrush_jwt_token') || null,

  async syncWithBackend(user) {
    if (!user) return null;
    try {
      const apiBase = window.BLOCKRUSH_API_BASE || '';
      const res = await fetch(`${apiBase}/api/v1/auth/firebase-login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          uid: user.uid,
          email: user.email,
          displayName: user.displayName || user.email?.split('@')[0] || 'Player',
          photoURL: user.photoURL
        })
      });
      const data = await res.json();
      if (data && data.access_token) {
        window.BlockRushAuth.jwtToken = data.access_token;
        localStorage.setItem('blockrush_jwt_token', data.access_token);
        localStorage.setItem('blockrush_user', JSON.stringify(data.user));
      }
      return data;
    } catch (err) {
      console.error("Backend auth sync error:", err);
      return null;
    }
  },

  async loginWithGoogle() {
    if (!firebaseAuth) throw new Error("Firebase Auth not loaded");
    const provider = new firebase.auth.GoogleAuthProvider();
    const result = await firebaseAuth.signInWithPopup(provider);
    await this.syncWithBackend(result.user);
    return result.user;
  },

  async loginWithEmail(email, password) {
    if (!firebaseAuth) throw new Error("Firebase Auth not loaded");
    const result = await firebaseAuth.signInWithEmailAndPassword(email, password);
    await this.syncWithBackend(result.user);
    return result.user;
  },

  async signupWithEmail(email, password, displayName) {
    if (!firebaseAuth) throw new Error("Firebase Auth not loaded");
    const result = await firebaseAuth.createUserWithEmailAndPassword(email, password);
    if (displayName && result.user) {
      await result.user.updateProfile({ displayName });
    }
    await this.syncWithBackend(result.user);
    return result.user;
  },

  async logout() {
    if (firebaseAuth) {
      await firebaseAuth.signOut();
    }
    this.currentUser = null;
    this.jwtToken = null;
    localStorage.removeItem('blockrush_jwt_token');
    localStorage.removeItem('blockrush_user');
    window.location.reload();
  },

  onStateChanged(callback) {
    if (!firebaseAuth) return;
    firebaseAuth.onAuthStateChanged(async (user) => {
      this.currentUser = user;
      if (user) {
        await this.syncWithBackend(user);
      }
      if (typeof callback === 'function') {
        callback(user);
      }
    });
  }
};
