import React from "react";

function ListItem(props){
    return (<div className="item">
        <h3>Item</h3>
        <h3>{props.item.title}</h3>
        <p>{props.item.category}</p>
        <p>{props.item.description}</p>
    </div>
    );
}

export default ListItem;