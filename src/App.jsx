import { useState } from "react";
import SideBar from "./component/SideBar";
import ChatSection from "./component/ChatSection";


export default function App() {

  const [isOpen, setIsOpen] = useState(true);

  return (
    <div className="h-screen flex flex-row bg-gray-300">
      <SideBar isOpen={isOpen}/>
      <div className="w-full">
        <ChatSection isOpen={isOpen} setIsOpen={setIsOpen}/>
      </div>
    </div>
  );
}
