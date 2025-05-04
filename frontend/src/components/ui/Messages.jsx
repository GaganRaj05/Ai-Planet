import { useAuth } from "../../context/AuthContext";
import "./messages.css"
import AiLogo from "../../assets/messagin-logo.png";
const Message = ({ classname, message, sender, key}) => {
    const {user} = useAuth();

    return (
        <div className='message' key={key}>
            <div className={`message-container ${sender}`}>
                <div className="message-content">
                    {sender === "user" ?<button className="user-btn">{user?.name?.charAt(0)}</button>:<img className="ai-response" src={AiLogo} alt="" />}
                    
                    <div>
                        <p>{message}</p>
                    </div>
                </div>

            </div>
        </div>
    )
}
export default Message;