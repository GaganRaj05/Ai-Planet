import { useState } from "react";
import { toast } from "react-toastify";
import "./common.css";
import {signUpService} from "../../services/auth"
function SignUp({ onClose, onLoginClick }) {
    const [formData, setFormData] = useState({
        name: "",
        email: "",
        password: "",
        confirmPassword: "",
    });
    const [isLoading, setIsLoading] = useState(false);

    const handleChange =  (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };



    const handleSubmit = async (e) => {
        e.preventDefault();
        if(formData.password !==formData.confirmPassword) {
            toast.error("Passwords do not match")
            return;
        }
        const response = await signUpService(formData);
        if(response.error) {
            toast.error(response.error === "Failed to fetch" ? "Some error occured please try again later":response.error);
            return;
        }
        onLoginClick();
        toast.success("Account created successfully! Please Login");

    };

    return (
        <div className="modal" onClick={onClose}>
            <div className="modal-content" onClick={(e) => e.stopPropagation()}>
                <button className="close-btn" onClick={onClose}>&times;</button>
                <h2 className="text-center text-xl font-semibold mb-4 text-white">Sign Up</h2>

                <form method="POST" onSubmit={(e)=>handleSubmit(e)} encType="multipart/form-data">

                    <label htmlFor="name">Name</label>
                    <input 
                        id="name" 
                        type="text" 
                        name="name" 
                        placeholder="Enter your name" 
                        onChange={handleChange} 
                        value={formData.name} 
                        required 
                    />

                    <label htmlFor="email">Email</label>
                    <input 
                        id="email" 
                        name="email" 
                        type="email" 
                        placeholder="Enter your email" 
                        onChange={handleChange} 
                        value={formData.email} 
                        required 
                    />

                    <label htmlFor="password">Password </label>
                    <input 
                        id="password" 
                        name="password" 
                        type="password" 
                        placeholder="Enter your password" 
                        onChange={handleChange} 
                        value={formData.password} 
                        minLength={6}
                        required 
                    />

                    <label htmlFor="confirmPassword">Confirm Password</label>
                    <input 
                        id="confirmPassword" 
                        type="password" 
                        name="confirmPassword" 
                        placeholder="Confirm password" 
                        onChange={handleChange} 
                        value={formData.confirmPassword} 
                        minLength={6}
                        required 
                    />

                    <button 
                        type="submit" 
                        className="login-submit" 
                        disabled={isLoading}
                    >
                        {isLoading ? "Submitting..." : "Submit"}
                    </button>
                    <p>Already a user  ?<a  ><button style={{border:"0px",color:"#0fa958",fontSize:"22px",backgroundColor:"white",cursor:"pointer"}} onClick={()=>onLoginClick()}>Login</button></a></p>

                </form>
            </div>
        </div>
    );
}

export default SignUp;