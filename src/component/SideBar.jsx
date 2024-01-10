import logo from "/logo.jpg";
import { FaMessage } from "react-icons/fa6";
import { faL, faSearch } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { useEffect, useState } from "react";
import { USER_ID, socketInstance } from "../services/core-providers-di";
import { useSelector } from "react-redux";
import ProfileAvatar from "./common/ProfileAvatar";

const SideBar = ({ isOpen, setIsOpen }) => {
  const [servers, setServers] = useState([]);
  const [activeBorder, setActiveBorder] = useState(0);
  const isConnected  = useSelector((state) => state.socket.isConnected)
  const chatUsers = [
    {
      src: logo,
      desc1: "47535785834",
      desc2: "cb1be95",
      desc3: "WORKFLOWAI",
    },
    {
      src: logo,
      desc1: "47535785834",
      desc2: "cb1be95",
      desc3: "WORKFLOWAI",
    },
  ];

  useEffect(() => {
    if(isConnected) {
      socketInstance.emit('get_user_servers',{
        user_id: USER_ID
      })
    }
  }, [isConnected]);

  socketInstance.on('server_response', (data) => {
    if(data.status === 'success'){
      setServers(data.data);
    }else {
      setServers([])
    }
  })

  return (
    <div className="flex">
      <div className=" top-0 left-0 h-screen py-4  flex flex-col gap-4 px-[15px] items-center z-50">
        <div className="absolute bottom-0 left-0 w-full h-1 bg-gray-500"></div>

        <div className="relative h-[40px]">
              <FaMessage
                onClick={() => setActiveBorder(-1)}
                className={`cursor-pointer w-10 text-green-500 rounded-md  h-10 `}
              />
              {activeBorder === -1 && (
                <p className="cursor-pointer w-[6px] h-[80%] bg-green-500 absolute left-[-15px] rounded-r-[100px]  top-[2px]"></p>
              )}

              {activeBorder === -1 && (
                <p className="cursor-pointer w-full h-[2px] bg-[#94a3b8] absolute left-0 rounded-r-[100px]  bottom-[-7px]"></p>
              )}
        </div>

          {
            servers?.map(({name, id}, index) => (
              <div key={index}>
                <div className="relative h-[40px]" key={index} onClick={() => setActiveBorder(index)}>
                  <ProfileAvatar fullName={name} />
                  {activeBorder === index && (
                    <p className=" w-[6px] h-[80%] bg-green-500 absolute left-[-15px] rounded-r-[100px]  top-[2px]"></p>
                  )}
                  {activeBorder === index && (
                    <p className=" w-full h-[2px] bg-[#94a3b8] absolute left-0 rounded-r-[100px]  bottom-[-7px]"></p>
                  )}
                </div>
              </div>
            ))
          }

{/* 
        {
          servers.map(server, index) => ( )}
            <div className="relative h-[40px]" key={index}>
              <img
                onClick={() => setActiveBorder(index)}
                src={Element}
                alt={`Logo ${index}`}
                className={`cursor-pointer w-10 h-10 rounded-full `}
              />
              {activeBorder === index && (
                <p className=" w-[6px] h-[80%] bg-green-500 absolute left-[-15px] rounded-r-[100px]  top-[2px]"></p>
              )}
              {activeBorder === index && (
                <p className=" w-full h-[2px] bg-[#94a3b8] absolute left-0 rounded-r-[100px]  bottom-[-7px]"></p>
              )}
            </div>
          )
        ) */}
      </div>

      {isOpen && (
        <div className={`flex flex-col gap-4 pt-7 bg-white rounded-lg px-4 `}>
          <h1 className="font-bold">WORKFLOWAI</h1>
          <div className="max-w-md mx-auto px-2 flex items-center bg-gray-200 rounded-sm">
            <input
              type="text"
              className="font-semibold placeholder-gray-400 bg-transparent focus:outline-none p-1"
              placeholder="Find a chat"
            />

            <FontAwesomeIcon icon={faSearch} className="text-gray-400 pr-1" />
          </div>

          {chatUsers.map((item, index) => (
            <button className="flex gap-3 items-center mb-2" key={index} onClick={() => setIsOpen(false)}>
              <img
                src="avatar.jpg"
                className="w-10 h-10 rounded-full mb-4 bg-yellow-500"
                alt={`User ${index}`}
              />

              <div>
                <p className="text-sm font-semibold">{item?.desc1} </p>
                <p className="text-sm font-semibold my-0.5">{item?.desc2} </p>
                <p className="text-xs font-semibold">{item?.desc3} </p>
              </div>
            </button>
          ))}
        </div>
      )}
    </div>
  );
};

export default SideBar;
