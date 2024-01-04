import { useState, useRef, useEffect } from "react";
import { MdVideoCall } from "react-icons/md";
import { IoCall } from "react-icons/io5";
import SideBarUpdated from "./component/SideBarUpdated";
import SearchSection from "./component/SearchSection";
import ChatMessage from "./component/ChatMessage";
import dummyImage from './assets/dummy-image-green.jpg'
// import logo from "logo.jpg"

const messages = [
  { isSender: true, content: "Hello there!" },
  { isSender: false, content: "Hi! How are you?" },
  { isSender: true, content: "I'm doing well, thanks!" },
  { isSender: false, content: "That's great to hear!" },
  { isSender: true, content: "What have you been up to?" },
  { isSender: false, content: "Just working on some projects. How about you?" },
  { isSender: true, content: "I've been busy too, lots of meetings." },
  { isSender: false, content: "Ah, the usual work stuff. Anything exciting happening?" },
  { isSender: true, content: "Not much, just trying to stay productive." },
  { isSender: true, content: "Hello there!" },
  { isSender: false, content: "Hi! How are you?" },
  { isSender: true, content: "I'm doing well, thanks!" },
  { isSender: false, content: "That's great to hear!" },
  { isSender: true, content: "What have you been up to?" },
  { isSender: false, content: "Just working on some projects. How about you?" },
  { isSender: true, content: "I've been busy too, lots of meetings." },
  { isSender: false, content: "Ah, the usual work stuff. Anything exciting happening?" },
  { isSender: true, content: "Not much, just trying to stay productive." },
  { isSender: true, content: "Hello there!" },
  { isSender: false, content: "Hi! How are you?" },
  { isSender: true, content: "I'm doing well, thanks!" },
  { isSender: false, content: "That's great to hear!" },
  { isSender: true, content: "What have you been up to?" },
  { isSender: false, content: "Just working on some projects. How about you?" },
  { isSender: true, content: "I've been busy too, lots of meetings." },
  { isSender: false, content: "Ah, the usual work stuff. Anything exciting happening?" },
  { isSender: false, type: 'image', imagePath: dummyImage },

  { isSender: true, content: "Not much, just trying to stay productive." },
];


export default function App() {
  const [isOpen, setIsOpen] = useState(true);
  const scrollContainerRef = useRef(null);
  const [chatInput, setChatInput] = useState('');

  const toggleSection = () => {
    setIsOpen(!isOpen);
  };

  useEffect(() => {
    if (scrollContainerRef.current) {
      scrollContainerRef.current.scrollTop = scrollContainerRef.current.scrollHeight;
    }
  }, []);

  return (
    <div className="h-screen flex flex-row bg-gray-300">
      <SideBarUpdated />
      <div className="grid grid-cols-10 w-full ">
        {isOpen && (
          <SearchSection isOpen={isOpen} />
        )}

        <div className={`${isOpen ? 'col-span-8' : 'col-span-10'} ml-3 flex flex-col max-h-screen`}>
          <div className="flex justify-between p-4 bg-[#F1F3F4] border-b-2 border-gray-300 rounded-t-3xl">
            <div>
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
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

          <section ref={scrollContainerRef}  className="flex-grow overflow-y-scroll bg-white px-2">
            <div className="flex flex-col space-y-2 justify-end">
              {
                messages.map((message, index) => (
                  <ChatMessage key={index} message={message}/>
                ))
              }
            </div>
          </section>

          <div className="flex items-center p-4 bg-white">
            <input type="text" placeholder="Type here ..." value={chatInput} onChange={() => setChatInput(chatInput)} className="w-full rounded-lg border border-gray-300 px-4 py-2"/>
            <button className="ml-2 rounded-lg bg-blue-500 px-4 py-2 text-white">Send</button>
          </div>
        </div>
      </div>
    </div>
  );
}
