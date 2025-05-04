import "./buttons.css";
const Button = ({classname, children, onClick, toDisable})=> {
    return (
        <button className={classname} onClick={onClick} disabled={toDisable}>
            {children}
        </button>
    )
}
export default Button;