import { configureStore } from "@reduxjs/toolkit";
import channelsSlice from "./features/chat/channels-slice";
import serversSlice from "./features/chat/servers-slice";
import socketSlice from "./features/chat/socket-slice";

export const store = configureStore({
  reducer: {
    channels: channelsSlice,
    servers: serversSlice,
    socket: socketSlice
  },
  middleware: (getDefaultMiddleware) => getDefaultMiddleware({}).concat([]),
  devTools: true,
  //   devTools: import.meta.env.NODE_ENV !== "production",

});
