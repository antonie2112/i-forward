import fs from 'fs';
import { config } from 'dotenv';
import { initializeApp } from "firebase/app";
import { getFirestore, doc, setDoc } from "firebase/firestore";

config({ path: '.env.local' });

const firebaseConfig = {
  apiKey: process.env.VITE_FIREBASE_API_KEY,
  authDomain: process.env.VITE_FIREBASE_AUTH_DOMAIN,
  projectId: process.env.VITE_FIREBASE_PROJECT_ID,
  storageBucket: process.env.VITE_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: process.env.VITE_FIREBASE_MESSAGING_SENDER_ID,
  appId: process.env.VITE_FIREBASE_APP_ID
};

const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

const data = JSON.parse(fs.readFileSync('/Users/nguyenphong/Desktop/catsheets_parsed.json', 'utf-8'));

async function upload() {
  let count = 0;
  for (const [productName, content] of Object.entries(data)) {
    // sanitize ID
    const safeName = productName.replace(/\//g, '-');
    await setDoc(doc(db, "catsheets", safeName), {
        name: productName,
        en: content.en || {},
        vi: content.vi || {}
    });
    count++;
  }
  console.log(`Successfully uploaded ${count} catsheets to Firestore.`);
  process.exit(0);
}

upload().catch(console.error);
