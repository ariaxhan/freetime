// src/App.js
import React from "react";
import { database } from "./firebase";
import { ref, set } from "firebase/database";

function writeUserData(userId, name, email, imageUrl) {
  set(ref(database, "users/" + userId), {
    username: name,
    email: email,
    profile_picture: imageUrl,
  });
}

function App() {
  const handleWrite = () => {
    writeUserData(
      "1",
      "John Doe",
      "john.doe@example.com",
      "http://example.com/john.jpg",
    );
  };

  return (
    <div className="App">
      <h1>Write to Firebase Realtime Database</h1>
      <button onClick={handleWrite}>Write Data</button>
    </div>
  );
}

export default App;
