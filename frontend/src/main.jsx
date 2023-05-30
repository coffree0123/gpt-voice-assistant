import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import WeekScheduler from './WeekScheduler.jsx'
import './index.css'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
import { Layout } from 'antd';
import SiderMenu from './SiderMenu';


ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <Router>
    <Layout style={{ height: "100%" }}>
      <SiderMenu />
      
        <Routes>
          <Route exact path="/" element={<App />}>
          </Route>
          <Route path="/weekly-calendar" element={<WeekScheduler />}>
          </Route>
        </Routes>
    </Layout>
    </Router>
  
  </React.StrictMode>,
)
