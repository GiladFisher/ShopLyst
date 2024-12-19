import React from "react";

function ListItem(props){
    function handleDelete(){
        props.deleteItem(props.item.id);
    }


    return (<div className="item">
        <h3>{props.item.title}</h3>
        <p>{props.item.category}</p>
        <p>{props.item.description}</p>
        <button onClick={handleDelete}>Delete</button>
    </div>
    );
}

export default ListItem;