import logo from './logo.svg';
import './App.css';
import * as Realm from "realm-web";
import AskLeafy from './_pages/AskLeafy/AskLeafy';
import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Navbar from './_components/navBar/Navbar';

function App() {

  // Add your App ID
  //const app = new Realm.App({ id: APP_ID });

  return (
    <div className="App">
      <header className="App-header">

        <BrowserRouter>
        <Navbar></Navbar>
          <Routes>
            <Route path="/askLeafy" element={<AskLeafy />} />
          </Routes>
        </BrowserRouter>
      </header>
    </div>
  );
}

export default App;
