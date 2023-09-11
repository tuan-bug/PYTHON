import { Col } from 'antd';
import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import { WapperHeader } from './style';
import Search from 'antd/es/transfer/search';
import { HeartOutlined, ShoppingCartOutlined } from '@ant-design/icons';

function HeaderComponent() {
  return (
    <nav className="navbar navbar-expand-lg navbar-light bg-light">
      <div className="container">
        <a className="navbar-brand" href="#">
          My App
        </a>
        <button
          className="navbar-toggler"
          type="button"
          data-toggle="collapse"
          data-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav">
            <li className="nav-item active">
              <a className="nav-link" href="#">
                Home
              </a>
            </li>
            <li className="nav-item">
              <a className="nav-link" href="#">
                About
              </a>
            </li>
            <li className="nav-item">
              <a className="nav-link" href="#">
                Services
              </a>
            </li>
            <li className="nav-item">
              <a className="nav-link" href="#">
                Contact
              </a>
            </li>
          </ul>
        </div>

        {/* Thêm ô tìm kiếm */}
        <form className="d-flex form-inline my-2 my-lg-0 ml-auto">
          <input className="form-control mr-sm-2" type="search" placeholder="Search" aria-label="Search" />
          <button className="btn btn-outline-success my-2 my-sm-0" type="submit">
            Search
          </button>
        </form>

        {/* Thêm biểu tượng giỏ hàng */}
        <ul className="navbar-nav ml-2">
          <li className="nav-item">
            <a className="nav-link" href="#">
              tim này
              <i className="fa fa-shopping-cart"></i>
            </a>
          </li>
        </ul>
      </div>
    </nav>
  );
}

export default HeaderComponent;
