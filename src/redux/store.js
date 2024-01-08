import { configureStore } from "@reduxjs/toolkit";

export const store = configureStore({
  reducer: {},
//   devTools: import.meta.env.NODE_ENV !== "production",
    devTools: true,
  middleware: (getDefaultMiddleware) => getDefaultMiddleware({}).concat([]),
});
