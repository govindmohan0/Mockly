import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyC7couKed7nv9f_QyxpQ-qtg_UBmiht-os",
  authDomain: "mockly-7e061.firebaseapp.com",
  projectId: "mockly-7e061",
  storageBucket: "mockly-7e061.firebasestorage.app",
  messagingSenderId: "905060319455",
  appId: "1:905060319455:web:5dacc87c68bd0b54ea696a",
  measurementId: "G-K4F7KQ1KSV"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app)



export { app, auth };
