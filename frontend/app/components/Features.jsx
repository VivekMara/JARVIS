import React from 'react';

const featuresData = [
  {
    icon: (
      <svg className="w-12 h-12 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9.75 17L12 21.75l2.25-4.75M21 12H3m12 6h-6m6-12h-6"></path>
      </svg>
    ),
    title: "Intelligent Automation",
    description: "Automate repetitive tasks, schedule meetings, manage emails, and more with unparalleled precision and efficiency."
  },
  {
    icon: (
      <svg className="w-12 h-12 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
      </svg>
    ),
    title: "Contextual Understanding",
    description: "Jarvis understands your needs and preferences, adapting its responses and actions based on context and past interactions."
  },
  {
    icon: (
      <svg className="w-12 h-12 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
      </svg>
    ),
    title: "Seamless Integration",
    description: "Connects effortlessly with your existing tools and platforms, including calendars, communication apps, and smart home devices."
  },
  {
    icon: (
      <svg className="w-12 h-12 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 11c0 1.657-3.582 3-8 3s-8-1.343-8-3 3.582-3 8-3 8 1.343 8 3z"></path>
      </svg>
    ),
    title: "Personalized Insights",
    description: "Gain valuable insights into your productivity, habits, and digital well-being, helping you optimize your workflow."
  },
];

const Features = () => {
  return (
    <section id="features" className="py-20 px-6 bg-gray-900">
      <div className="container mx-auto text-center">
        <h2 className="text-5xl font-extrabold text-white mb-16">
          Unleash the Power of <span className="bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-500">AI</span>
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-12">
          {featuresData.map((feature, index) => (
            <div
              key={index}
              className="bg-gray-800 p-8 rounded-xl shadow-2xl border border-gray-700 hover:border-blue-500 transition duration-300 transform hover:scale-105 group"
            >
              <div className="mb-6 flex justify-center">{feature.icon}</div>
              <h3 className="text-2xl font-bold text-white mb-4 group-hover:text-blue-400 transition duration-300">{feature.title}</h3>
              <p className="text-gray-400 leading-relaxed">{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Features;