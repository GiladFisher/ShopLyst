import React, { useEffect, useState } from "react";
import firebase from "firebase/compat/app";
import * as firebaseui from "firebaseui";
import "firebaseui/dist/firebaseui.css";
import { auth } from "./firebase";

const FirebaseUIAuth = () => {
  const [uiInstance, setUiInstance] = useState(null);

  useEffect(() => {
    // Initialize FirebaseUI instance
    let ui = firebaseui.auth.AuthUI.getInstance();
    if (!ui) {
      ui = new firebaseui.auth.AuthUI(auth);
      setUiInstance(ui);
    }

    // FirebaseUI configuration
    const uiConfig = {
      signInSuccessUrl: "", // Redirect after sign-in
      signInOptions: [
        firebase.auth.GoogleAuthProvider.PROVIDER_ID,
        firebase.auth.FacebookAuthProvider.PROVIDER_ID,
        firebase.auth.EmailAuthProvider.PROVIDER_ID,
      ],
    };

    // Start FirebaseUI
    ui.start("#firebaseui-auth-container", uiConfig);

    return () => {
      // Proper cleanup
      if (ui) {
        ui.delete().catch((error) => {
          console.error("FirebaseUI cleanup error:", error);
        });
      }
    };
  }, []); // Only run once

  return <div id="firebaseui-auth-container"></div>;
};

export default FirebaseUIAuth;
