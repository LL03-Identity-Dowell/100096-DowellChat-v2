import { IoIosCheckmark } from "react-icons/io";

const ChatMessage = ({ message }) => {
  return (
    <div className={`${message?.isSender ? "self-end" : "self-start"}`}>
          { 
            message?.type == 'image' ? (
                <div className="w-60 mx-10 my-5">
                    <img src={message?.imagePath} className="w-full object-cover rounded-lg" alt='image'/>
                </div> 
                ) : (
                    <div className={`${message?.isSender ? 'bg-green-300 rounded-full rounded-tr' : 'bg-blue-300 rounded-full rounded-tl self-start'} flex items-center text-sm sm:text-base text-black/50 shadow-lg py-2 px-3`}>
                        <IoIosCheckmark className="text-2xl" />
                        <p>{message?.content}</p>
                    </div>
                )
            }
    </div>
  );
};

export default ChatMessage;
