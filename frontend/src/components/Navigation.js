import React from 'react';
import { Link, useLocation } from 'react-router-dom';

function Navigation() {
  const location = useLocation();

  const navItems = [
    { path: '/', label: 'Dashboard' },
    { path: '/revenue', label: 'Revenue' },
    { path: '/expenses', label: 'Expenses' },
    { path: '/customers', label: 'Customers' },
    { path: '/products', label: 'Products' },
    { path: '/ai-insights', label: 'AI Insights' }
  ];

  return (
    <nav className="navigation">
      {navItems.map(item => (
        <Link 
          key={item.path}
          to={item.path} 
          className={location.pathname === item.path ? 'nav-link active' : 'nav-link'}
        >
          {item.label}
        </Link>
      ))}
    </nav>
  );
}

export default Navigation;