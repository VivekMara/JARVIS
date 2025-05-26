import React from 'react';

const Hero = () => {
  return (
    <section className="relative h-screen flex items-center justify-center text-center p-6 bg-cover bg-center" style={{ backgroundImage: 'url("/images/hero-bg.jpg")' }}>
      {/* Overlay for better text readability and darker aesthetic */}
      <div className="absolute inset-0 bg-black opacity-70"></div>
      {/* Glowing Sphere/Element - conceptual, might be a SVG or a sophisticated CSS animation */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-blue-500 rounded-full mix-blend-screen filter blur-3xl opacity-30 animate-pulse"></div>
      <div className="absolute top-1/3 right-1/4 w-80 h-80 bg-purple-600 rounded-full mix-blend-screen filter blur-3xl opacity-25 animate-pulse delay-500"></div>

      <div className="relative z-10 max-w-4xl mx-auto">
        <h1 className="text-6xl font-extrabold text-white leading-tight mb-6 animate-fade-in-up">
          Your Personal AI Co-pilot: <span className="bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-500">JARVIS</span>
        </h1>
        <p className="text-xl text-gray-300 mb-10 animate-fade-in-up delay-200">
          Unleash unparalleled productivity, intelligence, and control with Jarvis. Your ultimate AI assistant for every aspect of your life.
        </p>
        <div className="flex justify-center space-x-6 animate-fade-in-up delay-400">
          <button className="px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-700 text-white font-semibold rounded-full shadow-2xl hover:from-blue-700 hover:to-purple-800 transition duration-300 transform hover:scale-105">
            Explore Features
          </button>
          <button className="px-8 py-4 bg-gray-800 text-gray-200 font-semibold rounded-full shadow-xl border border-gray-700 hover:bg-gray-700 hover:text-white transition duration-300 transform hover:scale-105">
            Watch Demo
          </button>
        </div>
      </div>
      {/* Optional: A subtle scroll indicator */}
      <div className="absolute bottom-10 animate-bounce">
        <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 14l-7 7m0 0l-7-7m7 7V3"></path>
        </svg>
      </div>
    </section>
  );
};

export default Hero;