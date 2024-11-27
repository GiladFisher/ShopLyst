import React from "react";
import CreateItem from "./CreateItem";
import ListItem from "./ListItem";


 function List(props){
    const [listItems, setListItems] = React.useState([]);
    function addItem(newItem){
        alert("New item added " + newItem.title);
        setListItems(prevItems => {
            return [...prevItems, newItem];
        });
    }
    return(<div>
        <h1>List of Items</h1>
        <CreateItem addItem={addItem} />
        {listItems.map(item => <ListItem key={item.id} item={item} />)}
    </div>)
 }

 export default List;