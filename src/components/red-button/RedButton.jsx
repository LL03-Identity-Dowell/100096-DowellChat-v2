export const RedButton = ({ title = "Cancel", leaveCall }) => {
  return (
    <button
      className="px-2 py-2 min-w-[80px] text-white rounded-md shadow-md bg-red-500 mb-4"
      onClick={leaveCall}
    >
      {title}
    </button>
  );
};
