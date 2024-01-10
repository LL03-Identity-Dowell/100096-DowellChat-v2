import { setChannelsLoading, setServerChannels, setServerId } from "../redux/features/chat/channels-slice";
import { store } from '../redux/store.js'
import { socketInstance } from "./core-providers-di.js";

export const getServerChannels = (serverId) => {
    store.dispatch(setChannelsLoading({server_id: serverId, value: true}))
    store.dispatch(setServerId({server_id: serverId}))
    socketInstance.emit('get_server_channels', { server_id: serverId});
    watchChannels(serverId)
}


export const watchChannels = (server_id) => {
    socketInstance.on('channel_response', (data) => {
        if(data.operation == 'get_server_channels'){
            store.dispatch(setServerChannels({
                data,
                server_id
            }));
        }
      })
}
