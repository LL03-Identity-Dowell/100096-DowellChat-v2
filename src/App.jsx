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
    <div className="h-screen flex flex-row bg-gray-300">
      <SideBarUpdated />
      <div className="grid grid-cols-10 w-full ">
        {isOpen && (
          <SearchSection isOpen={isOpen} />
        )}

        <div className={`${isOpen ? 'col-span-8' : 'col-span-10'} ml-3 flex flex-col`}>
          <div className="flex justify-between p-4 bg-[#F1F3F4] border-b-2 border-gray-300 rounded-t-3xl">
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

          <section className="h-full bg-white">

          </section>
        </div>
      </div>
    </div>
  );
}
