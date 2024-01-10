const ChannelsLoading = () => (
    Array(3).fill(null).map((_, index) => (
        <div key={index} className="flex gap-3 items-center mb-2 animate-pulse">
            <div className="w-10 h-10 bg-gray-300 rounded-full mb-4"></div>
            <div className="flex flex-col">
                <div className="w-20 h-4 bg-gray-300 mb-1"></div>
                <div className="w-16 h-3 bg-gray-300"></div>
            </div>
        </div>
        ))
  );
  
export default ChannelsLoading;
  
