import { Routes, Route } from "react-router-dom";
import "./App.css";

import { LandingPage } from "./routes/landing-page";
import { VoiceChat } from "./routes/voice-chat";
import { VideoChat } from "./routes/video-chat";

function App() {
  return (
    <Routes>
      <Route path="/">
        <Route exect path="/" element={<LandingPage />} />
        <Route exect path="voice-chat" element={<VoiceChat />} />
        <Route exect path="video-chat" element={<VideoChat />} />
      </Route>
    </Routes>
  );
}

export default App;
