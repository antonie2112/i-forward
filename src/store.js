import { 
    collection, 
    addDoc, 
    query, 
    where, 
    getDocs, 
    serverTimestamp,
    orderBy,
    limit 
} from "firebase/firestore";
import { db, auth } from "./firebase";

// Save a draft quotation
export const saveDraft = async (tvdData) => {
    const user = auth.currentUser;
    if (!user) return;

    try {
        const docRef = await addDoc(collection(db, "drafts"), {
            uid: user.uid,
            email: user.email,
            data: tvdData,
            createdAt: serverTimestamp(),
            label: `Draft - ${new Date().toLocaleDateString()}`
        });
        console.log("Draft saved with ID: ", docRef.id);
        await logActivity("Created a new draft quotation");
        return docRef.id;
    } catch (e) {
        console.error("Error adding document: ", e);
    }
};

// Log user activity
export const logActivity = async (action) => {
    const user = auth.currentUser;
    if (!user) return;

    try {
        await addDoc(collection(db, "activities"), {
            uid: user.uid,
            email: user.email,
            action: action,
            timestamp: serverTimestamp()
        });
    } catch (e) {
        console.error("Error logging activity: ", e);
    }
};

// Fetch recent activity
export const getRecentActivity = async (count = 5) => {
    const user = auth.currentUser;
    if (!user) return [];

    const q = query(
        collection(db, "activities"),
        where("uid", "==", user.uid),
        orderBy("timestamp", "desc"),
        limit(count)
    );

    const querySnapshot = await getDocs(q);
    return querySnapshot.docs.map(doc => doc.data());
};

window.saveDraft = saveDraft;
window.getRecentActivity = getRecentActivity;
