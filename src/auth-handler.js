import { auth, GoogleAuthProvider, signInWithPopup, signOut, onAuthStateChanged, checkEcolabUser } from "./firebase";

const loginOverlay = document.getElementById('login-overlay');
const loginBtn = document.getElementById('loginBtn');
const loginError = document.getElementById('loginError');

// Login function
const handleLogin = async () => {
    const provider = new GoogleAuthProvider();
    try {
        const result = await signInWithPopup(auth, provider);
        const user = result.user;
        
        if (checkEcolabUser(user)) {
            // Success
            loginOverlay.classList.add('hidden');
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
        if (window.initializeAppData) window.initializeAppData(user);
    } else {
        loginOverlay.classList.remove('hidden');
    }
});

// Attach to UI
if (loginBtn) loginBtn.addEventListener('click', handleLogin);

// Export logout for global use
window.logoutUser = async () => {
    await signOut(auth);
    window.location.reload();
};
