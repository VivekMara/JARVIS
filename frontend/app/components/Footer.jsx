import React from 'react';

const Footer = () => {
  return (
    <footer className="bg-gray-950 py-10 px-6 text-gray-400 text-center">
      <div className="container mx-auto">
        <div className="flex justify-center space-x-8 mb-6">
          <a href="#" className="hover:text-white transition duration-300">Privacy Policy</a>
          <a href="#" className="hover:text-white transition duration-300">Terms of Service</a>
          <a href="#" className="hover:text-white transition duration-300">Support</a>
        </div>
        <p className="text-sm">&copy; {new Date().getFullYear()} Jarvis AI. All rights reserved.</p>
        <p className="text-xs mt-2">Designed with ❤️ using React & Tailwind CSS</p>
      </div>
    </footer>
  );
};

export default Footer;