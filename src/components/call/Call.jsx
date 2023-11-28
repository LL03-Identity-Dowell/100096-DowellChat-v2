export const Call = ({ myId, setIdToCall, onClick }) => {
  return (
    <div className="flex flex-col w-1/2 px-3 py-5 items-center shadow-lg rounded-lg border border-gray-300 bg-white">
      <h2 className="mb-7 text-2xl font-bold">
        Welcome to <span className="text-green-600">Dowell Voice Chat</span>
      </h2>
      <span className="mb-6">Your ID: {myId}</span>
      <div className="flex w-3/5 flex-col mb-8">
        <label htmlFor="id">Socket ID:</label>
        <input
          name="id"
          type="text"
          placeholder="Enter socket ID"
          className="h-10 px-2 border border-gray-400 outline-none"
          onInput={(event) => {
            setIdToCall(event.target.value);
          }}
        />
      </div>
      <button
        className="px-2 py-2 min-w-[80px] text-white rounded-md shadow-md bg-green-500 mb-4"
        onClick={onClick}
      >
        Call
      </button>
    </div>
  );
};
