import React from 'react';

const ImageUpload = ({ uploadedImage, handleImageUpload }) => {
  return (
    <section className="py-4 sm:py-6 px-4 sm:px-6">
      <div className="max-w-2xl sm:max-w-3xl mx-auto">
        <div className="bg-gradient-to-br from-gray-800 via-gray-700 to-gray-800 border-2 border-dashed border-orange-500/30 rounded-xl sm:rounded-2xl p-4 sm:p-6 text-center shadow-lg hover:shadow-orange-500/20 transition-all duration-300 transform hover:scale-[1.01]">
          <div className="w-10 h-10 sm:w-12 sm:h-12 bg-gradient-to-br from-orange-400 via-red-500 to-orange-600 rounded-lg sm:rounded-xl flex items-center justify-center mx-auto mb-3 sm:mb-4 shadow-lg hover:shadow-orange-500/50 transition-all duration-300 transform hover:scale-110">
            <i className="text-lg sm:text-xl text-white">
              <svg className="w-5 h-5 sm:w-6 sm:h-6" fill="currentColor" viewBox="0 0 512 512">
                <path d="M256 32c12.5 0 24.1 6.4 30.8 17L503.4 394.4c5.6 8.9 8.6 19.2 8.6 29.7c0 30.9-25 55.9-55.9 55.9H55.9C25 480 0 455 0 424.1c0-10.5 3-20.8 8.6-29.7L225.2 49c6.6-10.6 18.3-17 30.8-17zm65 192L256 120.4 176.9 246.5l18.3 24.4c6.4 8.5 19.2 8.5 25.6 0l25.6-34.1c6-8.1 15.5-12.8 25.6-12.8h49z" />
              </svg>
            </i>
          </div>
          <h3 className="text-lg sm:text-xl font-bold mb-2 sm:mb-3 bg-gradient-to-r from-gray-200 to-orange-300 bg-clip-text text-transparent">Upload Lunar Image</h3>
          <p className="text-gray-300 mb-4 sm:mb-5 text-sm sm:text-base leading-relaxed">Upload a lunar surface image for boulder and crater detection analysis</p>
          <input
            type="file"
            accept="image/*"
            onChange={handleImageUpload}
            className="hidden"
            id="image-upload"
          />
          <label
            htmlFor="image-upload"
            className="bg-gradient-to-r from-orange-500 via-red-600 to-orange-700 hover:from-orange-600 hover:via-red-700 hover:to-orange-800 px-4 sm:px-6 py-2 sm:py-3 rounded-lg sm:rounded-xl font-semibold transition-all duration-300 shadow-md hover:shadow-orange-500/50 cursor-pointer inline-block transform hover:scale-105 hover:-translate-y-1 text-sm sm:text-base"
          >
            <span className="flex items-center space-x-2">
              <svg className="w-4 h-4 sm:w-5 sm:h-5" fill="currentColor" viewBox="0 0 512 512">
                <path d="M256 32c12.5 0 24.1 6.4 30.8 17L503.4 394.4c5.6 8.9 8.6 19.2 8.6 29.7c0 30.9-25 55.9-55.9 55.9H55.9C25 480 0 455 0 424.1c0-10.5 3-20.8 8.6-29.7L225.2 49c6.6-10.6 18.3-17 30.8-17zm65 192L256 120.4 176.9 246.5l18.3 24.4c6.4 8.5 19.2 8.5 25.6 0l25.6-34.1c6-8.1 15.5-12.8 25.6-12.8h49z" />
              </svg>
              <span>Choose Image</span>
            </span>
          </label>
          {uploadedImage && (
            <div className="mt-4 sm:mt-5 animate-fade-in">
              <div className="relative inline-block">
                <img src={uploadedImage} alt="Uploaded" className="max-w-48 sm:max-w-64 mx-auto rounded-lg sm:rounded-xl shadow-lg border-2 border-green-500/30" />
                <div className="absolute -top-1 -right-1 w-5 h-5 sm:w-6 sm:h-6 bg-green-500 rounded-full flex items-center justify-center shadow-md">
                  <svg className="w-3 h-3 sm:w-4 sm:h-4 text-white" fill="currentColor" viewBox="0 0 448 512">
                    <path d="M438.6 105.4c12.5 12.5 12.5 32.8 0 45.3l-256 256c-12.5 12.5-32.8 12.5-45.3 0l-128-128c-12.5-12.5-12.5-32.8 0-45.3s32.8-12.5 45.3 0L160 338.7 393.4 105.4c12.5-12.5 32.8-12.5 45.3 0z" />
                  </svg>
                </div>
              </div>
              <p className="text-green-400 mt-2 sm:mt-3 text-sm sm:text-base font-semibold flex items-center justify-center">
                <svg className="w-4 h-4 sm:w-5 sm:h-5 mr-2" fill="currentColor" viewBox="0 0 448 512">
                  <path d="M438.6 105.4c12.5 12.5 12.5 32.8 0 45.3l-256 256c-12.5 12.5-32.8 12.5-45.3 0l-128-128c-12.5-12.5-12.5-32.8 0-45.3s32.8-12.5 45.3 0L160 338.7 393.4 105.4c12.5-12.5 32.8-12.5 45.3 0z" />
                </svg>
                Image uploaded successfully
              </p>
            </div>
          )}
        </div>
      </div>
    </section>
  );
};

export default ImageUpload; 