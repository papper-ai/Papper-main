import './Button.sass';
import React from 'react';


function Button({title, color}){
    return(
        <button className="button" style={{backgroundColor: color}}>{title}</button>
    )
}

export default Button