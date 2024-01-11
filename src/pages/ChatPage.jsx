import { useEffect, useState } from "react";
import ChatSection from "../component/chat/ChatSection";
import SideBar from "../component/chat/SideBar";
import { socketInstance } from "../services/core-providers-di";
import { useDispatch, useSelector } from "react-redux";
import { socketSlice } from "../redux/features/chat/socket-slice";


const ChatPage = () => {
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
    )
}

export default ChatPage;