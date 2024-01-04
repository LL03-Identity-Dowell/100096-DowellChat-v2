import LoginPage from "./pages/LoginPage";
import { useState } from "react";
import Dashboard from "./pages/Dashboard";
import Avatar from "react-avatar";
import { MdVideoCall } from "react-icons/md";
import { IoCall } from "react-icons/io5";
import SideBarUpdated from "./component/SideBarUpdated";
import SearchSection from "./component/SearchSection";
// import logo from "logo.jpg"

export default function App() {
  const [isOpen, setIsOpen] = useState(false);

  const toggleSection = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div className="h-screen flex flex-row">
      <SideBarUpdated />
      <div className="grid grid-cols-10 w-full">
        {isOpen && (
          <SearchSection isOpen={isOpen} />
        )}

        <div className={`${isOpen ? 'col-span-8' : 'col-span-10'}`}>
          <div className="flex justify-between p-4 border-gray-700 bg-[#F1F3F4]">
            <div>
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
                className="w-12 h-12"
                onClick={toggleSection}
              >
                <path d="M3 12h18M3 6h18M3 18h18"></path>
              </svg>
            </div>
            <div className="flex ">
              <img
                src="avatar.jpg"
                alt="Rounded Image"
                className="w-16 h-16 rounded-full"
              />
              <div className="font-bold ml-3 mt-4 hidden md:block">
                WORKFLOW AI
              </div>{" "}
            </div>

            <div className="flex space-x-2 md:space-x-4 lg:space-x-6">
              <div className="hidden md:block">
                <MdVideoCall className="w-12 h-12 text-xl" />
              </div>
              <div className="hidden md:block">
                <IoCall className="w-10 h-10 text-xl" />
              </div>
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
                className="w-10 h-10"
              >
                <circle cx="12" cy="12" r="1"></circle>
                <circle cx="12" cy="5" r="1"></circle>
                <circle cx="12" cy="19" r="1"></circle>
              </svg>
            </div>
          </div>
        </div>
      </div>

      {/* <div className="">
      <div className={`col-span-3 bg-white ${isOpen ? "block" : "hidden"}`}>
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
    </div> */}

      {/* <div className={`col-span-${columnSpanClass} bg-white`}>
        <div className="flex     border-gray-700 bg-gray-100 justify-between p-4">
          <div>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
              className="w-12 h-12"
              onClick={toggleSection}
            >
              <path d="M3 12h18M3 6h18M3 18h18"></path>
            </svg>
          </div>
          <div className="flex ">
            <img
              src="avatar.jpg"
              alt="Rounded Image"
              className="w-16 h-16 rounded-full"
            />
            <div className="font-bold ml-3 mt-4 hidden md:block">
              WORKFLOW AI
            </div>{" "}
          </div>

          <div className="flex space-x-2 md:space-x-4 lg:space-x-6">
            <div className="hidden md:block">
              <MdVideoCall className="w-12 h-12 text-xl" />
            </div>
            <div className="hidden md:block">
              <IoCall className="w-10 h-10 text-xl" />
            </div>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              className="w-10 h-10"
            >
              <circle cx="12" cy="12" r="1"></circle>
              <circle cx="12" cy="5" r="1"></circle>
              <circle cx="12" cy="19" r="1"></circle>
            </svg>
          </div>
        </div>
      </div> */}

      {/* The searching section */}
      {/* <div>
      <SearchSection isOpen={columnSpanClass}/>

      </div> */}

      {/* Chatting Section */}
      {/* <div className={`col-span-${columnSpanClass} bg-white`}>
        <div className="flex     border-gray-700 bg-gray-100 justify-between p-4">
          <div>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
              className="w-12 h-12"
              onClick={toggleSection}
            >
              <path d="M3 12h18M3 6h18M3 18h18"></path>
            </svg>
          </div>
          <div className="flex ">
            <img
              src="avatar.jpg"
              alt="Rounded Image"
              className="w-16 h-16 rounded-full"
            />
            <div className="font-bold ml-3 mt-4 hidden md:block">
              WORKFLOW AI
            </div>{" "}
          </div>

          <div className="flex space-x-2 md:space-x-4 lg:space-x-6">
            <div className="hidden md:block">
              <MdVideoCall className="w-12 h-12 text-xl" />
            </div>
            <div className="hidden md:block">
              <IoCall className="w-10 h-10 text-xl" />
            </div>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              className="w-10 h-10"
            >
              <circle cx="12" cy="12" r="1"></circle>
              <circle cx="12" cy="5" r="1"></circle>
              <circle cx="12" cy="19" r="1"></circle>
            </svg>
          </div>
        </div>
      </div> */}
    </div>
  );
}
