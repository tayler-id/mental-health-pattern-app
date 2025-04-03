import React from 'react';

const Footer = () => {
  return (
    <footer className="app-footer">
      <div className="app-footer-content">
        <p className="copyright">
          &copy; {new Date().getFullYear()} Mental Health Pattern Recognition Assistant
        </p>
        <p className="app-version">
          Web Version 0.1.0
        </p>
      </div>
    </footer>
  );
};

export default Footer;
