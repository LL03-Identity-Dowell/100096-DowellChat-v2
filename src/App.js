import { useEffect, useRef, useState } from "react";
import Peer from "simple-peer";
import io from "socket.io-client";

let socket = io.connect("https://www.dowellchat.uxlivinglab.online/");

function App() {
  const [localStream, setLocalStream] = useState();

  const [myId, setMyId] = useState();
  const [caller, setCaller] = useState();
  const [callerName, setCallerName] = useState("Ali");
  const [callerSignal, setCallerSignal] = useState();
  const [idToCall, setIdToCall] = useState();
  const [isRecievingCall, setIsRecievingCall] = useState(false);
  const [isCallAccepted, setIsCallAccepted] = useState(false);
  const [isCallOngoing, setIsCallOngoing] = useState(false);

  const localStreamRef = useRef(null);
  const remoteStreamRef = useRef(null);
  const connectionRef = useRef(null);

  useEffect(() => {
    navigator.mediaDevices
      .getUserMedia({ video: true, audio: true })
      .then((stream) => {
        setLocalStream(stream);
        localStreamRef.current.srcObject = stream;
        // createOffer();
      });
  }, [myId]);
  socket.on("me", (id) => {
    setMyId(id);
  });
  socket.on("callUser", (data) => {
    setIsCallOngoing(true);
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
        iceServers: [{ urls: "stun:stun.l.google.com:19302" }],
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
      remoteStreamRef.current.srcObject = stream;
    });

    socket.on("callAccepted", (signal) => {
      setIsCallAccepted(true);
      setIsRecievingCall(false);
      connectionRef.current.signal(signal);
    });

    setIsCallOngoing(true);
    connectionRef.current = peer;
  };

  const answerCall = () => {
    const peer = new Peer({
      initiator: false,
      trickle: false,
      stream: localStream,
      config: {
        iceServers: [{ urls: "stun:stun.l.google.com:19302" }],
      },
    });

    peer.on("signal", (data) => {
      socket.emit("answerCall", { signal: data, to: caller });
    });

    peer.on("stream", (stream) => {
      remoteStreamRef.current.srcObject = stream;
    });

    peer.signal(callerSignal);

    setIsCallAccepted(true);
    setIsRecievingCall(false);

    connectionRef.current = peer;
  };

  socket.on("callEnded", () => {
    setIsCallOngoing(false);
    setIsRecievingCall(false);
    setIsCallAccepted(false);
    if (connectionRef.current) {
      connectionRef.current?.destroy();
      connectionRef.current = null;
    }
  });

  const leaveCall = () => {
    socket.emit("endCall");
    connectionRef.current?.destroy();
    connectionRef.current = null;
    setIsCallOngoing(false);
    setIsRecievingCall(false);
    setIsCallAccepted(false);
  };

  return (
    <div className="App">
      <div id="videos">
        <video
          ref={localStreamRef}
          className="video-player my-video"
          id="video-1"
          autoPlay
          playsInline
          muted
        ></video>
        <video
          ref={remoteStreamRef}
          className="video-player remote-video"
          id="video-2"
          autoPlay
          playsInline
        ></video>
        <div className="call-control-container">
          {!isCallOngoing && (
            <div className="call-control">
              <input
                type="text"
                className="input"
                onInput={(event) => {
                  setIdToCall(event.target.value);
                }}
              />
              <button
                className="btn btn-blue"
                onClick={() => {
                  callUser(idToCall);
                }}
              >
                Call
              </button>
            </div>
          )}
          <span>My ID = {myId}</span>
        </div>
        {(isRecievingCall || isCallAccepted) && (
          <div className="call-actions">
            {isRecievingCall && !isCallAccepted && (
              <button
                className="btn btn-green"
                onClick={() => {
                  answerCall();
                }}
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  strokeWidth={1.5}
                  stroke="currentColor"
                  className="w-6 h-6"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M2.25 6.75c0 8.284 6.716 15 15 15h2.25a2.25 2.25 0 002.25-2.25v-1.372c0-.516-.351-.966-.852-1.091l-4.423-1.106c-.44-.11-.902.055-1.173.417l-.97 1.293c-.282.376-.769.542-1.21.38a12.035 12.035 0 01-7.143-7.143c-.162-.441.004-.928.38-1.21l1.293-.97c.363-.271.527-.734.417-1.173L6.963 3.102a1.125 1.125 0 00-1.091-.852H4.5A2.25 2.25 0 002.25 4.5v2.25z"
                  />
                </svg>
              </button>
            )}
            <button
              className="btn btn-red"
              onClick={() => {
                leaveCall();
              }}
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                strokeWidth={1.5}
                stroke="currentColor"
                className="w-6 h-6"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M15.75 3.75L18 6m0 0l2.25 2.25M18 6l2.25-2.25M18 6l-2.25 2.25m1.5 13.5c-8.284 0-15-6.716-15-15V4.5A2.25 2.25 0 014.5 2.25h1.372c.516 0 .966.351 1.091.852l1.106 4.423c.11.44-.054.902-.417 1.173l-1.293.97a1.062 1.062 0 00-.38 1.21 12.035 12.035 0 007.143 7.143c.441.162.928-.004 1.21-.38l.97-1.293a1.125 1.125 0 011.173-.417l4.423 1.106c.5.125.852.575.852 1.091V19.5a2.25 2.25 0 01-2.25 2.25h-2.25z"
                />
              </svg>
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
