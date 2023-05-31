import React from 'react';
import { Layout, Menu } from 'antd';
import { Link } from 'react-router-dom';
import {
  HomeOutlined,
  CalendarOutlined,
} from '@ant-design/icons';
const { Sider } = Layout;

function getItem(label, key, icon, children, type, path) {
  return {
    key,
    icon,
    children,
    label,
    type,
    path
  };
}
const items = [
  getItem(<Link to="/">Home</Link>, '1', <HomeOutlined />),
  getItem(<Link to="/weekly-calendar">Calender</Link>, '2', <CalendarOutlined />),
];

const SiderMenu = () => (
  <Sider
    breakpoint="lg"
    collapsedWidth="0"
    width={256}
  // style={{ width: 512 }}
  >
    <div className="demo-logo-vertical" />
    <Menu

      theme="dark"
      mode="inline"
      defaultSelectedKeys={['1']}
      items={items}
    ></Menu>
  </Sider>
);

export default SiderMenu;