import { createBrowserRouter, RouterProvider } from "react-router-dom";
import "./App.css";
import { Root } from "./routes/Root";
import { LandingPage } from "./routes/landing-page";
import { VoiceChat } from "./routes/voice-chat";
import { VideoChat } from "./routes/video-chat";

function App() {
  const router = createBrowserRouter([
    {
      element: <Root />,
      children: [
        {
          path: "/",
          element: <LandingPage />,
        },
        {
          path: "voice-chat",
          element: <VoiceChat />,
        },
        {
          path: "video-chat",
          element: <VideoChat />,
        },
      ],
    },
  ]);
  return <RouterProvider router={router} />;
}

export default App;
