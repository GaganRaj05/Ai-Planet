import {  createContext, useContext, useEffect, useState } from "react";

const AuthContext = createContext();


export const AuthProvider = ({children})=> {
    const [user, setUser] = useState(null);

    useEffect(()=> {
        async function fetchUser() {
        }
        fetchUser();
    },[])
    return (
        <AuthContext.Provider value = {{user, setUser}}>
            {children}
        </AuthContext.Provider>
    )
}

export function useAuth() {
    const context = useContext(AuthContext);
    return context;
}