import { useState } from "react";
import Logo from "../../assets/logo.png";
import "./navBar.css";
import { useAuth } from "../../context/AuthContext";
import Button from "../ui/Button";
import { useNavigate } from "react-router-dom";
import Login from "./Login";
import SignUp from "./SignUp";

const NavBar = () => {
  const { user } = useAuth();
  const [isLoginOpen, setIsLoginOpen] = useState(false);
  const [isSignUpOpen, setIsSignUpOpen] = useState(false);
  const navigate = useNavigate();

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
              login
            </Button>
            <Button
              classname="nav-btn sign-up"
              onClick={() => setIsSignUpOpen(true)}
            >
              sign up
            </Button>
            <Button classname="nav-btn upload">upload pdf</Button>
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
    </div>
  );
};

export default NavBar;
