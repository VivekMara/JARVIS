import React from 'react';

const CallToAction = () => {
  return (
    <section className="py-20 px-6 bg-gradient-to-r from-blue-700 to-purple-800 text-white text-center">
      <div className="container mx-auto max-w-3xl">
        <h2 className="text-5xl font-extrabold leading-tight mb-8">
          Ready to Experience the Future with Jarvis?
        </h2>
        <p className="text-xl opacity-90 mb-12">
          Join the revolution and elevate your daily life with the most advanced AI co-pilot.
        </p>
        <button className="px-10 py-5 bg-white text-blue-700 font-bold text-xl rounded-full shadow-2xl hover:bg-gray-100 hover:text-blue-800 transition duration-300 transform hover:scale-105">
          Get Started with Jarvis Today!
        </button>
      </div>
    </section>
  );
};

export default CallToAction;