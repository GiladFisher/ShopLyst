import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import ListItem from './ListItem.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <ListItem title={"apple"} description={"fruit"} />
  </StrictMode>,
)
