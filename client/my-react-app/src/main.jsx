import { StrictMode } from 'react'
// import ReactDOM from "react-dom";
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import ListItem from './ListItem.jsx'
import CreateItem from './CreateItem.jsx'
import List from './List.jsx'
import React from 'react';
import ReactDOM from 'react-dom/client';

// ReactDOM.render(<App />, document.getElementById("root"));
const root = ReactDOM.createRoot(document.getElementById('root'));

root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);