import { useState } from "react";
import "./qaform.css";
import { IoMdSend } from "react-icons/io";
import {useAuth} from "../../context/AuthContext";
import { toast } from "react-toastify";
const QaForm = ({onSubmit})=> {
    const [question, setQuestion] = useState("");
    const {pdfId} = useAuth();
    const handleChange = (e)=> {
        setQuestion(e.target.value);
    }
    const handleSubmit = (e)=> {
        e.preventDefault();
        if(!pdfId) {
            toast.error("No pdf uploaded");
            return;
        }
        if(question) {
            onSubmit(question);
            setQuestion('');
        }
    }
    return (
        <div className="qa-form-container">
            <form className="qa-form"  method="POST" onSubmit={handleSubmit}>
                <input type="text" value={question} placeholder="Send a message" onChange={handleChange}  required/>
                <button type="Submit"><IoMdSend/></button>
            </form>
        </div>
    )
}
export default QaForm;