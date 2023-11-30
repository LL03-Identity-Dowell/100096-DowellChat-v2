export const GreenButton = ({ answerCall }) => {
  return (
    <button
      className="px-2 py-2 min-w-[80px] text-white rounded-md shadow-md bg-green-500 mb-4"
      onClick={answerCall}
    >
      Accept
    </button>
  );
};
