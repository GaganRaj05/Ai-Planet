import "./buttons.css";
const Button = ({classname, children, onClick})=> {
    return (
        <button className={classname} onClick={onClick}>
            {children}
        </button>
    )
}
export default Button;