import React from 'react';
import './App.css';
import { Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import AboutUs from "./pages/AboutUs";
import NotFound from "./pages/NotFound";
import SignIn from './pages/SignIn';
import SignUp from "./pages/SignUp";

import Header from './components/Header';
function App() {
  return (
    <div className="App">
      <header className="header">
        <Header/>
      </header>
      <main className="content">
      <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/sign_in" element={<SignIn />} />
            <Route path='sign_up' element={<SignUp/>} />
            <Route path="/about" element={<AboutUs />} />
            <Route path="*" element={<NotFound />} />
      </Routes>
      </main>
    </div>
  );
}

export default App;
