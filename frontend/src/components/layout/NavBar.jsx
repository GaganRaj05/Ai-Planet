import { useState } from "react";
import Logo from "../../assets/logo.png";
import "./navBar.css";
import { useAuth } from "../../context/AuthContext";
import Button from "../ui/Button";
import { useNavigate } from "react-router-dom";
import Login from "./Login";
import SignUp from "./SignUp";
import { logoutService } from "../../services/auth";
import { toast } from "react-toastify";
import UploadPdf from "./UploadPdf"; 

const NavBar = ({onLogout}) => {
  const { user, setUser, pdfName, setPdfName, setPdfId } = useAuth();
  const [isLoginOpen, setIsLoginOpen] = useState(false);
  const [isSignUpOpen, setIsSignUpOpen] = useState(false);
  const [isUploadOpen, setIsUploadOpen] = useState(false);
  const navigate = useNavigate();

  const handleLogoutClick = async(e) => {
    const response = await logoutService();
    if(response.eror) {
      toast.error(response.error === "Failed to fetch" ? "Some error occured please try again later" : response.error);
      return;
    }
    setUser(null);
    setPdfId(null);
    setPdfName(null);
    onLogout();
    toast.success("Logout successfull");
    navigate("/",{replace:true})
  }

  return (
    <div className="nav-bar-container">
      <nav className="nav-bar">
        <img
          className="nav-logo"
          src={Logo}
          alt=""
          onClick={(e) => {
            e.preventDefault();
            navigate("/");
          }}
        />
        {!user && (
          <div>
            <Button
              classname="nav-btn login"
              onClick={() => setIsLoginOpen(true)}
            >
              Login
            </Button>
            <Button
              classname="nav-btn sign-up"
              onClick={() => setIsSignUpOpen(true)}
            >
              Sign up
            </Button>
          </div>
        )}
        {user && (
          <div>
            <Button classname={"nav-btn"} onClick={(e)=>handleLogoutClick(e)}>Logout</Button>
            {pdfName && <Button classname={" pdf-name"} >
              {pdfName}
            </Button>}
            <Button 
              classname="nav-btn upload" 
              onClick={() => setIsUploadOpen(true)}
            >
              upload PDF
            </Button>
            
          </div>
        )}
      </nav>
      {isLoginOpen && (
        <Login
          onClose={() => setIsLoginOpen(false)}
          onRegisterClick={() => {
            setIsLoginOpen(false);
            setIsSignUpOpen(true);
          }}
        />
      )}
      {isSignUpOpen && (
        <SignUp
          onClose={() => setIsSignUpOpen(false)}
          onLoginClick={() => {
            setIsSignUpOpen(false);
            setIsLoginOpen(true);
          }}
        />
      )}
      {isUploadOpen && (
        <UploadPdf onClose={() => setIsUploadOpen(false)} />
      )}
    </div>
  );
};

export default NavBar;