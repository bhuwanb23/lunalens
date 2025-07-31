import React from 'react';

const Background = () => {
  return (
    <>
      {/* Stars background */}
      <div className="stars absolute inset-0 opacity-70"></div>

      {/* Moon background */}
      <div 
        id="moon-background"
        className="absolute top-20 right-20 w-96 h-96 rounded-full bg-gradient-to-br from-gray-300 via-gray-400 to-gray-500 moon-glow opacity-20 floating"
      ></div>

      {/* Earth glow */}
      <div 
        id="earth-glow"
        className="absolute bottom-10 left-10 w-32 h-32 rounded-full bg-gradient-to-br from-blue-400 to-green-400 opacity-30 blur-lg"
      ></div>
    </>
  );
};

export default Background; 