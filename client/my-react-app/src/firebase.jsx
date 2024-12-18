// src/firebase.js
import {initializeApp} from "firebase/app";
import { getAuth } from "firebase/auth";

const firebaseConfig = {
    apiKey: "AIzaSyAahSvU3fQ0mXGfMvuOyW_wQFKSNXELUkU",
    authDomain: "shoplyst-584c0.firebaseapp.com",
    projectId: "shoplyst-584c0",
    storageBucket: "shoplyst-584c0.firebasestorage.app",
    messagingSenderId: "888379277599",
    appId: "1:888379277599:web:ffc40f44a7fc4e125ab02a"
  };

const firebaseApp = initializeApp(firebaseConfig);
const auth = getAuth(firebaseApp);

export { auth, firebaseApp };
