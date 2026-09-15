const API_BASE = "http://127.0.0.1:8000";

function getStudentId() {
    return localStorage.getItem("studentId");
}

function requireLogin() {
    if (!getStudentId()) {
        window.location.href = "index.html";
    }
}

function logout() {
    localStorage.removeItem("studentId");
    localStorage.removeItem("studentName");
    localStorage.removeItem("studentEmail");
    window.location.href = "index.html";
}

async function apiRequest(endpoint, options = {}) {
    const response = await fetch(API_BASE + endpoint, {
        ...options,
        headers: {
            "Content-Type": "application/json",
            ...(options.headers || {})
        }
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || data.message || "Request failed");
    return data;
}
