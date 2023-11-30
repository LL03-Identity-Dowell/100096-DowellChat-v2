import { Outlet } from "react-router-dom";

export const Root = () => {
  return (
    <div className="w-full min-h-screen bg-gray-300">
      <Outlet />
    </div>
  );
};
