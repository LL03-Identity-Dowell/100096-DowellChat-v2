import { Link } from "react-router-dom";

export const LandingPage = () => {
  return (
    <div className="flex gap-x-5 justify-center items-center">
      <Link
        to="voice-chat"
        className="flex flex-col gap-y-8 justify-center items-center w-60 h-52 bg-white rounded-lg shadow-sm hover:shadow-xl hover:bg-green-50 cursor-pointer"
      >
        <span className="text-3xl font-bold">
          <span className="text-green-600">Voice</span> Chat
        </span>
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
          fill="currentColor"
          className="w-10 h-10 text-green-600"
        >
          <path
            fillRule="evenodd"
            d="M1.5 4.5a3 3 0 013-3h1.372c.86 0 1.61.586 1.819 1.42l1.105 4.423a1.875 1.875 0 01-.694 1.955l-1.293.97c-.135.101-.164.249-.126.352a11.285 11.285 0 006.697 6.697c.103.038.25.009.352-.126l.97-1.293a1.875 1.875 0 011.955-.694l4.423 1.105c.834.209 1.42.959 1.42 1.82V19.5a3 3 0 01-3 3h-2.25C8.552 22.5 1.5 15.448 1.5 6.75V4.5z"
            clipRule="evenodd"
          />
        </svg>
      </Link>
      <Link
        to="video-chat"
        className="flex flex-col gap-y-8 justify-center items-center w-60 h-52 bg-white rounded-lg shadow-sm hover:shadow-xl hover:bg-green-50 cursor-pointer"
      >
        <span className="text-3xl font-bold">
          <span className="text-green-600">Video</span> Chat
        </span>
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
          fill="currentColor"
          className="w-10 h-10 text-green-600"
        >
          <path d="M4.5 4.5a3 3 0 00-3 3v9a3 3 0 003 3h8.25a3 3 0 003-3v-9a3 3 0 00-3-3H4.5zM19.94 18.75l-2.69-2.69V7.94l2.69-2.69c.944-.945 2.56-.276 2.56 1.06v11.38c0 1.336-1.616 2.005-2.56 1.06z" />
        </svg>
      </Link>
    </div>
  );
};
