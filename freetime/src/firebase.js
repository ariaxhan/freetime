// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getDatabase, ref, set } from "firebase/database";

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyCgQEAgZESMmntkN6-svRpmAl5hFydAH_w",
  authDomain: "freetime-9428d.firebaseapp.com",
  projectId: "freetime-9428d",
  databaseURL: "https://freetime-9428d-default-rtdb.firebaseio.com",
  storageBucket: "freetime-9428d.appspot.com",
  messagingSenderId: "205383744584",
  appId: "1:205383744584:web:529722900ffa50599dac7d",
  measurementId: "G-6STTHXTKSE",
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const database = getDatabase(app);
const analytics = getAnalytics(app);

export { database };
