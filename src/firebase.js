import { initializeApp } from "firebase/app";
import { 
    getAuth, 
    onAuthStateChanged, 
    GoogleAuthProvider, 
    signInWithPopup, 
    signOut 
} from "firebase/auth";
import { getFirestore } from "firebase/firestore";

// TODO: Replace with user's Firebase config
const firebaseConfig = {
  apiKey: "PLACEHOLDER",
  authDomain: "PLACEHOLDER",
  projectId: "PLACEHOLDER",
  storageBucket: "PLACEHOLDER",
  messagingSenderId: "PLACEHOLDER",
  appId: "PLACEHOLDER"
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export const db = getFirestore(app);

// Auth helper
export const checkEcolabUser = (user) => {
    if (!user) return false;
    return user.email && user.email.toLowerCase().endsWith("@ecolab.com");
};

export { GoogleAuthProvider, signInWithPopup, signOut, onAuthStateChanged };
