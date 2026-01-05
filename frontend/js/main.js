// ==============================
// API CONFIG
// ==============================
const API_BASE = "https://criminal-id-system.onrender.com";

// ==============================
// TOKEN HELPERS
// ==============================
function setToken(token) {
  localStorage.setItem("token", token);
}

function getToken() {
  return localStorage.getItem("token");
}

function clearToken() {
  localStorage.removeItem("token");
}

// ==============================
// AUTH HEADERS
// ==============================
function authHeaders() {
  return {
    Authorization: `Bearer ${getToken()}`
  };
}

// ==============================
// AUTH GUARD
// ==============================
function requireAuth() {
  if (!getToken()) {
    window.location.href = "login.html";
  }
}

// ==============================
// LOGOUT
// ==============================
function logout() {
  clearToken();
  updateAuthButton();          // 🔥 update UI immediately
  window.location.href = "index.html";
}

// ==============================
// NAVBAR AUTH STATE HANDLER
// ==============================
function updateAuthButton() {
  const btn = document.getElementById("authBtn");
  if (!btn) return;

  if (getToken()) {
    // Logged in
    btn.textContent = "Logout";
    btn.onclick = logout;
  } else {
    // Logged out
    btn.textContent = "Login";
    btn.onclick = () => {
      window.location.href = "login.html";
    };
  }
}

// ==============================
// INIT ON PAGE LOAD
// ==============================
document.addEventListener("DOMContentLoaded", updateAuthButton);

// ==============================
// EXPOSE GLOBALS (used elsewhere)
// ==============================
window.setToken = setToken;
window.getToken = getToken;
window.authHeaders = authHeaders;
window.requireAuth = requireAuth;
