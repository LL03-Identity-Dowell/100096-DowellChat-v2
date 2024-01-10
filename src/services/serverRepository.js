import { socketInstance } from "./core-providers-di.js";
import { USER_ID } from "./core-providers-di.js";
import { store } from '../redux/store.js'
import { setLoading, setServers } from "../redux/features/chat/servers-slice.js";

export function getUserServers () {
    store.dispatch(setLoading(true))
    socketInstance.emit('get_user_servers', {
        user_id : USER_ID
    });
    watchServers();
}


export function watchServers () {
    socketInstance.on('server_response', (data) => {
        if(data.operation === 'get_user_servers'){
            store.dispatch(setServers(data))
        } 
  })
}


