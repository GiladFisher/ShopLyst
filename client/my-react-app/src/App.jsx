import React, { useState, useEffect } from 'react';
import { jwtDecode } from 'jwt-decode';
import { jwtVerify } from 'jose';
import List from './List';

const App = () => {
  const [user, setUser] = useState(null);
  const [error, setError] = useState(null);
  const [signed, setSigned] = useState(false);

  useEffect(() => {
    // Load the Google Identity Services script
    const script = document.createElement('script');
    script.src = 'https://accounts.google.com/gsi/client';
    script.async = true;
    script.defer = true;
    script.onload = () => {
      google.accounts.id.initialize({
        client_id: '1038048702929-fa3fsb8ss4u2mq7nkjpai7l866aibgli.apps.googleusercontent.com',
        callback: handleCredentialResponse,
      });
      google.accounts.id.renderButton(
        document.getElementById('g_id_signin'),
        {
          theme: 'outline',
          size: 'large',
          text: 'signin_with',
        }
      );
    };
    document.body.appendChild(script);
  }, []);

  // Handle response from Google login
  const handleCredentialResponse = (response) => {
    if (response.error) {
      setError('Login failed');
      alert('Error occurred during login: ', response.error);
    } else {
      // The response.credential contains the JWT token
      // You can send this token to your backend for verification
      const token = response.credential;  // JWT token
    
      const userData = jwtDecode(response.credential);
      console.log('User data:', userData);
      setUser(userData);
      // set div to invisible 
      // document.getElementById('g_id_signin').hidden = true;
      setSigned(true); // set div to visible
    }
  };

  return (
    <div>
      {signed ? (
        <div>
          <h3>Welcome, {user.name}!</h3>
          <List user={user} />
        </div>
      ) : (
        <div id="g_id_signin" className="g_id_signin"></div>
      )}
      {error && <p>{error}</p>}
    </div>
  );
};

export default App;
