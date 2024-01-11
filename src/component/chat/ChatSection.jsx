import { useState, useRef, useEffect } from "react";
import { MdVideoCall } from "react-icons/md";
import { IoCall, IoMenuSharp } from "react-icons/io5";
import ChatMessage from "./ChatMessage";
import dummyImage from "../../assets/dummy-image-green.jpg";
import { FaEllipsisVertical } from "react-icons/fa6";
import { IoMdSend } from "react-icons/io";
import { MdOutlineMenuOpen, MdOutlineAttachFile } from "react-icons/md";

const messages = [
  { isSender: true, content: "Hello there!" },
  { isSender: false, content: "Hi! How are you?" },
  { isSender: true, content: "I'm doing well, thanks!" },
  { isSender: false, content: "That's great to hear!" },
  { isSender: true, content: "What have you been up to?" },
  { isSender: false, content: "Just working on some projects. How about you?" },
  { isSender: true, content: "I've been busy too, lots of meetings." },
  {
    isSender: false,
    content: "Ah, the usual work stuff. Anything exciting happening?",
  },
  { isSender: true, content: "Not much, just trying to stay productive." },
  { isSender: true, content: "Hello there!" },
  { isSender: false, content: "Hi! How are you?" },
  { isSender: true, content: "I'm doing well, thanks!" },
  { isSender: false, content: "That's great to hear!" },
  { isSender: true, content: "What have you been up to?" },
  { isSender: false, content: "Just working on some projects. How about you?" },
  { isSender: true, content: "I've been busy too, lots of meetings." },
  {
    isSender: false,
    content: "Ah, the usual work stuff. Anything exciting happening?",
  },
  { isSender: true, content: "Not much, just trying to stay productive." },
  { isSender: true, content: "Hello there!" },
  { isSender: false, content: "Hi! How are you?" },
  { isSender: true, content: "I'm doing well, thanks!" },
  { isSender: false, content: "That's great to hear!" },
  { isSender: true, content: "What have you been up to?" },
  { isSender: false, content: "Just working on some projects. How about you?" },
  { isSender: true, content: "I've been busy too, lots of meetings." },
  {
    isSender: false,
    content: "Ah, the usual work stuff. Anything exciting happening?",
  },
  { isSender: false, type: "image", imagePath: dummyImage },

  { isSender: true, content: "Not much, just trying to stay productive." },
];

const ChatSection = ({ isOpen, setIsOpen, handleSideBarToggle }) => {
  const scrollContainerRef = useRef(null);
  const [chatInput, setChatInput] = useState("");

  useEffect(() => {
    if (scrollContainerRef.current) {
      scrollContainerRef.current.scrollTop =
        scrollContainerRef.current.scrollHeight;
    }
  }, [messages]);
  

  return (
    <div className={`ml-3 flex flex-col max-h-screen w-full ${isOpen && 'hidden md:flex'}`}>
      <div className="flex justify-between items-center p-4 bg-[#F1F3F4] border-b-2 border-gray-300 rounded-t-3xl">
        <button className="cursor-pointer" onClick={handleSideBarToggle}>
          {isOpen ? (
            <MdOutlineMenuOpen className="w-6 md:w-10 h-10 " />
          ) : (
            <IoMenuSharp className="w-6 md:w-10 h-10  " />
          )}
        </button>

        <div className="inline-flex items-start">
          <img
            src="avatar.jpg"
            alt="Rounded Image"
            className="w-10 md:w-16 rounded-full"
          />
          <div className="font-bold ml-3 mt-4 hidden md:block uppercase">
            WORKFLOW AI
          </div>
        </div>

        <div className="flex items-center space-x-3 md:space-x-4 lg:space-x-6">
          <MdVideoCall className="w-6 md:w-10 h-10 text-xl" />
          <IoCall className="w-4 md:w-8  h-8 text-xl" />
          <FaEllipsisVertical className="w-4 md:w-8 h-6 md:h-8 " />
        </div>
      </div>

      <section
        ref={scrollContainerRef}
        className="h-[80%] flex-grow overflow-y-auto bg-white px-2"
      >
        <div className="flex flex-col space-y-2 justify-end">
          {messages.map((message, index) => (
            <ChatMessage key={index} message={message} />
          ))}
        </div>
      </section>

      <div className="relative flex items-center p-4 bg-white">
        <input
          type="text"
          placeholder="Type here ..."
          value={chatInput}
          onChange={(e) => setChatInput(e.target.value)}
          className="w-full rounded-lg border border-gray-300 px-4 py-2"
        />
        <MdOutlineAttachFile className="absolute  text-gray-500 hover:text-gray-700 pt-1 right-32 h-10 w-6 cursor-pointer transform rotate-12 origin-center" />
        <button className="ml-2 rounded-lg bg-blue-500 px-4 py-2 text-white inline-flex items-center">
          <span>Send</span>
          <IoMdSend className="ml-2 text-white" />
        </button>
      </div>
    </div>
  );
};

export default ChatSection;
