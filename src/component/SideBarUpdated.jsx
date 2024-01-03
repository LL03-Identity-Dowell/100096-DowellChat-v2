import React from "react";
import logo from "/logo.jpg";
import { FaMessage } from "react-icons/fa6";

const SideBarUpdated = () => {
  const imageSources = [logo, logo, logo, logo, logo, logo]; // Array of image sources

  return (
    <div className="fixed top-0 left-0 h-screen w-16 bg-[#DCDCDC] flex flex-col items-center z-50">
      <div className="rounded-full  ">
        <FaMessage className="w-10 text-green-500    rounded-md my-4 h-10" />
      </div>
      <div className="absolute bottom-0 left-0 w-full h-1 bg-gray-500"></div>

      {imageSources.map((src, index) => (
        <img
          key={index}
          src={src}
          alt={`Logo ${index}`}
          className="w-10 h-10 rounded-full mb-4"
        />
      ))}
      {/* Your SideBarUpdated content */}
    </div>
  );
};

export default SideBarUpdated;
