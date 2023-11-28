import dummyProfile from "../../assets/images/dummy.jpg";

export const IncomingCall = ({ callerId, answerCall, leaveCall }) => {
  return (
    <div className="flex flex-col w-1/3 px-3 py-5 items-center shadow-lg rounded-lg border border-gray-300 bg-white">
      <div className="flex flex-col items-center mt-3 gap-y-2 mb-8">
        <img
          src={dummyProfile}
          alt="profile"
          className="w-36 h-36 rounded-full object-cover"
        />
        <span>{callerId} is Calling...</span>
      </div>
      <div className="flex gap-x-3 w-full items-center justify-center">
        <button
          className="px-2 py-2 min-w-[80px] text-white rounded-md shadow-md bg-green-500 mb-4"
          onClick={answerCall}
        >
          Accept
        </button>
        <button
          className="px-2 py-2 min-w-[80px] text-white rounded-md shadow-md bg-red-500 mb-4"
          onClick={leaveCall}
        >
          Cancel
        </button>
      </div>
    </div>
  );
};
