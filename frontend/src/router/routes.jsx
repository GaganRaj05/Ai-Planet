import Home from "../pages/Home"
import {createBrowserRouter, RouterProvider} from "react-router-dom"
const router = createBrowserRouter([
    {
        path:"/",
        element:<Home/>
    }
])

const Router = ()=> {
    return (
        <RouterProvider router={router}/>
    )
}
export default Router;