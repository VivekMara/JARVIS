import React from 'react';

const Header = () => {
  return (
    <header className="absolute top-0 left-0 right-0 z-50 p-6">
      <nav className="container mx-auto flex justify-between items-center">
        <div className="text-3xl font-extrabold text-white tracking-wider">
          JARVIS
        </div>
        <ul className="flex space-x-8">
          <li><a href="#features" className="text-gray-300 hover:text-white transition duration-300">Features</a></li>
          <li><a href="#how-it-works" className="text-gray-300 hover:text-white transition duration-300">How It Works</a></li>
          <li><a href="#pricing" className="text-gray-300 hover:text-white transition duration-300">Pricing</a></li>
          <li><a href="#contact" className="text-gray-300 hover:text-white transition duration-300">Contact</a></li>
        </ul>
        <button className="px-6 py-2 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-full shadow-lg hover:from-blue-600 hover:to-purple-700 transition duration-300 transform hover:scale-105">
          Get Started
        </button>
      </nav>
    </header>
  );
};

export default Header;