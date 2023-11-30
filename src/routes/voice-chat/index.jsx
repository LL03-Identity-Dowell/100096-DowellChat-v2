import { useRef, useState, useEffect } from "react";

import Peer from "simple-peer";

import io from "socket.io-client";

import { Call } from "../../components/call/Call";
import { OngoingCall } from "../../components/ongoing-call/OngoingCall";
import { IncomingCall } from "../../components/incoming-call/IncomingCall";
import { AcceptedCall } from "../../components/accepted-call/AcceptedCall";

let socket = io.connect("https://www.dowellchat.uxlivinglab.online/");
export const VoiceChat = () => {
  const [myId, setMyId] = useState("");
  const [localStream, setLocalStream] = useState(null);
  const [caller, setCaller] = useState();
  const [callerName, setCallerName] = useState("Ali");
  const [callerSignal, setCallerSignal] = useState();
  const [idToCall, setIdToCall] = useState();
  const [isCalling, setIsCalling] = useState(false);
  const [isRecievingCall, setIsRecievingCall] = useState(false);
  const [isCallAccepted, setIsCallAccepted] = useState(false);

  const remoteAudioRef = useRef(null);
  const connectionRef = useRef(null);

  useEffect(() => {
    socket = io.connect("https://www.dowellchat.uxlivinglab.online/");
  }, [myId]);

  socket.on("me", async (id) => {
    await getMediaStream();
    setMyId(id);
  });
  socket.on("callUser", (data) => {
    setIsCallAccepted(false);
    setIsRecievingCall(true);
    setCaller(data.from);
    setCallerName(data.name);
    setCallerSignal(data.signal);
  });

  const callUser = (id) => {
    if (connectionRef.current && !connectionRef.current.destroyed) {
      connectionRef.current.destroy();
      connectionRef.current = null;
    }

    const peer = new Peer({
      initiator: true,
      trickle: false,
      stream: localStream,
      config: {
        iceServers: [
          { urls: "stun:stun.l.google.com:19302" },
          {
            urls: "turn:216.158.239.24:3478",
            username: "dowell",
            credential: "server177368",
          },
        ],
      },
    });

    peer.on("signal", (data) => {
      socket.emit("callUser", {
        userToCall: id,
        signalData: data,
        from: myId,
        name: callerName,
      });
    });

    peer.on("stream", (stream) => {
      remoteAudioRef.current.srcObject = stream;
    });

    socket.on("callAccepted", (signal) => {
      setIsCalling(false);
      setIsCallAccepted(true);
      setIsRecievingCall(false);
      connectionRef.current.signal(signal);
    });

    setIsCalling(true);
    connectionRef.current = peer;
  };

  const answerCall = () => {
    const peer = new Peer({
      initiator: false,
      trickle: false,
      stream: localStream,
      config: {
        iceServers: [
          { urls: "stun:stun.l.google.com:19302" },
          {
            urls: "turn:216.158.239.24:3478",
            username: "dowell",
            credential: "server177368",
          },
        ],
      },
    });

    peer.on("signal", (data) => {
      socket.emit("answerCall", { signal: data, to: caller });
    });

    peer.on("stream", (stream) => {
      remoteAudioRef.current.srcObject = stream;
    });

    setIsCallAccepted(true);
    setIsRecievingCall(false);

    peer.signal(callerSignal);

    connectionRef.current = peer;
  };

  socket.on("callEnded", () => {
    setIsCalling(false);
    setIsRecievingCall(false);
    setIsCallAccepted(false);
    if (connectionRef.current) {
      connectionRef.current?.destroy();
      connectionRef.current = null;
    }
    window.location.reload();
  });

  const leaveCall = () => {
    socket.emit("endCall");
    connectionRef.current?.destroy();
    connectionRef.current = null;
    setLocalStream(null);
    setIsCalling(false);
    setIsRecievingCall(false);
    setIsCallAccepted(false);
    window.location.reload();
  };

  const getMediaStream = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      console.log("got the audio permissions!!");
      setLocalStream(stream);
    } catch (e) {
      console.log(e.message);
    }
  };

  return (
    <div className="flex w-full min-h-screen bg-gray-300 justify-center items-center">
      <audio ref={remoteAudioRef} autoPlay />
      {!isCalling && !isRecievingCall && !isCallAccepted && (
        <Call
          myId={myId}
          setIdToCall={setIdToCall}
          onClick={() => {
            callUser(idToCall);
          }}
        />
      )}
      {isCalling && <OngoingCall idToCall={idToCall} leaveCall={leaveCall} />}
      {isRecievingCall && (
        <IncomingCall
          callerId={caller}
          answerCall={answerCall}
          leaveCall={leaveCall}
        />
      )}
      {isCallAccepted && (
        <AcceptedCall
          callerId={caller ? caller : idToCall}
          leaveCall={leaveCall}
        />
      )}
    </div>
  );
};
