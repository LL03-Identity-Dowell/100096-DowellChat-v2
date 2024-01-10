import { createSlice } from "@reduxjs/toolkit";

const _initialState = {
    isConnected: false, 
}
export const socketSlice = createSlice({
    name: 'socket',
    initialState: _initialState,
    reducers: {
        setConnected (state, action) {
            state.isConnected = action.payload.isConnected
        }
    }
})

export const { setConnected } = socketSlice.actions;
export default socketSlice.reducer;

