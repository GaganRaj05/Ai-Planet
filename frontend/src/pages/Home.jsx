import { useState } from "react";
import NavBar from "../components/layout/NavBar";
import QaContainer from "../components/layout/QaContainer";
import QaForm from "../components/layout/QaForm";
import { useAuth } from "../context/AuthContext";
import { askQuestion } from "../services/pdfServices";
const Home = ()=> {
    const [conversation, setConversation] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const {pdfId} = useAuth();

    const handleSubmit = async (question) => {
        setIsLoading(true);
        setConversation(prev => [...prev, {sender:'user',message:question}]);
        const formData = {
            "pdf_id":pdfId,
            "question":question,
        }
        
        const response = await askQuestion(formData);
        setIsLoading(false);
        if(response.error) {
            setConversation(prev=>[...prev, {sender:'bot',message:"Sorry something went wrong"}]);
            return;
        }
        setConversation(prev=>[...prev, {sender:"bot",message:response.answer}]);

    }
    const handleLogout = ()=> {
        setConversation([]);
        return;
    }
    return (
        <>  
            <NavBar onLogout={handleLogout}/>
            <QaContainer conversation={conversation} isLoading={isLoading}/>
            <QaForm onSubmit={handleSubmit}/>
        </>
    )
}
export default Home;