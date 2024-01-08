// // import React from "react";
// import logo from "/logo.jpg";
// import { FaMessage } from "react-icons/fa6";
// import { faSearch } from "@fortawesome/free-solid-svg-icons";
// import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
// import { useState } from "react";

// const SideBarUpdated = () => {
//   const [activeBorder, setActiveBorder] = useState(0);
//   const imageSources = [FaMessage, logo, logo, logo, logo, logo, logo]; // Array of image sources
//   const chatUsers = [
//     {
//       src: logo,
//       desc1: "47535785834",
//       desc2: "cb1be95",
//       desc3: "WORKFLOWAI",
//     },
//     {
//       src: logo,
//       desc1: "47535785834",
//       desc2: "cb1be95",
//       desc3: "WORKFLOWAI",
//     },
//   ];

//   // ===========All Event Handlers=======
//   const isActiveImg = (index) => {
//     setActiveBorder(index);
//   };
//   return (
//     <div className="flex">
//       {console.log(activeBorder)}
//       <div className=" top-0 left-0 h-screen py-4  flex flex-col gap-4 px-[15px] items-center z-50">
//         <div className="absolute bottom-0 left-0 w-full h-1 bg-gray-500"></div>

//         {imageSources.map((Element, index) =>
//           typeof Element === "function" ? (
//             <div key={index} className="relative h-[40px]">
//               <Element
//                 onClick={() => isActiveImg(index)}
//                 className={`cursor-pointer w-10 text-green-500 rounded-md  h-10 `}
//               />

//               {activeBorder === index && (
//                 <p className="cursor-pointer w-[6px] h-[80%] bg-green-500 absolute left-[-15px] rounded-r-[100px]  top-[2px]"></p>
//               )}

//               {activeBorder === index && (
//                 <p className="cursor-pointer w-full h-[2px] bg-black absolute left-0 rounded-r-[100px]  bottom-[-7px]"></p>
//               )}
//             </div>
//           ) : (
//             <div className="relative h-[40px]" key={index}>
//               <img
//                 onClick={() => isActiveImg(index)}
//                 src={Element}
//                 alt={`Logo ${index}`}
//                 className={`cursor-pointer w-10 h-10 rounded-full `}
//               />
//               {activeBorder === index && (
//                 <p className=" w-[6px] h-[80%] bg-green-500 absolute left-[-15px] rounded-r-[100px]  top-[2px]"></p>
//               )}
//               {activeBorder === index && (
//                 <p className=" w-full h-[2px] bg-black absolute left-0 rounded-r-[100px]  bottom-[-7px]"></p>
//               )}
//             </div>
//           )
//         )}
//         {/* Your SideBarUpdated content */}
//       </div>

//       <div className="flex flex-col gap-4 pt-7 bg-white rounded-lg px-4">
//         <h1 className="font-bold">WORKFLOWAI</h1>
//         <div className="max-w-md mx-auto px-2 flex items-center bg-gray-200 rounded-sm">
//           <input
//             type="text"
//             className="font-semibold placeholder-gray-400 bg-transparent focus:outline-none p-1"
//             placeholder="Find a chat"
//           />

//           <FontAwesomeIcon icon={faSearch} className="text-gray-400 pr-1" />
//         </div>

//         {chatUsers.map((item, index) => (
//           <div className="flex gap-3 items-center mb-2" key={index}>
//             <img
//               src="avatar.jpg"
//               className="w-10 h-10 rounded-full mb-4 bg-yellow-500"
//               alt={`User ${index}`}
//             />

//             <div>
//               <p className="text-sm font-semibold">{item?.desc1} </p>
//               <p className="text-sm font-semibold my-0.5">{item?.desc2} </p>
//               <p className="text-xs font-semibold">{item?.desc3} </p>
//             </div>
//           </div>
//         ))}
//       </div>
//     </div>
//   );
// };

// export default SideBarUpdated;

// ============

// import React from "react";
import logo from "/logo.jpg";
import { FaMessage } from "react-icons/fa6";
import { faSearch } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { useState } from "react";

const SideBarUpdated = ({ isOpen, setIsOpen }) => {
  const [activeBorder, setActiveBorder] = useState(0);
  const imageSources = [FaMessage, logo, logo, logo, logo, logo, logo]; // Array of image sources
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

  // ===========All Event Handlers=======
  const isActiveImg = (index) => {
    setActiveBorder(index);
  };
  return (
    <div className="flex">
      <div className="  top-0 left-0 h-screen py-4  flex flex-col gap-4 px-[15px] items-center z-50">
        {/* <div className="absolute bottom-0 left-0 w-full h-1 bg-gray-500"></div>  */}

        {imageSources.map((Element, index) =>
          typeof Element === "function" ? (
            <div key={index} className="relative h-[40px]">
              <Element
                onClick={() => isActiveImg(index)}
                className={`cursor-pointer w-10 text-green-500 rounded-md  h-10 `}
              />

              {activeBorder === index && (
                <p className="cursor-pointer w-[6px] h-[80%] bg-green-500 absolute left-[-15px] rounded-r-[100px]  top-[2px]"></p>
              )}

              {activeBorder === index && (
                <p className="cursor-pointer w-full h-[2px] bg-[#94a3b8] absolute left-0 rounded-r-[100px]  bottom-[-7px]"></p>
              )}
            </div>
          ) : (
            <div className="relative h-[40px]" key={index}>
              <img
                onClick={() => isActiveImg(index)}
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
        )}
        {/* Your SideBarUpdated content */}
      </div>

      {isOpen && (
        <div
          className={`max-[600px]:w-40 flex flex-col gap-4 pt-7 bg-white rounded-lg max-[600px]:px-2 px-4 `}
        >
          <h1 className="font-bold">WORKFLOWAI</h1>
          <div className="px-2 relative items-center bg-gray-200 rounded-sm">
            <input
              type="text"
              className="font-semibold placeholder-gray-400 bg-transparent focus:outline-none p-1"
              placeholder="Find a chat"
            />
            <FontAwesomeIcon
              icon={faSearch}
              className="text-gray-400 pr-1 absolute top-2/4 right-1 translate-y-[-50%]"
            />
          </div>

          {chatUsers.map((item, index) => (
            <div className="flex gap-3 items-center mb-2" key={index}>
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
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default SideBarUpdated;
