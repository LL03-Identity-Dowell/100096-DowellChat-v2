import { useEffect, useState } from "react";
import ChatSection from "./component/ChatSection";
import SideBar from "./component/SideBar";
import { socketInstance } from "./services/core-providers-di";
import { useDispatch, useSelector } from "react-redux";
import { socketSlice } from "./redux/features/chat/socket-slice";

export default function App() {
  const [isOpen, setIsOpen] = useState(true);
  const dispatch = useDispatch()
  const handleSideBarToggle = () => {
    setIsOpen(!isOpen);
  };

  useEffect(() => {
    socketInstance.on('connect', () => {
      dispatch(socketSlice.actions.setConnected({
        isConnected: true,
      }))
    })

    socketInstance.on('disconnect', () => {
      dispatch(socketSlice.actions.setConnected({
        isConnected: false,
      }))
    })
  }, [])

  return (
    <div className="h-screen flex bg-gray-300">
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
