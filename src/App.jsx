import { useState } from "react";
// import SideBar from "./component/SideBar";
import ChatSection from "./component/ChatSection";
import SideBarUpdated from "./component/SidebarUpdate";

export default function App() {
  const [isOpen, setIsOpen] = useState(true);
  const handleSideBarToggle = () => {
    setIsOpen(!isOpen);
  };
  return (
    <div className="h-screen flex bg-gray-300">
      {/* <SideBar isOpen={isOpen} setIsOpen={setIsOpen} /> */}
      <SideBarUpdated
        isOpen={isOpen}
        setIsOpen={setIsOpen}
        handleSideBarToggle={handleSideBarToggle}
      />
      <ChatSection
        isOpen={isOpen}
        setIsOpen={setIsOpen}
        handleSideBarToggle={handleSideBarToggle}
      />
    </div>
  );
}
