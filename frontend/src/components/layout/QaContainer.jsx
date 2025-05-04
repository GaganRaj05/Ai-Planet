import "./qacontainer.css"
import Greet from "./Greet";
import Message from "../ui/Messages";
import BotLogo from "../../assets/messagin-logo.png";
const QaContainer = ({conversation, isLoading}) => {
    return (
        <div className="qa-container">
            {conversation.length === 0 ? (
                <div className="qa-greet-container">
                    <Greet/>
                </div>
                ) : (
                    <div className="conversation">
                        {conversation.map((item, index)=> (
                                <Message classname={`message ${item.sender}`} key={index} message={item.message} sender={item.sender}/>
                        ))}
                        {isLoading && (
                            <div className="message bot">
                               <img className="bot-logo" src={BotLogo} alt="" />
                                <p className="bot-typing">Typing...</p>
                            </div>
                        )}
                    </div>
                )
                
            }

        </div>
    )
}
export default QaContainer;