import React from "react";
import { FaMessage } from "react-icons/fa6";

const SearchSection = ({ isOpen }) => {
  return (
      <div className={`col-span-2 bg-white   ${isOpen ? "block" : "hidden"} pl-4`}>
        <div className="mt-6 font-bold text-3xl"> WorkflowAI </div>
        <div
          className={`flex flex-col mt-12 mr-4 ${
            isOpen ? "block" : "hidden md:flex"
          }`}
        >
          <input
            type="text"
            className="border focus:outline-none md:mx-0 h-10 px-4 ml-[-2] bg-gray-100 w-[50%] sm:w-auto md:w-auto lg:w-[75%]"  
                      placeholder="  Find in Chat "
          />

          <div className="flex flex-col mt-8">
            <div className="flex my-4">
              <div>
                <img
                  src="avatar.jpg"
                  alt="Circle Image"
                  className="w-16 h-16 md:w-12 md:h-12 rounded-full"
                />
              </div>
              <div className="ml-4">
                <div className="grid grid-rows-2">
                  <div className="">
                    <span className="font-semibold">Id:</span> g77g8g8g888g
                  </div>

                  <div className="mt-1">
                    <span className="font-semibold">WORKFLOW AI</span>
                  </div>
                </div>
              </div>
            </div>

            <div className="flex my-4">
              <div>
                <img
                  src="avatar.jpg"
                  alt="Circle Image"
                  className="w-16 h-16 md:w-12 md:h-12 rounded-full"
                />
              </div>
              <div className="ml-4">
                <div className="grid grid-rows-2">
                  <div>
                    <span className="font-semibold">Id:</span> h90h9h9h099h
                  </div>
                  <div className="mt-1">
                    <span className="font-semibold">WORKFLOW AI</span>
                  </div>
                </div>
              </div>
            </div>

            <div className="flex my-4">
              <div>
                <img
                  src="avatar.jpg"
                  alt="Circle Image"
                  className="w-16 h-16 md:w-12 md:h-12 rounded-full"
                />
              </div>
              <div className="ml-4">
                <div className="grid grid-rows-2">
                  <div>
                    <span className="font-semibold">Id:</span> 565656565GAb
                  </div>
                  <div className="mt-1">
                    <span className="font-semibold">WORKFLOW AI</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
  );
};

export default SearchSection;