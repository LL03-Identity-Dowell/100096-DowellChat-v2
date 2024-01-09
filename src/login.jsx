import LoginPage from "./pages/LoginPage";
import Dashboard from "./pages/Dashboard";
import Avatar from "react-avatar";

export default function App() {
  return (
    <div className="grid h-screen grid-cols-12">
      <div className=" bg-gray-300 flex-none w-14 sm:w-20 h-screen">
        {/* Home Icon */}
        <div className="h-20 items-center flex">
          <img
            src="logo.jpg "
            alt="Home"
            className="rounded-full w-12 h-12 text-gray-300 left-3 sm:left-4 fixed"
          />
        </div>

        <div className="h-20 items-center flex">
          <img
            src="logo.jpg "
            alt="Home"
            className="rounded-full w-12 h-12 text-gray-300 left-3 sm:left-4 fixed"
          />
        </div>

        <div className="h-20 items-center flex">
          {/* <Avatar name="Foo Bar"        size="70"     className="rounded-full w-12 h-12 text-gray-300 left-3 sm:left-4 fixed"
 /> */}

          <img
            src="logo.jpg "
            alt="Home"
            className="rounded-full w-12 h-12 text-gray-300 left-3 sm:left-4 fixed"
          />
        </div>

        <div className="h-20 items-center flex">
          <img
            src="logo.jpg "
            alt="Home"
            className="rounded-full w-12 h-12 text-gray-300 left-3 sm:left-4 fixed"
          />
        </div>

        <div className="h-20 items-center flex">
          <img
            src="logo.jpg "
            alt="Home"
            className="rounded-full w-12 h-12 text-gray-300 left-3 sm:left-4 fixed"
          />
        </div>

        <div className="h-20 items-center flex">
          <img
            src="logo.jpg "
            alt="Home"
            className="rounded-full w-12 h-12 text-gray-300 left-3 sm:left-4 fixed"
          />
        </div>
        <div className="h-20 items-center flex">
          <img
            src="logo.jpg "
            alt="Home"
            className="rounded-full w-12 h-12 text-gray-300 left-3 sm:left-4 fixed"
          />
        </div>
        <div className="h-20 items-center flex">
          <img
            src="logo.jpg "
            alt="Home"
            className="rounded-full w-12 h-12 text-gray-300 left-3 sm:left-4 fixed"
          />
        </div>
      </div>

{/* The searching section */}
      <div className="col-span-2 bg-white">
        <div className="mt-6 font-bold text-3xl"> WorkflowAI </div>
        <div className="flex flex-col mt-12 mr-4 ">
          <input
            type="text"
            className="border border-green-700 h-10 px-4 ml-[-2]  bg-gray-100 w-full"
            placeholder="  Find in Chat "
          />

          <div className="flex flex-col mt-8">
            <div className="flex my-4">
              <div>
                <img
                  src="avatar.jpg"
                  alt="Circle Image"
                  className="w-16 h-16 rounded-full"
                />
              </div>
              <div className="ml-4">
                <div className="grid grid-rows-2">
                  <div className="">
                    <span className="font-semibold ">Id:</span> g77g8g8g888g
                  </div>

                  <div className="mt-1">
                    <span className="font-semibold">WORKFLOW AI</span>
                  </div>
                </div>
              </div>
            </div>

            <div className="flex  my-4">
              <div>
                <img
                  src="avatar.jpg"
                  alt="Circle Image"
                  className="w-16 h-16 rounded-full"
                />
              </div>
              <div className="ml-4">
                <div className="grid grid-rows-2">
                  <div>
                    <span className="font-semibold">Id:</span> h90h9h9h099h
                  </div>
                  <div className="mt-1">
                    <span className="font-semibold">WORKFLOW AI</span>
                  </div>
                </div>
              </div>
            </div>

            <div className="flex  my-4">
              <div>
                <img
                  src="avatar.jpg"
                  alt="Circle Image"
                  className="w-16 h-16 rounded-full"
                />
              </div>
              <div className="ml-4">
                <div className="grid grid-rows-2">
                  <div>
                    <span className="font-semibold">Id:</span> 565656565GAb
                  </div>
                  <div className="mt-1">
                    <span className="font-semibold">WORKFLOW AI</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>


    </div>
  );
}
        