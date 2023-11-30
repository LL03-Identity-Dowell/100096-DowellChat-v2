import React, { useEffect } from "react";
import { RedButton } from "../red-button/RedButton";

export const AcceptedVideoCall = ({
  localStream,
  leaveCall,
  localStreamRef,
  remoteStreamRef,
}) => {
  useEffect(() => {
    if (localStreamRef.current) {
      localStreamRef.current.srcObject = localStream;
    }
  }, [localStream, localStreamRef]);

  return (
    <div className=" flex flex-col w-1/2 items-center shadow-lg rounded-lg border border-gray-300 bg-white">
      <div className="relative w-full">
        <video
          ref={localStreamRef}
          className="absolute border-2 border-white object-cover w-56 h-48 rounded-md shadow-md bottom-4 right-8"
          id="video-1"
          autoPlay
          playsInline
          muted
        />
        <video
          ref={remoteStreamRef}
          className="w-full rounded-t-md object-cover"
          id="video-2"
          autoPlay
          playsInline
        />
      </div>
      <div className="flex w-full py-2 justify-center items-center">
        <RedButton title="End" leaveCall={leaveCall} />
      </div>
    </div>
  );
};
