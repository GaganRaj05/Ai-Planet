import "./greet.css";
import {useAuth} from "../../context/AuthContext"
import { toast } from "react-toastify";
const Greet = ()=> {
    const {user} = useAuth();
    const handleClick =(e)=> {
        e.preventDefault();
        if(!user) {
            toast.error("Login to upload pdf files");
            return;
        }
        toast.success("Use the upload button in the top right corner")

    }
    return (
        <div className="greet-container">
            <h1>Welcome to <span className="cr">AI PLANET!...</span></h1>
            <p class="greet-info">Upload a PDF, To start asking questions.. <a href="" onClick={(e)=>handleClick(e)}> <span className="cr">Upload..</span> </a> </p>
        </div>
    )
}
export default Greet;