import React, { Component, Fragment } from 'react';
// import axios from 'axios';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import { routes } from './routes/index';
import Home from './pages/Home/Home';
import Order from './pages/Order/Order';
import HeaderComponent from './components/HeaderComponent/HeaderComponent';
import DefaultComponent from './components/DefaultComponent/DefaultComponent';

function App() {
  return (
    <div>
      <Router>
        <div className="App">
          <Routes>
            {/* <Route path="/" element={<Home />} />
          <Route path="order" element={<Order />} /> */}
            {routes.map((route) => {
              const Page = route.page;
              const Layout = route.isShowHeader ? DefaultComponent : Fragment;

              return (
                <Route
                  key={route.path}
                  path={route.path}
                  element={
                    <Layout>
                      <Page />
                    </Layout>
                  }
                />
              );
            })}
          </Routes>
        </div>
      </Router>
    </div>
  );
}

export default App;
