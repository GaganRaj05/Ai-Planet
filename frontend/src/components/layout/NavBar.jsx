import { useState } from "react";
import Logo from "../../assets/logo.png";
import "./navBar.css";
import { useAuth } from "../../context/AuthContext";
import Button from "../ui/Button";
import { useNavigate } from "react-router-dom";
const NavBar = ()=> {
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const {user} = useAuth()
    
    const navigate = useNavigate();

    return (
        <div className="nav-bar-container">
            <nav className="nav-bar">
                <img className="nav-logo" src={Logo} alt=""  onClick={(e)=>{e.preventDefault(); navigate("/")}}/>
                {!user && (
                    <div>
                        <Button classname="nav-btn login">login</Button>
                        <Button classname="nav-btn sign-up">sign up</Button>                    
                        <Button classname="nav-btn upload">upload pdf</Button>                    
                    </div>
                )}
            </nav>
        </div>
    )
}

export default NavBar;