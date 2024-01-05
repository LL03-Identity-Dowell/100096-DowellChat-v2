import { useState } from "react";
import SideBar from "./component/SideBar";
import ChatSection from "./component/ChatSection";


export default function App() {

  const [isOpen, setIsOpen] = useState(true);

  return (
    <div className="h-screen flex bg-gray-300">
      <SideBar isOpen={isOpen} setIsOpen={setIsOpen}/>
      <ChatSection isOpen={isOpen} setIsOpen={setIsOpen}/>
    </div>
  );
}
