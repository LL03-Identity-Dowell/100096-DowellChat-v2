import {io} from 'socket.io-client'

export const USER_ID = 'chidiebere';
// const SocketURL = process.env.NODE_ENV === 'production' ? undefined : 'http://localhost:4000';
const SocketURL =  'http://www.dowellchat.uxlivinglab.online/';

export const socketInstance = io(SocketURL);

// let socket;

// export default function provideSocket() {

//     if (!socket) {
//         socket = io(SocketURL);
//     }
    
//     return socket ;
// } 

