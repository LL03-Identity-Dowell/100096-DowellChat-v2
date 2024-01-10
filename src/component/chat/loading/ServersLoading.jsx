const ServerButtonsShimmer = () => (
    Array(4).fill().map((_, index) => (
      <div className="relative h-[40px] w-[40px] animate-pulse" key={index}>
        <div className="bg-gray-100 h-full w-full rounded-md"></div>
      </div>
    ))
  );
    
export default ServerButtonsShimmer