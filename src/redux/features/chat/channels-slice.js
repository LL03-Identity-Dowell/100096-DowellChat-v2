import { createSlice } from "@reduxjs/toolkit";

let _intialState = {
    server_id : null
}

export const channelsSlice = createSlice({
    name: 'channels',
    initialState: _intialState,
    reducers: {
        setServerChannels(state, action) {
            let data = action.payload.data;
            let server_id = action.payload.server_id;
            if(!state.hasOwnProperty(server_id)){
                state[server_id] = {}
            }
            if (data.status == 'success') {
                state[server_id].isLoading = false;
                state[server_id].success = true;
                state[server_id].channels = data.data;
                state[server_id].isError = false;
                state[server_id].error = '';
            } else {
                state[server_id].isLoading = false;
                state[server_id].success = false;
                state[server_id].channels = [];
                state[server_id].isError = true;
                state[server_id].error = data.data;
            }

        },

        setChannelsLoading(state, action) {
            let server_id = action.payload.server_id;
            let isLoading = action.payload.value;

            if(!state.hasOwnProperty(server_id)){
                state[server_id] = {}
            }
            
            state[server_id].isLoading = isLoading;
        },

        setServerId(state, action) {
            let server_id = action.payload.server_id;
            state.server_id = server_id;
        }

        

        // createChannel(state, action) {
        // },

        // updateChannel(state, action){
        // },

        // deleteChannel(state, action){
        // },
        // addChannelMember(state, action){

        // },
        // deleteChannelMember(state, action) {

        // }
    }
})

export const {setServerChannels, setChannelsLoading, setServerId} = channelsSlice.actions;
export default channelsSlice.reducer;