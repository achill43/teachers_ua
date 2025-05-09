import React from 'react';
import './App.css';
import { Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import AboutUs from "./pages/AboutUs";
import NotFound from "./pages/NotFound";
import Login from './pages/Login';
import Header from './components/Header';
function App() {
  return (
    <div className="App">
      <div className="header">
        <Header/>
      </div>
      <div className="content">
      <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/about" element={<AboutUs />} />
            <Route path="*" element={<NotFound />} />
      </Routes>
      </div>
    </div>
  );
}

export default App;
