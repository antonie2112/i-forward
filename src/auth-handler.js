import { auth, GoogleAuthProvider, signInWithPopup, signOut, onAuthStateChanged, checkEcolabUser } from "./firebase";

const loginOverlay = document.getElementById('login-overlay');
const loginBtn = document.getElementById('loginBtn');
const loginError = document.getElementById('loginError');
const bottomNav = document.querySelector('.mobile-bottom-nav');
const skipLoginBtn = document.getElementById('skipLoginBtn');
const mainDashboard = document.getElementById('main-dashboard');

function toggleBottomNav(show) {
    if (bottomNav) {
        if (show) {
            bottomNav.classList.remove('nav-hidden');
        } else {
            bottomNav.classList.add('nav-hidden');
        }
    }
}

function toggleDashVisibility(show) {
    if (mainDashboard) {
        if (show) {
            mainDashboard.classList.remove('hidden');
        } else {
            mainDashboard.classList.add('hidden');
        }
    }
}

// Login function
const handleLogin = async () => {
    const provider = new GoogleAuthProvider();
    try {
        const result = await signInWithPopup(auth, provider);
        const user = result.user;
        
        if (checkEcolabUser(user)) {
            // Success
            loginOverlay.classList.add('hidden');
            toggleDashVisibility(true);
            toggleBottomNav(true);
            loginError.classList.add('hidden');
            console.log("Logged in as:", user.email);
            // Initialize app data if needed
            if (window.initializeAppData) window.initializeAppData(user);
        } else {
            // Wrong domain
            await signOut(auth);
            loginError.innerText = "Access restricted to @ecolab.com emails only.";
            loginError.classList.remove('hidden');
        }
    } catch (error) {
        console.error("Auth Error:", error);
        loginError.innerText = "Login failed. Please try again.";
        loginError.classList.remove('hidden');
    }
};

// Check current auth state
onAuthStateChanged(auth, (user) => {
    if (user && checkEcolabUser(user)) {
        loginOverlay.classList.add('hidden');
        toggleDashVisibility(true);
        toggleBottomNav(true);
        if (window.initializeAppData) window.initializeAppData(user);
    } else {
        loginOverlay.classList.remove('hidden');
        toggleDashVisibility(false);
        toggleBottomNav(false);
    }
});


// Guest Access function
const handleGuestAccess = () => {
    loginOverlay.classList.add('hidden');
    toggleDashVisibility(true);
    toggleBottomNav(true);
    console.log("Accessing as Guest");
    // Mock user for UI if needed
    if (window.initializeAppData) window.initializeAppData({ 
        email: "guest@iforward.app", 
        displayName: "Guest User",
        isGuest: true
    });
};

// Attach to UI
if (loginBtn) loginBtn.addEventListener('click', handleLogin);
if (skipLoginBtn) skipLoginBtn.addEventListener('click', handleGuestAccess);

// Export logout for global use
window.logoutUser = async () => {
    await signOut(auth);
    window.location.reload();
};
