import {  createContext, useContext, useEffect, useState } from "react";
import { checkAuth } from "../services/auth";
import {toast} from "react-toastify";
const AuthContext = createContext();


export const AuthProvider = ({children})=> {
    const [user, setUser] = useState(null);
    const [pdfName, setPdfName] = useState("");
    const [pdfId, setPdfId] = useState('');
    useEffect(()=> {
        async function fetchUser() {
            const response = await checkAuth();
            if(response.error) {
                setUser(null);
                return;
            }
            setUser(response);
        }   
        fetchUser();
    },[])
    useEffect(()=> {
        console.log(user);
    },[user])
    return (
        <AuthContext.Provider value = {{user, setUser, pdfName, setPdfName, pdfId,setPdfId}}>
            {children}
        </AuthContext.Provider>
    )
}

export function useAuth() {
    const context = useContext(AuthContext);
    return context;
}