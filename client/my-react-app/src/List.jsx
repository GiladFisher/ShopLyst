import React from "react";
import CreateItem from "./CreateItem";
import ListItem from "./ListItem";


 function List(props){
    const [listItems, setListItems] = React.useState([]);
    function deleteItem(itemId){
        setListItems(prevItems => {
            return prevItems.filter(item => {return item.id !== itemId;});
        });
    }
    function addItem(newItem){
        setListItems(prevItems => {
            return [...prevItems, newItem];
        });
    }
    return(<div>
        <h1>List of Items</h1>
        <CreateItem addItem={addItem} />
        {listItems.map(item => <ListItem key={item.id} id={item.id}  item={item} deleteItem={deleteItem} />)}
    </div>)
 }

 export default List;