import { useState } from "react";
import SideBarUpdated from "./component/SideBarUpdated";
import SearchSection from "./component/SearchSection";
import ChatSection from "./component/ChatSection";

// import logo from "logo.jpg"



export default function App() {

  const [isOpen, setIsOpen] = useState(true);

  return (
    <div className="h-screen flex flex-row bg-gray-300">
      <SideBarUpdated />
      <div className="grid grid-cols-10 w-full ">
        {isOpen && (
          <SearchSection isOpen={isOpen} />
        )}

        <ChatSection isOpen={isOpen} setIsOpen={setIsOpen}/>
      </div>
    </div>
  );
}
