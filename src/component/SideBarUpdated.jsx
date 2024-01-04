import React from "react";
import logo from "/logo.jpg";
import Avatar from "react-avatar";
import { FaMessage } from "react-icons/fa6";
import { faSearch } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

const SideBarUpdated = () => {
  const imageSources = [logo, logo, logo, logo, logo, logo]; // Array of image sources
  const chatUsers = [
    {
      src: logo,
      desc1: "47535785834",
      desc2: "cb1be95",
      desc3: "WORKFLOWAI",
    },
    {
      src: logo,
      desc1: "47535785834",
      desc2: "cb1be95",
      desc3: "WORKFLOWAI",
    },
  ];
  return (
    <div className="flex gap-7  ">
      <div className="fixed top-0 left-0 h-screen w-16 flex flex-col items-center z-50">
        <div className="rounded-full  ">
          <FaMessage className="w-10 text-green-500 rounded-md my-4 h-10" />
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

      <div className="flex flex-col gap-6 pt-7 bg-white rounded-lg px-4">
        <h1 className="font-bold">WORKFLOWAI</h1>
        <div className="max-w-md mx-auto px-2 flex items-center bg-gray-200 rounded-sm">
          <input
            type="text"
            className="font-semibold placeholder-gray-400 bg-transparent focus:outline-none p-1"
            placeholder="Find a chat"
          />

          <FontAwesomeIcon icon={faSearch} className="text-gray-400 pr-1" />
        </div>

        {chatUsers.map((item, index) => (
          <div className="flex gap-3 items-center mb-2" key={index}>
            <img
              src="avatar.jpg"
              className="w-10 h-10 rounded-full mb-4 bg-yellow-500"
              alt={`User ${index}`}
            />

            <div>
              <p className="text-sm font-semibold">{item?.desc1} </p>
              <p className="text-sm font-semibold my-0.5">{item?.desc2} </p>
              <p className="text-xs font-semibold">{item?.desc3} </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default SideBarUpdated;
