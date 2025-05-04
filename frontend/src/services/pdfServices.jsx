const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;
const uploadPdf = async (file)=> {
    try {
        const formData = new FormData();
        formData.append('file',file)
        const response = await fetch(`${BACKEND_URL}/uploads/upload-pdf`, {
            method:"POST",
            credentials:'include',
            body:formData
        });

        const data = await response.json();
        if(!response.ok) return {error:data};
        return data;
    }
    catch(err) {
        console.log(err.message);
        return {error:err.message};
    }
}

const askQuestion = async(fdata) => {
    try {
        const response = await fetch(`${BACKEND_URL}/uploads/ask-question`, {
            method:"POST",
            body:JSON.stringify(fdata),
            credentials:'include',
            headers:{"Content-type":"application/json"}
        })
        const data = await response.json();
        if(!response.ok) return {error:data};
        return data;
    }
    catch(err) {
        console.log(err.message);
        return {error:err.message};
    }
}

export {uploadPdf, askQuestion};