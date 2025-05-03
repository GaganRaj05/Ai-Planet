import "./buttons.css";
const Button = ({classname, children})=> {
    return (
        <button className={classname}>
            {children}
        </button>
    )
}
export default Button;