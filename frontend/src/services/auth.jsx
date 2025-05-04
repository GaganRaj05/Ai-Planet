const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

const loginService = async (formData) => {
    try {
        const response = await fetch(`${BACKEND_URL}/auth/sign-in`, {
            method: "POST",
            headers:{"Content-type":"application/json"},
            body:JSON.stringify(formData),
            credentials:'include'
        });

        const data = await response.json();
        if(!response.ok) return {error:data.detail};
        return data;
    }   
    catch(err) {
        console.log(err.message);
        return {error:err.message};
    }
}

const signUpService = async(formData) => {
    try {
        const response = await fetch(`${BACKEND_URL}/auth/sign-up`, {
            method:"POST",
            headers:{"Content-type":"application/json"},
            body:JSON.stringify(formData),
            credentials:'include'
        });
        const data = await response.json();
        if(!response.ok) return {error:data.detail};
        return data.message;
    }
    catch(err) {
        console.log(err.message);
        return {error:err.message};
    }
}
const checkAuth = async() => {
    try {
        const response = await fetch(`${BACKEND_URL}/auth/check-auth`,{
            method:"GET",
            credentials:'include'
        });
        const data = await response.json();
        if(!response.ok) return {error:data.detail};
        return data;
    }   
    catch(err) {
        console.log(err.message);
        return {error:err.message}
    }
}

const logoutService = async()=> {
    try {
        const response = await fetch(`${BACKEND_URL}/auth/logout`, {
            method:"POST",
            credentials:'include'
        });
        const data = await response.json();
        if(!response.ok) return {error:data}
        return data.message;
    }   
    catch(err) {
        console.log(err.message);
        return {error:err.message};
    }
}

export {loginService, signUpService, checkAuth, logoutService};