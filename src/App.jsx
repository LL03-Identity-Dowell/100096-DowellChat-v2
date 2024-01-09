import { useState } from "react";
import ChatSection from "./component/ChatSection";
import SideBar from "./component/SideBar";

export default function App() {
  const [isOpen, setIsOpen] = useState(true);
  const handleSideBarToggle = () => {
    setIsOpen(!isOpen);
  };
  return (
    <div className="h-screen w-screen flex bg-gray-300">
      <SideBar
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
