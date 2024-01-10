import { faL } from "@fortawesome/free-solid-svg-icons";
import { createSlice } from "@reduxjs/toolkit";

let _initialState = {
    isLoading : true,
    isError: false,
    success: false,
    error: '',
    servers: []
}

export const serversSlice = createSlice({
    name: 'servers',
    initialState: _initialState,
    reducers: {
        setServers(state, action) {
            let data = action.payload;
            if (data.status == 'success') {
                state.isLoading = false;
                state.success = true;
                state.isError = false;
                state.servers = data.data;
                state.error = '';
            } else {
                state.isLoading = false;
                state.isError = true;
                state.error = data.data;
                state.servers = []
                state.success = false;
            }
        },
        setLoading(state, action) {
          state.isLoading = action.payload;  
        }
    }
})

export const { setServers, setLoading } = serversSlice.actions;
export default serversSlice.reducer;